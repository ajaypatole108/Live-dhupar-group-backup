// Copyright (c) 2016, Gurshish Dhupar and contributors
// For license information, please see license.txt
/* eslint-disable */

// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors // License: GNU General Public License v3. See license.txt frappe.query_reports["Dhupar GSTR-1"] = {
frappe.query_reports["HSN SUMMARY"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"type_of_business",
			"label": __("Type of Business"),
			"fieldtype": "Select",
			"reqd": 1,
			"options": ["HSN summary"],
			"default": "B2B"
		}
	]
}
