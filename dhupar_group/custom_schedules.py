# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
from ast import Pass
from datetime import datetime
import frappe
import json
import copy
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form
from frappe import _
from six import string_types
from frappe.model.utils import get_fetch_values
from frappe.model.mapper import get_mapped_doc
from dhupar_group.custom_actions import get_debtor_days
from calendar import monthrange


def update_dso():

    data = frappe.db.sql(
				"""
				SELECT name
				FROM `tabCustomer`
				ORDER BY name
			""",
				as_dict=1,
			)
    
    for i in data:
        frappe.db.set_value("Customer", {"name": i['name']}, "debtor_days", get_debtor_days(i['name']))

    frappe.db.commit()
