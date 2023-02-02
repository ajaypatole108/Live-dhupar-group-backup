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
from erpnext.stock.stock_balance import update_bin_qty, get_reserved_qty
from frappe.desk.notifications import clear_doctype_notifications
from frappe.contacts.doctype.address.address import get_company_address
from erpnext.selling.doctype.customer.customer import check_credit_limit
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.accounts.utils import get_fiscal_year, get_balance_on
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.accounts.report.accounts_receivable_summary.accounts_receivable_summary import execute as get_ageing
from calendar import monthrange
import requests
import logging

@frappe.whitelist()
def make_pick_list(source_name, target_doc=None):
	def post_process(source, doc):
		doc.purpose = "Pick List"		

	def update_item(source, target, source_parent):
		target.project = source_parent.project
		target.qty = flt(source.qty) - flt(source.delivered_qty)

	doc = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Stock Entry",
			"validation": {
				"docstatus": ["=", 1]
			},
            "field_map": {
                "sales_order_no": "sales_order"
            }
            },

		"Sales Order Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"name": "sales_order_item",
				"parent": "sales_order",
				"stock_uom": "uom",
				"stock_qty": "qty"
			},
			"postprocess": update_item,
			"condition": lambda doc: abs(doc.delivered_qty) < abs(doc.qty) and doc.delivered_by_supplier!=1
		}
	}, target_doc, post_process)

	return doc

@frappe.whitelist()
def make_put_list(source_name, target_doc=None):
	def post_process(source, doc):
		doc.purpose = "Put List"

	def update_item(source, target, source_parent):
		target.project = source_parent.project

	doc = get_mapped_doc("Purchase Receipt", source_name, {
		"Purchase Receipt": {
			"doctype": "Stock Entry",
			"validation": {
				"docstatus": ["=", 1]
			},
            "field_map": {
                "purchase_receipt_no": "purchase_receipt"
            }
            },

		"Purchase Receipt Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"name": "purchase_receipt_item",
				"stock_uom": "uom",
				"stock_qty": "qty"
			},
		}
	}, target_doc, post_process)

	return doc

@frappe.whitelist()
def get_dashboard_info(party_type, party, loyalty_program=None):
	current_fiscal_year = get_fiscal_year(nowdate(), as_dict=True)

	doctype = "Sales Invoice"

	companies = frappe.get_all(doctype, filters={
		'docstatus': 1,
		party_type.lower(): party
	}, distinct=1, fields=['company'])

	company_wise_info = []

	company_wise_grand_total = frappe.get_all(doctype,
		filters={
			'docstatus': 1,
			party_type.lower(): party,
			'posting_date': ('between', [current_fiscal_year.year_start_date, current_fiscal_year.year_end_date])
			},
			group_by="company",
			fields=["company", "sum(grand_total) as grand_total", "sum(base_grand_total) as base_grand_total"]
		)

	company_wise_grand_total_last_year = frappe.get_all(doctype,
		filters={
			'docstatus': 1,
			party_type.lower(): party,
			'posting_date': ('between', [frappe.utils.add_days(current_fiscal_year.year_start_date,-365), frappe.utils.add_days(current_fiscal_year.year_end_date,-365)])
			},
			group_by="company",
			fields=["company", "sum(grand_total) as grand_total", "sum(base_grand_total) as base_grand_total"]
		)

	company_wise_billing_this_year = frappe._dict()
	company_wise_billing_last_year = frappe._dict()
	for d in company_wise_grand_total:
		company_wise_billing_this_year.setdefault(
			d.company,{
				"grand_total": d.grand_total,
				"base_grand_total": d.base_grand_total
			})
			
	for d in company_wise_grand_total_last_year:
		company_wise_billing_last_year.setdefault(
			d.company,{
				"grand_total": d.grand_total,
				"base_grand_total": d.base_grand_total
			})

	for d in companies:

		billing_this_year = flt(company_wise_billing_this_year.get(d.company,{}).get("grand_total"))
		billing_last_year = flt(company_wise_billing_last_year.get(d.company,{}).get("grand_total"))

		info = {}
		info["billing_this_year"] = flt(billing_this_year) if billing_this_year else 0
		info["billing_last_year"] = flt(billing_last_year) if billing_last_year else 0
		info["company"] = d.company

		company_wise_info.append(info)

	return company_wise_info

@frappe.whitelist()
def get_ageing_data(customer,company="Dhupar Brothers Trading Pvt. Ltd."):
	
	ageing_filters = frappe._dict({
		'company': company,
		'report_date': nowdate(),
		'ageing_based_on': "Posting Date",
		'range1': 30,
		'range2': 60,
		'range3': 90,
		'range4': 120,
		'customer': customer
	})
	col1, ageing = get_ageing(ageing_filters)

	return ageing

@frappe.whitelist()
def get_debtor_days(customer):

	outstanding = get_balance_on(date = nowdate(), party_type = 'Customer', party = customer)

	data = frappe.db.sql(
				"""
				SELECT posting_date as "month", rounded_total as "total"
				FROM `tabSales Invoice`
				WHERE customer = %s AND docstatus = 1
				ORDER BY posting_date DESC
			""",
				customer,
				as_dict=1,
			)
	
	dso = 0

	for i in data:
		
		obj_date = i["month"]
#		print("before: " + str(outstanding))
		outstanding = outstanding - i['total']
#		print("after:" + str(outstanding))
		
		if outstanding <= 0:
			return round((datetime.now().date()-obj_date).days,0)
			# 	dso = (datetime.now() - obj_date).days
			
			# else:
				
			# 	dso = dso + (1 if outstanding > i['total'] else outstanding/i['total']) * monthrange(i["year"], i["month"])[1]
			# 	outstanding = outstanding - i['total']
	
	return 9999

@frappe.whitelist()
def get_data_for_dashboard():
	pass

# aj - call from - remainders.remainders.public.js.dispatch_order(js).dispatch(function)
@frappe.whitelist()
def send_to_trello(link='',name='',customer='',date='',po_no='',contact_person='',transport_payment='',delivery_type='',customer_vehicle='',special_instructions=''):
	
	url = "https://n8n.dhupargroup.com/webhook/865fd238-9558-48f8-a0c6-079a33f6d8a3"
	
	data = {
		"link": link,
		"name": name,
		"customer": customer,
		"date": date,
		"po_no": po_no,
		"contact_person": contact_person,
		"transport_payment": transport_payment,
		"delivery_type": delivery_type,
		"customer_vehicle": customer_vehicle,
		"special_instructions": special_instructions
	}

	headers = {
		'content-type': "application/json",
		'cache-control': "no-cache"
		}

	response = requests.post(url, data=json.dumps(data), headers=headers)

# call from n8n http request (name: customer sync to kylas)
@frappe.whitelist()
def retrive_customer_data():
	cust_data = frappe.db.sql("""
								SELECT name,tax_id FROM `tabCustomer`
							""",as_dict=1)
	# d = json.dumps(cust_data)
	return cust_data


# (client_script - sales_invoice) call this function (event --> onload) --> script_line_no - 1-12
@frappe.whitelist()
def check_tcs(party_type, party, loyalty_program=None):
	cust = frappe.get_doc('Customer',party)
	# logging.basicConfig(filename='log_aj.txt',level=logging.DEBUG,filemode='w')
	# logging.debug(cust)
	return cust.tcs_disable


# def moving_average(items):
# 	moving_average_list = []
#     # for item in items:
# 	stock_values = frappe.db.sql(f"""SELECT actual_qty,voucher_no,stock_value_difference FROM `tabStock Ledger Entry`
# 									WHERE 
# 									item_code = '{items}'
# 									ORDER BY posting_date ASC limit 100""",as_dict=1)[3:]
# 	print(stock_values)

# 	total_amt = 39508
# 	q = 35

# 	for i in stock_values:
# 		total_amt = total_amt + i.stock_value_difference
# 		q = q + i.actual_qty

# 	print('total_amt: ',total_amt)
# 	print('q: ',q)
# 	moving_average = total_amt / q
# 	moving_average_list.append((items, moving_average))
# 	return moving_average_list



def extract_data():
	inv = []
	cust = ['ACCUSONIC CONTROLS PVT. LTD. (S)',
			'ACME ENGINEERING SOLUTIONS',
			'ANANTKRUPA ELECTRICALS',
			'ANJ TURNKEY PROJECTS PVT. LTD.',
			'APTECH CONTROL SYSTEMS',
			'Aptech control systems - 1',
			'ASHDAN DEVELOPERS PRIVATE LIMITED',
			'Aurionpro Solutions Ltd',
			'Bharati Vidypeeth',
			'Burckhardt Compression (India) Pvt. Ltd.',
			'Cash Sale',
			'CASH SALE MUMBAI',
			'CLASSIC ELECTRIC',
			'Cotmac Electronics Pvt.Ltd.',
			'ELECTRONICA AUTOMATIONS PVT.LTD.',
			'Electronica India Limited (GEN Division)',
			'EMTEC SOLUTIONS',
			'Enrich Energy Pvt. Ltd.',
			'EVIO PRIVATE LIMITED',
			'Gera Developments Pvt. Ltd.',
			'Giriraj Enterprises ( Baner )',
			'GLATT SYSTEMS PVT.LTD.',
			'GODREJ AND BOYCE MANUFACTURING CO LTD',
			'GODREJ SKYLINE DEVELOPERS PRIVATE LIMITED',
			'Greaves Cotton Ltd.',
			'H.T.SWITCHGEARS',
			'IKE ELECTRIC PVT.LTD.',
			'INVRECO PRIVATE LIMITED',
			'ITD CEMENTATION INDIA LIMITED',
			'JSW Steel Coated Products Ltd.',
			'KEAN CONSTRUCTION LLP',
			'KULASWAMINEE ENGINEERS',
			'Larsen & Toubro Limited',
			'MIRHAE ENGINEERING INDIA PRIVATE LIMITED',
			'Nalanda Shelter Pvt Ltd',
			'Neeraj Projects Pvt Ltd',
			'Neilsoft Pvt Limited',
			'Nichrome India Ltd.',
			'NNP BUILDCON LLP',
			'NNP BUILDCON PRIVATE LIMITED',
			'Nyati engineers and consultant Pvt Ltd.',
			'Omkar Electric Works',
			'ORBITTAL ELECTROMECH ENGI.PROJ.PVT.LTD',
			'PANCHASHIL COPORATE PARK PVT.LTD.',
			'PANCHASHIL INFRASTURE HOLDINGS PVT. LTD.',
			'PANCHASHIL TECH PARK PVT.LTD.',
			'Panchshil Corporate Park',
			'Panchshil Corporate Park Pvt Ltd',
			'PANCHSHIL HOTELS PVT LTD',
			'Panchshil Realty And Developers Pvt. Ltd.',
			'PANCHSHIL TECH PARK PVT LTD. (yerwada)',
			'PRASA INFOCOM AND POWER SOLUTIONS PRIVATE LIMITED',
			'Quadrogen India Private Limited',
			'RAGHAVENDRA ELECTRICAL ENGINEERS',
			'Ratilal Bhagwandas Contruction Company',
			'ROHAN & ATUL ENTRPRISES',
			'ROHAN BUILDERS & DEVELOPERS PVT LTD.',
			'ROHAN HOUSING PVT LTD.',
			'ROHAN PROMOTORS & DEVELOPERS',
			'S.R. ELECTRICALS ENTERPRISES',
			'S.S.Engineers',
			'Saakshi Machine & Tools Pvt. Ltd.',
			'SAMCON INDUSTRIAL CONTROLS PRIVATE LIMITED',
			'Scon Projects Private Limited',
			'SEDEMAC MECHATRONICS PVT.LTD.',
			'SHAPOORJI PALLONJI & CO. PVT. LTD.',
			'Shree Flameproof Industries Pvt Ltd.',
			'ŠKODA AUTO Volkswagen India Private Limited',
			'Sparkline Equipment Pvt. Ltd.',
			'STERLING AND WILSON PVT. LTD.',
			'SUCG INFRASTRUCTURE INDIA PRIVATE LIMITED',
			'SUVARNA ELECTRICALS PVT. LTD.',
			'Tata Motors Ltd (Car Plant)',
			'Tata Motors Ltd (Pimpri)',
			'TATA PROJECTS LIMITED',
			'TECH INDIA ELECTROSOLUTIONS PRIVATE LIMITED',
			'Tech India Engineers Pvt. Ltd.',
			'Thyssenkrupp Industries India Private.Ltd.',
			'TOLBURN MANAGMENT SERVICES PRIVATE LIMITED',
			'Turnkey Electrical Engineers Pvt. Ltd.',
			'Ujjwal Pune Ltd',
			'UNIQUE ENGINEERS PVT LTD',
			'UNIVERSAL MEP PROJECTS & ENGINEERING SERVICES LIMITED',
			'Vascon Engineers Ltd',
			'VENKATESHWARA HATCHERIES PVT LTD  - 1',
			'VIDYUT CONTROL & AUTOMATION PVT.LTD',
			'VIRAJ PROFILES LIMITED',
			'Vivid Electromech Pvt.Ltd.',
			'VTP CORPORATION LLP',
			'VTP URBAN PROJECT PUNE LLP',
			'Wilo Mather & Platt Pumps Pvt.Ltd.',
			'Yeternity Systems.']

	for i in cust:
		print()
		print(f'''---------------------------------{i}---------------------------------------------''')
		print()
		d = frappe.db.sql(f"""
							select NAME,CREATION,CUSTOMER_NAME,signed_einvoice 
							from `tabSales Invoice` 
							where customer_name = '{i}'
							and docstatus = '1'
							and name like '%DINV%' 
							""",as_dict=1)
		for j in d:
			# print(j)
			if j.signed_einvoice == None:
				continue
			else:
				n = j.NAME
				d2 = j.signed_einvoice
				d3 = json.loads(d2)
				d4 = d3['ValDtls']['OthChrg']
				if d4 != 0.0:
					inv.append(n)
		print(inv)
		inv = []