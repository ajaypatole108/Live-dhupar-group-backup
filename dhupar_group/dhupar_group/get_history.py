import frappe
import json


@frappe.whitelist()
def get_item_history(customer, items, items_array, invoice):

    items = json.loads(items)
    items = [str(i['item_code']) for i in items if i['name'] in items_array]

    invoices =  frappe.db.sql("select name from `tabSales Invoice` where customer_name = '%s'" % str(customer))
    k = [ str(i[0]) for i in invoices]
    if invoice in k :
        k.remove(invoice)

    format_invoices = ','.join(['\'%s\''] * len(k))
    result = []

    for item in items:
        result1 = frappe.db.sql("""select creation, item_code, item_name, qty, price_list_rate, discount_percentage 
                                    from `tabSales Invoice Item` 
                                    where parent in ({invoices}) and item_code = ('{items}')
                                    limit 5 ;""".format(invoices = format_invoices % tuple(k), items = item))
        
        result.append(result1)
    
    return result
    