

frappe.ui.form.on("Blanket Order", {

    setup: function(frm) {
        cur_frm.set_query("contact_person", function() {
			return {
				filters: [
					["Dynamic Link", "link_doctype", "=", "Customer"],
			["Dynamic Link", "link_name", "=", cur_frm.doc.customer],
				]
			}
		});

        cur_frm.set_query("customer_address", function() {
			return {
				filters: [
					["Dynamic Link", "link_doctype", "=", "Customer"],
			["Dynamic Link", "link_name", "=", cur_frm.doc.customer],
				]
			}
		});
    },
    onload: function(frm) {

        setTimeout(() => {
            var x = document.getElementsByClassName("grid-row-check pull-left");
            for(var i=0; i<x.length;i++)
            {
                x[i].removeAttribute('disabled');
            }
        },300);
    },
    before_save: function (frm) {
        cur_frm.doc.net_total = 0
        cur_frm.doc.items.forEach(function (item, index) {
            
            if (cur_frm.doc.items[index].discount_percentage == null) {
                cur_frm.doc.items[index].discount_percentage = 0;
                cur_frm.refresh_fields();
            }
            cur_frm.doc.items[index].rate = cur_frm.doc.items[index].price_list_rate*(1-cur_frm.doc.items[index].discount_percentage/100);
            cur_frm.doc.items[index].amount = cur_frm.doc.items[index].rate * cur_frm.doc.items[index].qty
            cur_frm.doc.net_total = cur_frm.doc.net_total + cur_frm.doc.items[index].amount
        });
        cur_frm.refresh_fields();
    }

});

frappe.ui.form.on("Blanket Order Item", {

    onload: function (frm, ctd, ctn) {
        locals[ctd][ctn].discount_percentage = 0;
        cur_frm.refresh_fields();
    },
    
    price_list_rate: function (frm, ctd, ctn) {
        if (locals[ctd][ctn].discount_percentage == null) {
            locals[ctd][ctn].discount_percentage = 0;
            cur_frm.refresh_fields();
        }
        locals[ctd][ctn].rate = locals[ctd][ctn].price_list_rate*(1-locals[ctd][ctn].discount_percentage/100);
        locals[ctd][ctn].amount = locals[ctd][ctn].rate * locals[ctd][ctn].qty
        cur_frm.refresh_fields();
    },
    discount_percentage: function (frm,ctd,ctn) {
        locals[ctd][ctn].rate = locals[ctd][ctn].price_list_rate*(1-locals[ctd][ctn].discount_percentage/100);
        locals[ctd][ctn].amount = locals[ctd][ctn].rate * locals[ctd][ctn].qty
        cur_frm.refresh_fields();
    },
    qty: function (frm,ctd,ctn) {
        if (locals[ctd][ctn].discount_percentage == null) {
            locals[ctd][ctn].discount_percentage = 0;
            cur_frm.refresh_fields();
        }
        locals[ctd][ctn].rate = locals[ctd][ctn].price_list_rate*(1-locals[ctd][ctn].discount_percentage/100);
        locals[ctd][ctn].amount = locals[ctd][ctn].rate * locals[ctd][ctn].qty
        cur_frm.refresh_fields();
    }

});