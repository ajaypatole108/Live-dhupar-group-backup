import frappe
from erpnext.selling.doctype.customer.customer import Customer, get_customer_outstanding
from frappe import _

class CustomCustomer(Customer):

    def validate_credit_limit_on_change(self):
        # print("is is where we are")
        if self.get("__islocal") or not self.credit_limits:
            return

        past_credit_limits = [d.credit_limit
            for d in frappe.db.get_all("Customer Credit Limit", filters={'parent': self.name}, fields=["credit_limit"], order_by="company")]

        current_credit_limits = [d.credit_limit for d in sorted(self.credit_limits, key=lambda k: k.company)]

        if past_credit_limits == current_credit_limits:
            return

        company_record = []
        for limit in self.credit_limits:
            if limit.company in company_record:
                frappe.throw(_("Credit limit is already defined for the Company {0}").format(limit.company, self.name))
            else:
                company_record.append(limit.company)

            outstanding_amt = get_customer_outstanding(self.name, limit.company)
            # if flt(limit.credit_limit) < outstanding_amt:
            #   frappe.throw(_("""New credit limit is less than current outstanding amount for the customer. Credit limit has to be atleast {0}""").format(outstanding_amt))







