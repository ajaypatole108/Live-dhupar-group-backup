// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["TCS Bills"] = {
        "filters": [
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
                }
        ]
}




