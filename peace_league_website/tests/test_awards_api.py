"""
Unit tests for peace_league_website.api_awards

Run with: bench --site <site> run-tests --module peace_league_website.tests.test_awards_api
"""

import unittest

import frappe
from frappe import _
from frappe.tests import IntegrationTestCase
from unittest.mock import patch

from peace_league_website.api_awards import (
    get_categories,
    get_category,
    create_nomination,
    cast_vote,
)


class TestAwardsAPI(IntegrationTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create test category if not exists (once for class)
        if not frappe.db.exists("Award Category", {"slug": "test-category"}):
            cat = frappe.get_doc({
                "doctype": "Award Category",
                "category_name": "Test Category",
                "slug": "test-category",
                "description": "For testing",
                "is_active": 1,
                "sort_order": 1,
            })
            cat.insert(ignore_permissions=True)
            frappe.db.commit()
        cls.category_name = frappe.db.get_value("Award Category", {"slug": "test-category"}, "name")
        # Create nominee if not exists
        if not frappe.db.exists("Award Nominee", {"nominee_name": "Test Nominee"}):
            nominee = frappe.get_doc({
                "doctype": "Award Nominee",
                "nominee_name": "Test Nominee",
                "category": cls.category_name,
                "description": "A test nominee",
                "status": "Active",
                "submission_date": frappe.utils.nowdate(),
            })
            nominee.insert(ignore_permissions=True)
            # Create 3 votes
            for _ in range(3):
                vote = frappe.get_doc({
                    "doctype": "Award Vote",
                    "nominee": nominee.name,
                    "category": cls.category_name,
                    "ip_address": "127.0.0.1",
                })
                vote.insert(ignore_permissions=True)
            frappe.db.commit()
        cls.nominee_name = frappe.db.get_value("Award Nominee", {"nominee_name": "Test Nominee"}, "name")

    def test_get_categories_returns_active(self):
        result = get_categories()
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["data"], list)
        slugs = [c["slug"] for c in result["data"]]
        self.assertIn("test-category", slugs)

    def test_get_category_returns_nominees_with_vote_counts(self):
        result = get_category("test-category")
        self.assertEqual(result["status"], "success")
        data = result["data"]
        self.assertIn("category", data)
        self.assertIn("nominees", data)
        nominees = data["nominees"]
        self.assertTrue(len(nominees) > 0)
        # Find our test nominee
        test_nom = next((n for n in nominees if n["name"] == self.__class__.nominee_name), None)
        self.assertIsNotNone(test_nom, "Test nominee should be present")
        self.assertEqual(test_nom["votes"], 3)  # we created 3 votes

    def test_get_category_not_found(self):
        result = get_category("non-existent-slug")
        self.assertEqual(result["status"], "error")
        self.assertIn("not found", result["message"].lower())

    def test_cast_vote_creates_and_counts(self):
        # Create a fresh nominee with no votes
        fresh_nom = frappe.get_doc({
            "doctype": "Award Nominee",
            "nominee_name": "Fresh Test Nominee",
            "category": self.__class__.category_name,
            "description": "Fresh",
            "status": "Active",
            "submission_date": frappe.utils.nowdate(),
        })
        fresh_nom.insert(ignore_permissions=True)
        frappe.db.commit()

        # Cast vote via API (mock IP to avoid rate limit issues)
        with patch.object(frappe, 'request', create=True) as mock_req:
            mock_req.remote_addr = "127.0.0.2"
            result = cast_vote(nominee_id=fresh_nom.name, category_slug="test-category")
        self.assertEqual(result["status"], "success")
        # Verify vote count increased
        res = get_category("test-category")
        nominees = res["data"]["nominees"]
        fresh = next(n for n in nominees if n["name"] == fresh_nom.name)
        self.assertEqual(fresh["votes"], 1)

        # Clean up: delete the vote and nominee
        frappe.db.delete("Award Vote", {"nominee": fresh_nom.name})
        fresh_nom.delete(ignore_permissions=True)
        frappe.db.commit()

    def test_create_nomination_requires_fields(self):
        # Empty form should fail
        result = create_nomination()
        self.assertEqual(result["status"], "error")
        self.assertIn("required", result["message"].lower())


if __name__ == "__main__":
    unittest.main()
