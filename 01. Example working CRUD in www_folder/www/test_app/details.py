import frappe
from frappe.model.document import Document


def get_context(context):
    name = frappe.form_dict.get('name')

    object_1 = frappe.get_doc("Referral", "Esther Smith-2025-04-12 20:06:02.271682")
    
    template = "repherod/www/doctor_referral_response/details.html"

    context["object_1"] = object_1
    
    context["template_to_include"] = template

    return context


# YOU CAN EVEN DO A REDIRECT:
# import frappe
# from frappe import _

# def get_context(context):
    # Check some condition to decide whether to redirect
    # name = frappe.form_dict.get('name')
    
    # For example, if 'name' is not provided, redirect to a different page
    # if not name:
        # frappe.local.response["type"] = "redirect"
        # frappe.local.response["location"] = "/some-other-page"
        # return context

    #If 'name' exists, proceed with the normal flow
    # try:
        # object_1 = frappe.get_doc("Referral", "Esther Smith-2025-04-12 20:06:02.271682")
    # except frappe.DoesNotExistError:
        #Handle the case where the referral doesn't exist
        # frappe.local.response["type"] = "redirect"
        # frappe.local.response["location"] = "/error-page"
        # return context

    # If everything is okay, set the context as normal
    # template = "repherod/www/doctor_referral_response/details.html"

    # context["object_1"] = object_1
    # context["template_to_include"] = template

    # return context
