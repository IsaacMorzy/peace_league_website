import frappe
from frappe.utils import getdate


def _log(level, msg):
    try:
        with open("/tmp/gt_debug.log", "a") as f:
            f.write(f"[{level}] {msg}\n")
    except Exception:
        pass


def seed_causes(force=False):
    """Create sample Cause records."""
    try:
        frappe.flags.ignore_permissions = True
        if force:
            frappe.db.delete("Cause", {"is_active": 1})
            frappe.db.commit()
        created_counts = {}

        EDU = "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800&q=80&auto=format&fit=crop"
        YTH = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80&auto=format&fit=crop"
        COM = "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800&q=80&auto=format&fit=crop"
        TRN = "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800&q=80&auto=format&fit=crop"
        EVT = "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&q=80&auto=format&fit=crop"
        WTR = "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=800&q=80&auto=format&fit=crop"
        HTH = "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&q=80&auto=format&fit=crop"
        AGR = "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=800&q=80&auto=format&fit=crop"
        EMG = "https://images.unsplash.com/photo-1544027993-37dbfe43562a?w=800&q=80&auto=format&fit=crop"
        ENV = "https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=800&q=80&auto=format&fit=crop"

        sample_causes = [
            {"title": "Peace Education", "description": "Comprehensive peace education workshops for schools and communities, teaching conflict resolution and peaceful communication skills across East Africa.", "category": "Education", "goal_amount": 50000, "raised_amount": 15000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-01-15", "end_date": "2026-12-31", "donors_count": 45, "image": EDU},
            {"title": "Youth Empowerment Initiative", "description": "Empowering young leaders through mentorship programs, skills training, and community service opportunities in 12 communities across 5 countries.", "category": "Youth", "goal_amount": 75000, "raised_amount": 32000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-03-01", "end_date": "2026-11-30", "donors_count": 78, "image": YTH},
            {"title": "Community Reconciliation", "description": "Facilitating dialogue and reconciliation processes in communities affected by conflict and division across the Great Lakes region.", "category": "Community", "goal_amount": 40000, "raised_amount": 18000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-02-01", "end_date": "2026-10-31", "donors_count": 62, "image": COM},
            {"title": "Peace Leader Training", "description": "Intensive leadership development program for emerging peace leaders and community organizers from 20 African nations.", "category": "Training", "goal_amount": 60000, "raised_amount": 25000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-04-15", "end_date": "2026-08-15", "donors_count": 34, "image": TRN},
            {"title": "Global Peace Summit 2026", "description": "Annual international conference bringing together peace advocates, leaders, and organizations from around the world in Nairobi.", "category": "Event", "goal_amount": 120000, "raised_amount": 45000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-09-20", "end_date": "2026-09-25", "donors_count": 120, "image": EVT},
            {"title": "Girls Education Initiative", "description": "Breaking barriers to girls' education through scholarships, mentorship programs, and community advocacy in rural communities across 8 regions.", "category": "Education", "goal_amount": 80000, "raised_amount": 28000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-01-01", "end_date": "2026-12-31", "donors_count": 95, "image": EDU},
            {"title": "Clean Water Access", "description": "Building sustainable water wells and purification systems for 50 communities facing water scarcity across Kenya's arid and semi-arid regions.", "category": "Water", "goal_amount": 100000, "raised_amount": 41000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-03-15", "end_date": "2027-03-15", "donors_count": 156, "image": WTR},
            {"title": "Healthcare Outreach", "description": "Mobile health clinics bringing essential healthcare services including vaccinations, maternal care, and health education to remote villages.", "category": "Health", "goal_amount": 90000, "raised_amount": 33000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-02-01", "end_date": "2026-12-31", "donors_count": 112, "image": HTH},
            {"title": "Sustainable Agriculture", "description": "Training farmers in climate-resilient farming techniques, providing improved seeds and tools to 2,000 families across 5 agricultural regions.", "category": "Agriculture", "goal_amount": 65000, "raised_amount": 19000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-04-01", "end_date": "2027-04-01", "donors_count": 87, "image": AGR},
            {"title": "Digital Literacy for All", "description": "Bridging the digital divide by providing computer labs, internet access, and digital skills training to students in 100 underserved schools.", "category": "Education", "goal_amount": 55000, "raised_amount": 12000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-05-01", "end_date": "2027-05-01", "donors_count": 53, "image": EDU},
            {"title": "Emergency Relief Fund", "description": "Rapid emergency response providing food, shelter, and medical aid to communities affected by natural disasters and humanitarian crises across East Africa.", "category": "Emergency", "goal_amount": 200000, "raised_amount": 85000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-01-01", "end_date": "2026-12-31", "donors_count": 320, "image": EMG},
            {"title": "Women Empowerment Program", "description": "Empowering women through entrepreneurship training, financial literacy, and leadership development programs in 15 communities across 6 countries.", "category": "Community", "goal_amount": 80000, "raised_amount": 32000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-02-15", "end_date": "2027-02-15", "donors_count": 145, "image": COM},
            {"title": "Climate Resilience Initiative", "description": "Helping farming communities adapt to climate change through drought-resistant crops, water conservation techniques, and reforestation programs across 5 regions.", "category": "Agriculture", "goal_amount": 150000, "raised_amount": 45000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-03-01", "end_date": "2027-06-30", "donors_count": 98, "image": ENV},
            {"title": "Orphanage Support Program", "description": "Providing nutritious meals, school supplies, and psychosocial support to orphaned children across 25 care centers in Rwanda, DRC, and Burundi.", "category": "Community", "goal_amount": 60000, "raised_amount": 28000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-04-01", "end_date": "2026-12-31", "donors_count": 210, "image": COM},
            {"title": "Sports for Peace", "description": "Uniting communities through sports tournaments and youth leagues that promote teamwork, mutual respect, and cross-cultural understanding across 30 communities.", "category": "Youth", "goal_amount": 40000, "raised_amount": 12000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-05-01", "end_date": "2026-12-31", "donors_count": 67, "image": YTH},
            {"title": "Refugee Support Program", "description": "Helping refugees resettle and integrate into host communities through emergency shelter, legal aid, psychosocial support, and livelihood programs across refugee-hosting regions in East Africa.", "category": "Community", "goal_amount": 100000, "raised_amount": 22000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-04-01", "end_date": "2027-04-01", "donors_count": 134, "image": COM},
            {"title": "Mental Health Initiative", "description": "Providing trauma counseling, mental health awareness campaigns, and professional training for community health workers to address psychological scars of conflict across 20 communities.", "category": "Health", "goal_amount": 75000, "raised_amount": 14000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-05-01", "end_date": "2027-05-01", "donors_count": 89, "image": HTH},
            {"title": "Microfinance for Women", "description": "Providing small business loans, financial literacy training, and mentorship to women entrepreneurs in rural and peri-urban areas, enabling economic independence and community growth.", "category": "Community", "goal_amount": 85000, "raised_amount": 31000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-03-01", "end_date": "2027-03-01", "donors_count": 178, "image": COM},
            {"title": "School Feeding Program", "description": "Providing nutritious daily meals to primary school students in food-insecure regions, boosting attendance rates and academic performance across 60 schools in 4 countries.", "category": "Education", "goal_amount": 90000, "raised_amount": 26000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-02-01", "end_date": "2026-12-31", "donors_count": 201, "image": EDU},
            {"title": "Peace Journalism Training", "description": "Training journalists and media professionals in conflict-sensitive reporting, ethical journalism, and the role of media in promoting peace and social cohesion across 10 countries.", "category": "Training", "goal_amount": 50000, "raised_amount": 11000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-06-01", "end_date": "2027-06-01", "donors_count": 42, "image": TRN},
            {"title": "Art for Peace Program", "description": "Using creative expression — music, dance, theater, and visual arts — to heal trauma, bridge divides, and empower youth as peace advocates in post-conflict communities.", "category": "Youth", "goal_amount": 45000, "raised_amount": 9000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-05-15", "end_date": "2026-12-31", "donors_count": 56, "image": YTH},
            {"title": "Disaster Preparedness", "description": "Establishing community-based early warning systems, emergency response training, and stockpiling essential supplies in disaster-prone regions across the Horn of Africa.", "category": "Emergency", "goal_amount": 180000, "raised_amount": 38000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-04-01", "end_date": "2027-04-01", "donors_count": 76, "image": EMG},
            {"title": "Tree Planting Campaign", "description": "Restoring degraded landscapes through community-led reforestation, agroforestry training, and climate action awareness across 100 villages in Kenya, Uganda, and Ethiopia.", "category": "Environment", "goal_amount": 70000, "raised_amount": 15000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-06-01", "end_date": "2027-06-01", "donors_count": 210, "image": ENV},
            {"title": "Vocational Skills Training", "description": "Equipping out-of-school youth and young adults with marketable skills in carpentry, tailoring, IT, and renewable energy, creating pathways to dignified employment and self-reliance.", "category": "Education", "goal_amount": 65000, "raised_amount": 17000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-05-01", "end_date": "2027-05-01", "donors_count": 63, "image": EDU},
            {"title": "Interfaith Dialogue Initiative", "description": "Bringing together religious leaders, scholars, and community members from diverse faith traditions to foster mutual understanding, reduce sectarian tensions, and build social cohesion.", "category": "Community", "goal_amount": 55000, "raised_amount": 13000, "status": "Active", "is_active": 1, "show_on_website": 1, "start_date": "2026-04-15", "end_date": "2026-12-31", "donors_count": 48, "image": COM},
        ]

        for c in sample_causes:
            if not frappe.db.exists("Cause", {"title": c["title"]}):
                cause = frappe.get_doc({
                    "doctype": "Cause",
                    "title": c["title"],
                    "description": c["description"],
                    "category": c["category"],
                    "goal_amount": c["goal_amount"],
                    "raised_amount": c["raised_amount"],
                    "status": c["status"],
                    "is_active": c["is_active"],
                    "show_on_website": c["show_on_website"],
                    "start_date": c["start_date"],
                    "end_date": c["end_date"],
                    "donors_count": c["donors_count"],
                    "image": c.get("image", ""),
                })
                cause.insert(ignore_permissions=True)
                created_counts["causes"] = created_counts.get("causes", 0) + 1

        frappe.db.commit()
        return {"status": "success", "message": f"Created {created_counts.get('causes', 0)} causes", "data": created_counts}
    except Exception as e:
        frappe.log_error(f"Error seeding causes: {str(e)}")
        return {"status": "error", "message": str(e)}


def generate_test_data():
    """Generate sample test data for frappe_npo doctypes: Members, Donors, Chapters, Volunteers, Donations."""
    try:
        frappe.flags.ignore_permissions = True
        created_counts = {}
        _log("INFO", "=== generate_test_data START ===")

        if not frappe.db.exists("Membership Type", "Individual"):
            membership_type = frappe.get_doc({
                "doctype": "Membership Type",
                "membership_type": "Individual",
                "amount": 50,
            })
            membership_type.insert(ignore_permissions=True)
            created_counts["membership_types"] = 1
            _log("INFO", f"Membership Type created")

        members_data = [
            {"member_name": "Alice Johnson", "email_id": "alice.johnson@email.com", "phone": "+1-555-0101", "membership_type": "Individual"},
            {"member_name": "Robert Smith", "email_id": "robert.smith@email.com", "phone": "+1-555-0102", "membership_type": "Individual"},
            {"member_name": "Maria Garcia", "email_id": "maria.garcia@email.com", "phone": "+1-555-0103", "membership_type": "Individual"},
            {"member_name": "James Wilson", "email_id": "james.wilson@email.com", "phone": "+1-555-0104", "membership_type": "Individual"},
            {"member_name": "Sarah Brown", "email_id": "sarah.brown@email.com", "phone": "+1-555-0105", "membership_type": "Individual"},
        ]

        for m in members_data:
            if not frappe.db.exists("Member", {"email_id": m["email_id"]}):
                _log("INFO", f"Creating member: {m['member_name']} ({m['email_id']})")
                member = frappe.get_doc({
                    "doctype": "Member",
                    "naming_series": "NPO-MEM-.YYYY.-",
                    "member_name": m["member_name"],
                    "email_id": m["email_id"],
                    "membership_type": m["membership_type"],
                    "membership_expiry_date": "2026-12-31",
                })
                member.insert(ignore_permissions=True)
                created_counts["members"] = created_counts.get("members", 0) + 1
                _log("INFO", f"Member inserted: {member.name}")

        for dt in ["Individual", "Organization"]:
            if not frappe.db.exists("Donor Type", dt):
                dt_doc = frappe.get_doc({"doctype": "Donor Type", "donor_type": dt})
                dt_doc.insert(ignore_permissions=True)
                created_counts["donor_types"] = created_counts.get("donor_types", 0) + 1

        if not frappe.db.exists("Custom Field", "Donor-naming_series"):
            cf = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Donor",
                "fieldname": "naming_series",
                "label": "Series",
                "fieldtype": "Select",
                "options": "NPO-DON-.YYYY.-",
                "insert_after": "donor_name",
                "allow_on_submit": 1,
            })
            cf.insert(ignore_permissions=True)
        frappe.db.sql("UPDATE `tabDocType` SET `autoname`='naming_series:' WHERE `name`='Donor'")

        donors_data = [
            {"donor_name": "William Thompson", "email": "william.thompson@charity.org", "phone_number": "+1-555-0201", "donor_type": "Individual"},
            {"donor_name": "Elizabeth Davis", "email": "elizabeth.davis@charity.org", "phone_number": "+1-555-0202", "donor_type": "Individual"},
            {"donor_name": "Peace Foundation", "email": "donations@peacefdn.org", "phone_number": "+1-555-0203", "donor_type": "Organization"},
            {"donor_name": "Michael Lee", "email": "michael.lee@email.com", "phone_number": "+1-555-0204", "donor_type": "Individual"},
            {"donor_name": "Global Aid Trust", "email": "giving@globalaid.org", "phone_number": "+1-555-0205", "donor_type": "Organization"},
        ]

        for d in donors_data:
            if not frappe.db.exists("Donor", {"email": d["email"]}):
                donor = frappe.get_doc({
                    "doctype": "Donor",
                    "donor_name": d["donor_name"],
                    "email": d["email"],
                    "phone_number": d["phone_number"],
                    "donor_type": d["donor_type"],
                })
                donor.insert(ignore_permissions=True)
                created_counts["donors"] = created_counts.get("donors", 0) + 1

        chapters_data = [
            {"chapter_name": "Peace Builders New York", "region": "Northeast", "city": "New York", "address": "123 Peace Avenue, NY 10001"},
            {"chapter_name": "California Peace Alliance", "region": "West", "city": "Los Angeles", "address": "456 Harmony Street, CA 90001"},
            {"chapter_name": "Midwest Peace Initiative", "region": "Midwest", "city": "Chicago", "address": "789 Unity Road, IL 60601"},
            {"chapter_name": "Southern Peace Network", "region": "South", "city": "Atlanta", "address": "321 Calm Lane, GA 30301"},
            {"chapter_name": "Peace Council Texas", "region": "South", "city": "Houston", "address": "654 Serenity Blvd, TX 77001"},
        ]

        if not frappe.db.exists("Custom Field", "Chapter-naming_series"):
            cf = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Chapter",
                "fieldname": "naming_series",
                "label": "Series",
                "fieldtype": "Select",
                "options": "NPO-CHAP-.YYYY.-",
                "insert_after": "chapter_head",
                "allow_on_submit": 1,
            })
            cf.insert(ignore_permissions=True)
        frappe.db.sql("UPDATE `tabDocType` SET `autoname`='naming_series:' WHERE `name`='Chapter'")
        frappe.clear_cache(doctype="Chapter")

        first_member_list = frappe.get_all("Member", fields=["name"], order_by="creation asc", limit=1)
        first_member = first_member_list[0].name if first_member_list else None

        for c in chapters_data:
            if not frappe.db.exists("Chapter", {"introduction": c["chapter_name"]}):
                chapter = frappe.get_doc({
                    "doctype": "Chapter",
                    "naming_series": "NPO-CHAP-.YYYY.-",
                    "introduction": c["chapter_name"],
                    "chapter_head": first_member,
                    "region": c["region"],
                    "city": c["city"],
                    "address": c["address"],
                    "published": 1,
                })
                chapter.insert(ignore_permissions=True)
                created_counts["chapters"] = created_counts.get("chapters", 0) + 1

        if not frappe.db.exists("Volunteer Type", "Event Volunteer"):
            vt1 = frappe.get_doc({"doctype": "Volunteer Type", "title": "Event Volunteer"})
            vt1.insert(ignore_permissions=True)
            created_counts["volunteer_types"] = created_counts.get("volunteer_types", 0) + 1

        if not frappe.db.exists("Volunteer Type", "Community Outreach"):
            vt2 = frappe.get_doc({"doctype": "Volunteer Type", "title": "Community Outreach"})
            vt2.insert(ignore_permissions=True)
            created_counts["volunteer_types"] = created_counts.get("volunteer_types", 0) + 1

        volunteers_data = [
            {"volunteer_name": "Emily Chen", "email": "emily.chen@email.com", "phone_number": "+1-555-0301", "volunteer_type": "Event Volunteer"},
            {"volunteer_name": "David Martinez", "email": "david.martinez@email.com", "phone_number": "+1-555-0302", "volunteer_type": "Community Outreach"},
            {"volunteer_name": "Jennifer White", "email": "jennifer.white@email.com", "phone_number": "+1-555-0303", "volunteer_type": "Event Volunteer"},
            {"volunteer_name": "Christopher Taylor", "email": "chris.taylor@email.com", "phone_number": "+1-555-0304", "volunteer_type": "Community Outreach"},
            {"volunteer_name": "Amanda Anderson", "email": "amanda.anderson@email.com", "phone_number": "+1-555-0305", "volunteer_type": "Event Volunteer"},
        ]

        for v in volunteers_data:
            if not frappe.db.exists("Volunteer", {"email": v["email"]}):
                volunteer = frappe.get_doc({
                    "doctype": "Volunteer",
                    "volunteer_name": v["volunteer_name"],
                    "email": v["email"],
                    "phone_number": v["phone_number"],
                    "volunteer_type": v["volunteer_type"],
                })
                volunteer.insert(ignore_permissions=True)
                created_counts["volunteers"] = created_counts.get("volunteers", 0) + 1

        donations_data = [
            {"donor": "william.thompson@charity.org", "amount": 250, "mode_of_payment": "Online"},
            {"donor": "elizabeth.davis@charity.org", "amount": 500, "mode_of_payment": "Wire Transfer"},
            {"donor": "donations@peacefdn.org", "amount": 1000, "mode_of_payment": "Cheque"},
            {"donor": "michael.lee@email.com", "amount": 100, "mode_of_payment": "Online"},
            {"donor": "giving@globalaid.org", "amount": 2000, "mode_of_payment": "Wire Transfer"},
        ]

        for d in donations_data:
            donor_name = frappe.db.get_value("Donor", {"email": d["donor"]}, "name")
            if donor_name and not frappe.db.exists("Donation", {"donor": donor_name, "amount": d["amount"]}):
                donation = frappe.get_doc({
                    "doctype": "Donation",
                    "naming_series": "DON-.YYYY.-",
                    "donor": donor_name,
                    "amount": d["amount"],
                    "currency": "USD",
                    "mode_of_payment": d["mode_of_payment"],
                    "date": "2025-06-01",
                    "paid": 1,
                    "company": "Peace League Africa",
                })
                donation.insert(ignore_permissions=True)
                created_counts["donations"] = created_counts.get("donations", 0) + 1

        frappe.db.commit()
        _log("INFO", f"=== SUCCESS: created {created_counts}")

        return {
            "status": "success",
            "message": "Test data generated successfully",
            "data": {
                "records_created": created_counts,
                "total_records": sum(created_counts.values())
            }
        }
    except Exception as e:
        import traceback
        _log("ERROR", f"EXCEPTION: {type(e).__name__}: {e}")
        _log("ERROR", traceback.format_exc())
        frappe.log_error(f"Error generating test data: {str(e)}")
        return {"status": "error", "message": str(e)}
