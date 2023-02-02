from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Selling"),
			"items": [
				{
					"type": "doctype",
					"name": "Sales Order",
					"description": _("SO."),
				},
				{
					"type": "doctype",
					"name": "Reservation Schedule",
					"description": _("RS."),
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
					"description": _("SE."),
				},
				{
					"type": "doctype",
					"name": "Delivery Note",
					"description": _("DN."),
				},
			]
		},
		{
			"label": _("Configuration"),
			"items": [
				{
					"type": "doctype",
					"name": "Reservation Configurations",
					"description": _("SO."),
				},
				
			]
		},

	]