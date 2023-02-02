from __future__ import unicode_literals
import frappe, json, copy
from frappe import _
from frappe.utils import flt, formatdate
from datetime import date
from six import iteritems

def execute(filters=None):
	return Gstr1Report(filters).run()

class Gstr1Report(object):
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})
		self.columns = []
		self.data = []

	def run(self):

		self.get_columns()
		hsn_list = list(frappe.db.sql('''
		select `tabSales Invoice Item`.gst_hsn_code, sum(`tabSales Invoice Item`.qty), sum(`tabSales Invoice Item`.net_amount),
		`tabSales Invoice Item`.item_tax_rate, `tabSales Taxes and Charges`.account_head, `tabSales Taxes and Charges`.rate
		FROM `tabSales Invoice Item`, `tabSales Taxes and Charges`
		where `tabSales Invoice Item`.docstatus = 1 and `tabSales Taxes and Charges`.parent = `tabSales Invoice Item`.parent
		AND (SELECT posting_date from `tabSales Invoice` where name = `tabSales Invoice Item`.parent) BETWEEN "{0}" and "{1}"
		GROUP by gst_hsn_code, account_head, item_tax_rate
		ORDER by gst_hsn_code, item_tax_rate
		'''.format(self.filters.get('from_date'), self.filters.get('to_date'))))
		row = []
		prev_item = {
			'HSN': 			"",
			'description': 	"",
			'UOM': 			"NOS-NUMBERS",
			'quantity': 	0,
			'after_tax': 	0,
			'before_tax': 	0,
			'SGST':        	0,
			'CGST':        	0,
			'IGST': 		0,
			'cess': 		0,
		}
		for i in hsn_list:
			i = list(i)
			taxes = json.loads(i[3])
			i[2] = round(i[2], 2)
			if 'SGST - DBTPL' in taxes:
				item = {
				'HSN': 			i[0],
				'description': 	"",
				'UOM': 			"NOS-NUMBERS",
				'quantity': 	i[1],
				'after_tax': 	0,
				'before_tax': 	i[2],
				'SGST':        	round(i[2] * taxes['SGST - DBTPL'] / 100,4) if 'SGST' in i[4]  else 0,
				'CGST':        	round(i[2] * taxes['CGST - DBTPL'] / 100,4) if 'CGST' in i[4]  else 0,
				'IGST': 		round(i[2] * taxes['IGST - DBTPL'] / 100,4) if 'IGST' in i[4]  else 0,
				'cess': 		0,
				}
			else:
				item = {
				'HSN': 			i[0],
				'description': 	"",
				'UOM': 			"NOS-NUMBERS",
				'quantity': 	i[1],
				'after_tax': 	0,
				'before_tax': 	i[2],
				'SGST':        	0,
				'CGST':        	0,
				'IGST': 		0,
				'cess': 		0,
				}
			
			added = False
			for j in row:
				if j['HSN'] == item['HSN']:

					if not (prev_item['quantity'] == item['quantity'] and prev_item['before_tax'] == item['before_tax'] and prev_item['HSN'] == item['HSN']):
						j['quantity'] = j['quantity'] + item['quantity']
						j['after_tax'] = j['after_tax'] + item['after_tax']
						j['before_tax'] = j['before_tax'] + item['before_tax']
					j['SGST'] = j['SGST'] + item['SGST']
					j['CGST'] = j['CGST'] + item['CGST']
					j['IGST'] = j['IGST'] + item['IGST']
					added = True
					break
			prev_item = copy.copy(item)
			if not added:
				row.append(item)
		#print len(row)
		quantity =0
		after_tax =0
		before_tax =0
		sgst =0
		cgst =0
		igst =0 
		
		for i in row:
			self.data.append([i['HSN'], i['description'], i['UOM'], i['quantity'], i['before_tax'] + i['SGST'] + i['CGST'] + i['IGST'], i['before_tax'], i['SGST'], i['CGST'], i['IGST']])
		for i in self.data:
			quantity += i[3]
			after_tax += i[4]
			before_tax += i[5]
			sgst += i[6]
			cgst += i[7]
			igst += i[8] 
		self.data.append(["","","Totals",quantity,after_tax,before_tax,sgst,cgst,igst])

		return self.columns, self.data

	def get_columns(self):

		self.invoice_columns = [
			{
				"fieldname": "hsn_code",
				"label": "HSN Code",
				"fieldtype": "Int",
				"width":120
			},
			{
				"fieldname": "description",
				"label": "Description",
				"fieldtype": "Data",
				"options": "Sales Invoice",
				"width":120
			},
			{
				"fieldname": "uqc",
				"label": "UQC",
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "total_quantity",
				"label": "Total Quantity",
				"fieldtype": "Int",
				"width": 120
			},
			{
				"fieldname": "total_amount",
				"label": "Total Amount",
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"fieldname": "total_taxable_value",
				"label": "Total Taxable Value",
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"fieldname": "state_tax_amount",
				"label": "State Tax Amount",
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"fieldname": "central_tax_amount",
				"label": "Central Tax Amount",
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"fieldname": "integrated_tax_amount",
				"label": "Integrated Tax Amount",
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"fieldname": "cess_amount",
				"label": "Cess Amount",
				"fieldtype": "Currency",
				"width": 120
			}
		]
		
		self.columns = self.invoice_columns

