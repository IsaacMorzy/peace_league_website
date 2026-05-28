"""
Seed data utilities for Peace League Website.

This module delegates to domain-specific seeders in the `seed/` sub-package.
Kept for backward compatibility - all logic is now in individual seed modules.

Graph edges:
- calls: seed.seed_causes, seed.seed_members, seed.seed_donors
- calls: seed.seed_volunteers, seed.seed_chapters, seed.seed_donations
"""

import frappe

logger = frappe.logger("peace_league", allow_site=True, file_count=5)

from peace_league_website.utils.seed.seed_causes import seed_causes
from peace_league_website.utils.seed.seed_members import seed_members
from peace_league_website.utils.seed.seed_donors import seed_donors
from peace_league_website.utils.seed.seed_volunteers import seed_volunteers
from peace_league_website.utils.seed.seed_chapters import seed_chapters
from peace_league_website.utils.seed.seed_donations import seed_donations


def generate_test_data():
    """Generate sample test data for all DocTypes.

    Calls each domain seeder in dependency order (members first, then
    chapters/volunteers/donors, then donations).

    Graph edges:
    - creates: Member, Donor, Chapter, Volunteer, Donation
    - creates: Membership Type, Donor Type, Volunteer Type
    """
    try:
        frappe.flags.ignore_permissions = True
        all_created = {}

        logger.info("=== generate_test_data START ===")

        # Order matters: members → chapters, volunteers, donors → donations
        all_created.update(seed_members())
        all_created.update(seed_donors())
        all_created.update(seed_chapters())
        all_created.update(seed_volunteers())
        all_created.update(seed_donations())

        frappe.db.commit()
        logger.info(f"=== SUCCESS: created {all_created} ===")

        return {
            "status": "success",
            "message": "Test data generated successfully",
            "data": {
                "records_created": all_created,
                "total_records": sum(all_created.values()),
            },
        }
    except Exception as e:
        import traceback
        logger.error(f"EXCEPTION: {type(e).__name__}: {e}")
        logger.error(traceback.format_exc())
        frappe.log_error(f"Error generating test data: {e}")
        return {"status": "error", "message": str(e)}
