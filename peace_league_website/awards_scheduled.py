"""
Scheduled tasks for Peace League Africa Awards.

Registered in hooks.py via scheduler_events.
- close_voting(): Called after Dec 5 00:00 EAT to freeze voting
- publish_results(): Called on Dec 5 18:00 EAT to compute and release winners
"""

import datetime

import frappe

logger = frappe.logger("awards", allow_site=True, file_count=5)

# ── Constants ──

VOTING_CLOSES_UTC = datetime.datetime(2026, 12, 4, 21, 0, 0)  # Dec 5 00:00 EAT
RESULTS_ANNOUNCED_UTC = datetime.datetime(2026, 12, 17, 7, 0, 0)  # Dec 17 10:00 AM EAT


def close_voting():
    """Scheduled task: close voting at Dec 5 00:00 EAT.

    Sets a cache flag so that the cast_vote endpoint rejects new votes.
    Also logs how many votes were cast before closing.
    Marks each Award Category as voting_closed=1.
    """
    now_utc = datetime.datetime.utcnow()

    # Safety guard: don't close before the scheduled date
    if now_utc < VOTING_CLOSES_UTC:
        logger.warning(
            f"close_voting called too early (now={now_utc}, target={VOTING_CLOSES_UTC}). Skipping."
        )
        return {"status": "skipped", "reason": "too_early"}

    # Set cache flag (persists in Redis, survives process restarts)
    frappe.cache().set_value("awards_voting_closed", True)

    # Mark all active categories as voting closed
    categories = frappe.get_list(
        "Award Category",
        filters={"is_active": 1},
        fields=["name", "category_name"],
    )
    for cat in categories:
        doc = frappe.get_doc("Award Category", cat.name)
        doc.db_set("is_active", 0)  # ponytail: reuse is_active flag to close voting

    # Aggregate vote totals in a single query
    total_votes = frappe.db.count("Award Vote")
    category_count = len(categories)
    logger.info(
        f"Voting closed. {total_votes} total votes across {category_count} categories."
    )

    frappe.db.commit()

    return {
        "status": "success",
        "data": {
            "categories_closed": category_count,
            "total_votes": total_votes,
        },
    }


def publish_results():
    """Scheduled task: compute winners at Dec 5 18:00 EAT.

    Runs the same computation as get_results() but logs winners and sets
    a cache flag so the frontend knows results are published.
    """
    now_utc = datetime.datetime.utcnow()

    # Safety guard
    if now_utc < RESULTS_ANNOUNCED_UTC:
        logger.warning(
            f"publish_results called too early (now={now_utc}, target={RESULTS_ANNOUNCED_UTC}). Skipping."
        )
        return {"status": "skipped", "reason": "too_early"}

    # Aggregate all vote counts per category in a single query to avoid N+1
    category_totals = frappe.db.sql(
        """
        SELECT category, COUNT(*) as total_votes
        FROM `tabAward Vote`
        GROUP BY category
        """,
        as_dict=True,
    )
    total_map = {r.category: r.total_votes for r in category_totals}

    # Get top nominee per category in a single query
    winners_sql = frappe.db.sql(
        """
        SELECT v1.category, v1.nominee, COUNT(*) as cnt
        FROM `tabAward Vote` v1
        INNER JOIN (
            SELECT category, MAX(vote_count) as max_cnt
            FROM (
                SELECT category, nominee, COUNT(*) as vote_count
                FROM `tabAward Vote`
                GROUP BY category, nominee
            ) t1
            GROUP BY category
        ) t2 ON v1.category = t2.category
        GROUP BY v1.category, v1.nominee
        HAVING COUNT(*) = t2.max_cnt
        """,
        as_dict=True,
    )
    top_map = {r.category: r for r in winners_sql}

    # Build winners list from categories
    categories = frappe.get_list("Award Category", fields=["name", "category_name", "slug"])
    winners = []
    for cat in categories:
        total = total_map.get(cat.name, 0)
        top = top_map.get(cat.name)
        winner_data = {"category": cat.category_name, "slug": cat.slug, "total_votes": total}

        if top and top.nominee:
            winner_doc = frappe.get_doc("Award Nominee", top.nominee)
            winner_data["winner"] = winner_doc.nominee_name
            winner_data["votes"] = top.cnt
            winner_data["percentage"] = round((top.cnt / total) * 100, 1) if total else 0
        else:
            winner_data["winner"] = None
            winner_data["votes"] = 0
            winner_data["percentage"] = 0

        winners.append(winner_data)

    # Set published flag in cache (persists in Redis, survives restarts)
    frappe.cache().set_value("awards_results_published", True)
    frappe.cache().set_value("awards_results", winners)

    logger.info(f"Results published: {len(winners)} categories.")

    # Optionally notify admin users
    _notify_results_published(len(winners))

    return {
        "status": "success",
        "data": {"categories": len(winners), "winners": winners},
    }


def _notify_results_published(category_count):
    """Send a system notification that awards results are published."""
    try:
        # Has Role is a child table of User, not a field on User doctype
        role_assignments = frappe.db.get_all(
            "Has Role",
            filters={"role": "Awards Admin", "parenttype": "User"},
            pluck="parent",
        )
        if not role_assignments:
            logger.info("No Awards Admin users to notify.")
            return

        enabled_users = frappe.db.get_all(
            "User",
            filters={"name": ["in", role_assignments], "enabled": 1},
            pluck="name",
        )
        for user in enabled_users:
            frappe.publish_realtime(
                "awards_results_published",
                {"message": f"Awards results are now live for {category_count} categories!"},
                user=user,
            )
    except Exception as e:
        logger.warning(f"Failed to notify results: {e}")
