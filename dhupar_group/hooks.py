# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version
# from dhupar_group import dhupar_group


app_name = "dhupar_group"
app_title = "Dhupar Group"
app_publisher = "Gurshish Dhupar"
app_description = "A set of automation utilities for Dhupar Group"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "gurshish@dhupargroup.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/dhupar_group/css/dhupar_group.css"
app_include_js = "/assets/js/dhupar_group.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/dhupar_group/css/dhupar_group.css"
# web_include_js = "/assets/dhupar_group/js/dhupar_group.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
		"Blanket Order":"public/js/blanket_order.js",
		"Customer":"public/js/customer.js"
	}

override_doctype_class ={
        'Customer':'dhupar_group.overrides.customer.CustomCustomer'
}

# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# fixtures
fixtures = [
	'Custom Field', 'Property Setter', 'Role', 'Designation', 'Print Format', \
	'Workflow', 'Workflow State', 'Workflow Action'
]

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "dhupar_group.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "dhupar_group.install.before_install"
# after_install = "dhupar_group.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dhupar_group.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	# "*": {
# 	# 	"on_update": "method",
# 	# 	"on_cancel": "method",
# 	# 	"on_trash": "method"
# 	# }

# 	"Sales Order": {
# 		"validate": "dhupar_group.custom.sales_order.sales_order.validate",
# 		"on_submit": "dhupar_group.custom.sales_order.sales_order.on_submit",
# 		"on_update_after_submit":"dhupar_group.custom.sales_order.sales_order.on_update_after_submit",
# 		"on_change": "dhupar_group.custom.sales_order.sales_order.on_change"
# 	},
# 	"Delivery Note": {
# 		"validate": "dhupar_group.custom.delivery_note.delivery_note.validate",
# 		"on_submit": "dhupar_group.custom.delivery_note.delivery_note.on_submit",
# 		"on_cancel": "dhupar_group.custom.delivery_note.delivery_note.on_cancel",
# 		"on_update_after_submit": "dhupar_group.custom.delivery_note.delivery_note.on_update_after_submit"
# 	},
# 	"Stock Entry":{
# 		"on_cancel": "dhupar_group.custom.stock_entry.stock_entry.on_cancel",
# 		"validate": "dhupar_group.custom.stock_entry.stock_entry.validate",
# 		"on_submit": "dhupar_group.custom.stock_entry.stock_entry.on_submit",
# 		"on_update_after_submit": "dhupar_group.custom.stock_entry.stock_entry.on_update_after_submit"
# 	}
# }
doc_events = {
	# "Stock Entry": {
	# 	"get_rack_number": "dhupar_group.custom_actions.get_rack_number",
	# }
	# "Purchase Receipt":{
	# 	"on_submit":"dhupar_group.dhupar_group.doctype.reservation_schedule.reservation_schedule.reservation_shedular"
	# }

}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"cron": {
#         "*/30 * * * *": [
#             "dhupar_group.dhupar_group.doctype.reservation_schedule.reservation_schedule.reservation_shedular"
#         ],
#         "0 0 * * *":[
#         	"dhupar_group.dhupar_group.doctype.reservation_schedule.reservation_schedule.reverse_expired_se_qty"
#         ],
#         "*/20 * * * *":[
#         	"dhupar_group.dhupar_group.doctype.reservation_schedule.reservation_schedule.get_closed_reservation",
#         ],
#         "40 * * * *":[
#         	"dhupar_group.dhupar_group.doctype.reservation_schedule.reservation_schedule.cancelled_dn_details",
#         ],
#         "50 * * * *":[
#         	"dhupar_group.dhupar_group.doctype.reservation_schedule.reservation_schedule.cancelled_ese_details"
#         ]
#     }
   "daily": [
		"dhupar_group.custom_schedules.update_dso"
	],

#	"hourly": [       ATBBUUvhL8YG7mZxf4zuvzXNMyK3A90BB448
# #  		"dhupar_group.custom_schedues.update_dso",
# # 		"dhupar_group.dhupar_group.doctype.reservation_schedule.reservation_schedule.get_closed_reservation",
# # 		"dhupar_group.dhupar_group.doctype.reservation_schedule.reservation_schedule.cancelled_ese_details"
#	]
}

# }
# Testing
# -------

# before_tests = "dhupar_group.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dhupar_group.event.get_events"
# }

