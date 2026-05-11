import frappe
import random
from frappe import _
from datetime import datetime, timedelta

def generate_sample_data():
    frappe.flags.ignore_permissions = True

    print("Generating sample data for Frappe NPO...")

    created_records = []

    # 1. Create Volunteer Types
    volunteer_types = ["Teaching", "Medical", "Community Outreach", "Fundraising", "Administrative", "Event Support"]
    for vt_name in volunteer_types:
        if not frappe.db.exists("Volunteer Type", vt_name):
            vt = frappe.get_doc({
                "doctype": "Volunteer Type",
                "volunteer_type": vt_name,
                "description": f"Volunteers for {vt_name.lower()} activities"
            })
            vt.insert(ignore_permissions=True)
            created_records.append(f"Volunteer Type: {vt_name}")
            print(f"Created Volunteer Type: {vt_name}")

    # 2. Create Volunteer Skills
    skills = ["First Aid", "CPR", "Teaching", "Counseling", "Medical", "Cooking", "Driving", "Photography", "IT Support", "Languages"]
    for skill_name in skills:
        if not frappe.db.exists("Volunteer Skill", skill_name):
            skill = frappe.get_doc({
                "doctype": "Volunteer Skill",
                "skill_name": skill_name
            })
            skill.insert(ignore_permissions=True)
            created_records.append(f"Volunteer Skill: {skill_name}")
            print(f"Created Volunteer Skill: {skill_name}")

    # 3. Create Members
    member_types = ["Individual", "Corporate", "Student", "Senior"]
    for mt in member_types:
        if not frappe.db.exists("Membership Type", mt):
            mem_type = frappe.get_doc({
                "doctype": "Membership Type",
                "membership_type": mt,
                "amount": random.choice([500, 1000, 2500, 5000]),
                "description": f"{mt} membership tier"
            })
            mem_type.insert(ignore_permissions=True)
            created_records.append(f"Membership Type: {mt}")
            print(f"Created Membership Type: {mt}")

    # 4. Create Chapters
    chapters_data = [
        {"name": "Nairobi Chapter", "city": "Nairobi", "country": "Kenya"},
        {"name": "Mombasa Chapter", "city": "Mombasa", "country": "Kenya"},
        {"name": "Kisumu Chapter", "city": "Kisumu", "country": "Kenya"},
        {"name": "Nakuru Chapter", "city": "Nakuru", "country": "Kenya"},
        {"name": "Eldoret Chapter", "city": "Eldoret", "country": "Kenya"},
    ]

    for ch_data in chapters_data:
        if not frappe.db.exists("Chapter", ch_data["name"]):
            chapter = frappe.get_doc({
                "doctype": "Chapter",
                "chapter_name": ch_data["name"],
                "city": ch_data["city"],
                "country": ch_data["country"],
                "description": f"Peace League {ch_data['city']} Chapter",
                "email": f"info@{ch_data['name'].lower().replace(' ', '')}.org",
                "phone": f"+254{random.randint(700000000, 799999999)}"
            })
            chapter.insert(ignore_permissions=True)
            created_records.append(f"Chapter: {ch_data['name']}")
            print(f"Created Chapter: {ch_data['name']}")

    # 5. Create Donor Types
    donor_types = ["Individual", "Corporate", "Foundation", "Government", "NGO Partner"]
    for dt in donor_types:
        if not frappe.db.exists("Donor Type", dt):
            donor_type = frappe.get_doc({
                "doctype": "Donor Type",
                "donor_type": dt,
                "description": f"{dt} donor category"
            })
            donor_type.insert(ignore_permissions=True)
            created_records.append(f"Donor Type: {dt}")
            print(f"Created Donor Type: {dt}")

    # 6. Create Donors
    donor_names = [
        "John Smith Foundation",
        "ABC Corporation",
        "Global Aid Foundation",
        "Hope Fund",
        "Community Builders Inc",
        "Green Earth Initiative",
        "Unity Trust",
        "Bright Future Foundation"
    ]

    for donor_name in donor_names:
        if not frappe.db.exists("Donor", donor_name):
            donor = frappe.get_doc({
                "doctype": "Donor",
                "donor_name": donor_name,
                "donor_type": random.choice(donor_types),
                "email": f"donations@{donor_name.lower().replace(' ', '').replace(',', '')}.org",
                "phone": f"+254{random.randint(700000000, 799999999)}",
                "address": f"P.O. Box {random.randint(1000, 99999)}, Nairobi",
                "description": f"Major donor organization"
            })
            donor.insert(ignore_permissions=True)
            created_records.append(f"Donor: {donor_name}")
            print(f"Created Donor: {donor_name}")

    # 7. Create Beneficiaries
    beneficiary_names = [
        "Grace Wanjiku",
        "James Ochieng",
        "Mary Akinyi",
        "Peter Oduya",
        "Sarah Nekesa",
        "David Maina",
        "Faith Atieno",
        "Michael Kipkorir",
        "Ruth Kemunto",
        "Samuel Karanja",
        "Hannah Mwangi",
        "Joseph Odhiambo",
        "Mary Wambui",
        "Samuel Kipng'eno",
        "Grace Chebet",
    ]

    for i, name in enumerate(beneficiary_names):
        if not frappe.db.exists("Beneficiary", name):
            beneficiary = frappe.get_doc({
                "doctype": "Beneficiary",
                "beneficiary_name": name,
                "first_name": name.split()[0],
                "last_name": name.split()[1] if len(name.split()) > 1 else "",
                "gender": random.choice(["Male", "Female"]),
                "date_of_birth": (datetime.now() - timedelta(days=random.randint(3650, 15000))).strftime("%Y-%m-%d"),
                "phone": f"+254{random.randint(700000000, 799999999)}",
                "email": f"{name.lower().replace(' ', '.')}@email.com",
                "address": f"House {random.randint(1, 500)}, Street {random.randint(1, 100)}",
                "city": random.choice(["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]),
                "country": "Kenya",
                "status": "Active"
            })
            beneficiary.insert(ignore_permissions=True)
            created_records.append(f"Beneficiary: {name}")
            print(f"Created Beneficiary: {name}")

    # 8. Create Cases
    case_types = ["Education Support", "Healthcare", "Shelter", "Family Reintegration", "Vocational Training"]
    for i, name in enumerate(beneficiary_names[:10]):
        case_name = f"CASE-{1000 + i}"
        if not frappe.db.exists("Case", case_name):
            case = frappe.get_doc({
                "doctype": "Case",
                "case_id": case_name,
                "case_type": random.choice(case_types),
                "beneficiary": name,
                "status": random.choice(["Open", "In Progress", "Pending Review"]),
                "priority": random.choice(["Low", "Medium", "High"]),
                "description": f"Case for {name} - {random.choice(case_types)} support"
            })
            case.insert(ignore_permissions=True)
            created_records.append(f"Case: {case_name}")
            print(f"Created Case: {case_name}")

    # 9. Create Donations
    for i in range(10):
        donation_name = f"DON-{2024}{random.randint(1000, 9999)}"
        if not frappe.db.exists("Donation", donation_name):
            donation = frappe.get_doc({
                "doctype": "Donation",
                "donor": random.choice(donor_names),
                "amount": random.randint(5000, 250000),
                "date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
                "payment_method": random.choice(["Bank Transfer", "Cash", "Credit Card", "M-Pesa"]),
                "status": "Received",
                "remarks": f"Donation received for program support"
            })
            donation.insert(ignore_permissions=True)
            created_records.append(f"Donation: {donation_name}")
            print(f"Created Donation: {donation_name}")

    # 10. Create Volunteers
    volunteer_names = [
        "Alice Kamau",
        "Bob Ochieng",
        "Carol Atieno",
        "Daniel Kiprop",
        "Emma Wanjiku",
        "Frank Odhiambo",
        "Grace Akinyi",
        "Henry Kipng'eno"
    ]

    for name in volunteer_names:
        if not frappe.db.exists("Volunteer", name):
            volunteer = frappe.get_doc({
                "doctype": "Volunteer",
                "volunteer_name": name,
                "first_name": name.split()[0],
                "last_name": name.split()[1] if len(name.split()) > 1 else "",
                "email": f"{name.lower().replace(' ', '.')}@email.com",
                "phone": f"+254{random.randint(700000000, 799999999)}",
                "volunteer_type": random.choice(volunteer_types),
                "availability": random.choice(["Weekdays", "Weekends", "Flexible"]),
                "status": "Active"
            })
            volunteer.insert(ignore_permissions=True)
            created_records.append(f"Volunteer: {name}")
            print(f"Created Volunteer: {name}")

    # 11. Create Beneficiary Programs
    programs = [
        "Education Support Program",
        "Healthcare Access Program",
        "Food Security Initiative",
        "Shelter and Housing Program",
        "Vocational Training Program",
        "Family Reintegration Program",
        "Psychosocial Support Program"
    ]

    for prog_name in programs:
        if not frappe.db.exists("Beneficiary Program", prog_name):
            program = frappe.get_doc({
                "doctype": "Beneficiary Program",
                "program_name": prog_name,
                "description": f"Comprehensive {prog_name.lower()} for vulnerable populations",
                "start_date": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(days=275)).strftime("%Y-%m-%d"),
                "budget": random.randint(500000, 5000000),
                "status": "Active"
            })
            program.insert(ignore_permissions=True)
            created_records.append(f"Beneficiary Program: {prog_name}")
            print(f"Created Beneficiary Program: {prog_name}")

    # 12. Create Counties
    counties = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Kakamega", "Kiambu", "Machakos", "Meru"]
    for county_name in counties:
        if not frappe.db.exists("County", county_name):
            county = frappe.get_doc({
                "doctype": "County",
                "county_name": county_name,
                "description": f"{county_name} County"
            })
            county.insert(ignore_permissions=True)
            created_records.append(f"County: {county_name}")
            print(f"Created County: {county_name}")

    # 13. Create States
    states = ["Nairobi", "Coast", "Western", "Rift Valley", "Central", "Eastern", "North Eastern"]
    for state_name in states:
        if not frappe.db.exists("State", state_name):
            state = frappe.get_doc({
                "doctype": "State",
                "state_name": state_name,
                "country": "Kenya"
            })
            state.insert(ignore_permissions=True)
            created_records.append(f"State: {state_name}")
            print(f"Created State: {state_name}")

    print(f"\n✅ Successfully created {len(created_records)} sample records!")
    print("\nCreated records summary:")
    for record in created_records:
        print(f"  - {record}")

    return created_records

if __name__ == "__main__":
    generate_sample_data()