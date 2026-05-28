# Copyright (c) 2021, Peace League and contributors
# For license information, please see license.txt
#
# 🚧 DEPRECATED: This module has been consolidated into peace_league_website/hooks.py
# and peace_league_website/doctype/plw_donation/donation.py
#
# All custom fields and DocType extensions are now managed from:
#   - apps/peace_league_website/peace_league_website/hooks.py  (custom_fields, extend_doctype_class)
#   - apps/peace_league_website/peace_league_website/doctype/plw_donation/donation.py  (Donation class)
#
# This file kept for backward compatibility during migration.
# Remove after confirming all sites have migrated.

from peace_league_website.hooks import custom_fields  # Re-export consolidated custom fields
