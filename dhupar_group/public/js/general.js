
// close button on order reports
// console.log("hi");

frappe.provide("erpnext");

$.extend(erpnext, {
    consoleerp_hi: function (data) {
        frappe.call({
            method: "erpnext.selling.doctype.sales_order.sales_order.update_status",
            args: {
                status: "Closed",
                name: data
            },
            callback: function (r) {
                frappe.msgprint("closed " + data);
            }
        });
    }
});

// console.log(consoleerp_hi);

function branch(data){
    frappe.db.set_value('Sales Order', data, {
        'branch': 'Project'
    })
}

frappe.ui.form.on("Quotation", "get_history", function (frm) {

    var item_list = cur_frm.get_selected();
    if (item_list.items) {

        frappe.call({
            method: "dhupar_group.dhupar_group.get_history.get_item_history",
            args: {
                'customer': cur_frm.doc.customer_name,
                'items': cur_frm.doc.items,
                'items_array': item_list.items,
                'invoice': cur_frm.doc.name
            },
            callback: function (r) {

                console.log(r);
                if (r.message[0].length > 0) {
                    frappe.msgprint(`
                    <div style="height: 400px; overflow-y: auto; margin-bottom: 10px;" class="table-wrapper-scroll-y">
                        <table class="table table-bordered table-striped table-sm">
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Item Code</th>
                                    <th>Description</th>
                                    <th>Pricelist Rate</th>
                                    <th>QTY.</th>
                                    <th>discount</th>
                                </tr>
                            </thead>
                            <tbody id="history-table">
                                
                            </tbody
                        </table>
                    </div>`);

                    frappe.msgprint(`
                    <div style="height: 400px; overflow-y: auto; margin-bottom: 10px;" class="table-wrapper-scroll-y">
                        <table class="table table-bordered table-striped table-sm">
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Item Code</th>
                                    <th>Description</th>
                                    <th>Pricelist Rate</th>
                                    <th>QTY.</th>
                                    <th>discount</th>
                                </tr>
                            </thead>
                            <tbody id="history-table">
                                
                            </tbody
                        </table>
                    </div>`);

                    var table = document.getElementById("history-table");

                    //console.log(table);

                    for (var j = 0; j < r.message.length; j++) {
                        //console.log(r.message[0].length);
                        for (var i = 0; i < r.message[j].length; i++) {
                            //console.log(document.getElementById("history-table"));
                            var newRow = table.insertRow(table.rows.length);
                            //console.log(r.message[0].length);
                            newRow.innerHTML = "<td>" + moment(r.message[j][i][0]).format('MM/DD/YYYY') + "</td>" +
                                "<td>" + r.message[j][i][1] + "</td>" +
                                "<td>" + r.message[j][i][2] + "</td>" +
                                "<td>" + r.message[j][i][4] + "</td>" +
                                "<td>" + r.message[j][i][3] + "</td>" +
                                "<td>" + r.message[j][i][5] + "</td>"
                        }
                    }
                } else {
                    frappe.msgprint("Never Sold to " + cur_frm.doc.customer_name)
                }
            }
        });

    }

});



