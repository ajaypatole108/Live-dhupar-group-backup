import frappe
import json

@frappe.whitelist()
def get_item_stock(customer, items, items_array, invoice):
    print("items: \n",items)
    print("items_array: ",items_array)

    items1 = json.loads(items)
    items = [str(i['item_code']) for i in items1 if i['name'] in items_array]
    idx1 = [str(i['idx']) for i in items1 if i['name'] in items_array]
    qty1 = [str(i['qty']) for i in items1 if i['name'] in items_array]

    cnt = 0
    result=[]
    for item_code in items:
        idx = idx1[cnt]
        qty = qty1[cnt]
        data = frappe.db.sql(f"""
                                select tabBin.item_code,
                                tabItem.item_name as description,
                                tabItem.item_group as item_Group,
                                tabItem.brand as brand,
                                ((select SUM(tabBin.actual_qty)
                                from tabBin
                                WHERE
                                tabBin.actual_qty <> 0 and tabBin.warehouse not LIKE "Rejection%%" and tabBin.warehouse not LIKE "Wagholi Faulty  - DBTPL%%" and tabBin.warehouse not LIKE "Shed Wagholi Faulty - DBTPL%%"  and tabBin.warehouse not LIKE "Tata Ujjwal Warehouse - DBTPL%%" and tabBin.warehouse not LIKE "P%%" and tabBin.warehouse not LIKE "Aut%%" and tabBin.warehouse not LIKE "WC - DBTPL%%" and tabBin.warehouse not LIKE "M%%" and tabBin.warehouse not LIKE "Wagholi Excess Material - DBTPL%%" and tabBin.warehouse not LIKE "Wagholi Shortage - DBTPL%%" and tabBin.item_code = tabItem.item_code) - (SELECT CASE WHEN SUM(rsi.reserve_qty) IS NULL THEN 0 WHEN SUM(rsi.reserve_qty) < 0 THEN 0 ELSE SUM(rsi.reserve_qty) END  FROM `tabReservation Schedule Item` as rsi join `tabReservation Schedule` as rs on rsi.parent = rs.name WHERE rsi.item_code = tabItem.item_code and rs.parent_warehouse = "WAGHOLI BIN RACK - DBTPL" AND rs.status = 'Open')) as Wagholi,
                                ((select SUM(tabBin.actual_qty)
                                from tabBin
                                WHERE
                                tabBin.actual_qty <> 0 and tabBin.warehouse="Pune - DBTPL" and tabBin.item_code = tabItem.item_code) - (SELECT CASE WHEN SUM(rsi.reserve_qty) IS NULL THEN 0 WHEN SUM(rsi.reserve_qty) < 0 THEN 0 ELSE SUM(rsi.reserve_qty) END FROM `tabReservation Schedule Item` as rsi join `tabReservation Schedule` as rs on rsi.parent = rs.name WHERE rsi.item_code = tabItem.item_code and rs.parent_warehouse = "All Warehouses - DBTPL" AND rs.status = 'Open')) as Pune,
                                ((select SUM(tabBin.actual_qty)
                                from tabBin
                                WHERE
                                tabBin.actual_qty <> 0 and tabBin.warehouse in (select name from tabWarehouse WHERE tabWarehouse.parent_warehouse = "PIMPRI BIN RACK - DBTPL") and tabBin.item_code = tabItem.item_code) - (SELECT CASE WHEN SUM(rsi.reserve_qty) IS NULL THEN 0 WHEN SUM(rsi.reserve_qty) < 0 THEN 0 ELSE SUM(rsi.reserve_qty) END FROM `tabReservation Schedule Item` as rsi join `tabReservation Schedule` as rs on rsi.parent = rs.name WHERE rsi.item_code = tabItem.item_code and rs.parent_warehouse = "PIMPRI BIN RACK - DBTPL" AND rs.status = 'Open')) as Pimpri,
                                ((select SUM(tabBin.actual_qty) 
                                from tabBin
                                WHERE
                                tabBin.actual_qty <> 0 and tabBin.warehouse in (select name from tabWarehouse WHERE tabWarehouse.parent_warehouse = "MAHAPE BIN RACK - DBTPL") and tabBin.item_code = tabItem.item_code) - (SELECT CASE WHEN SUM(rsi.reserve_qty) IS NULL THEN 0 WHEN SUM(rsi.reserve_qty) < 0 THEN 0 ELSE SUM(rsi.reserve_qty) END FROM `tabReservation Schedule Item` as rsi join `tabReservation Schedule` as rs on rsi.parent = rs.name WHERE rsi.item_code = tabItem.item_code and rs.parent_warehouse = "MAHAPE BIN RACK - DBTPL" AND rs.status = 'Open')) as Mahape
                                FROM tabBin
                                left join tabItem on tabBin.item_code = tabItem.item_code
                                WHERE 
                                tabBin.actual_qty > 0
                                AND
                                tabBin.item_code = '{item_code}'
                                group by tabBin.item_code
                            """,as_dict=1)
        if len(data) != 0:
            for i in data:
                i['idx'] = idx
                i['qty'] = qty

                if i.description == None:
                    i.description = ''
                if i.item_Group == None:
                    i.item_Group = ''
                if i.brand == None:
                    i.brand = ''
                if i.Wagholi == None:
                    i.Wagholi = ''
                if i.Pune == None:
                    i.Pune = ''
                if i.Pimpri == None:
                    i.Pimpri = ''
                if i.Mahape == None:
                    i.Mahape = ''
            i1 = (i.idx,i.item_code,i.description,i.item_Group,i.brand,i.qty,i.Wagholi,i.Pune,i.Pimpri,i.Mahape)
            result.append(i1)
        else:
           d1 = frappe.db.sql(f"""
                            SELECT item_code,description,item_Group,brand 
                            FROM `tabItem`
                            WHERE
                            item_code = '{item_code}'
                        """,as_dict=1)
           if len(d1)!= 0:
                for i in d1:
                    i['idx'] = idx
                    i['qty'] = qty

                    if i.description == None:
                        i.description = ''
                    if i.item_Group == None:
                        i.item_Group = ''
                    if i.brand == None:
                        i.brand = ''

                    i['Wagholi'] = ''
                    i['Pune'] = ''
                    i['Pimpri'] = ''
                    i['Mahape'] = ''
                i1 = (i.idx,i.item_code,i.description,i.item_Group,i.brand,i.qty,i.Wagholi,i.Pune,i.Pimpri,i.Mahape)
                result.append(i1)
        cnt +=1
    return [(result)]