function consoleerp_hi(data) {
	var d = new frappe.ui.Dialog({
		'fields': [
			{'fieldname': 'ht', 'fieldtype': 'HTML'},
			{'fieldname': 'today', 'fieldtype': 'Date', 'default': frappe.datetime.nowdate()}
    		],
    		primary_action: function(){
        		d.hide();
    		}
	});

	d.fields_dict.ht.$wrapper.html('Please Select the Items to Reserve');
	d.show();
}
