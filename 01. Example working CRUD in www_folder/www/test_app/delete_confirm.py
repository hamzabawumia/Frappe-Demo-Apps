import frappe

from frappe.exceptions import DoesNotExistError

def get_context(context):
    try:
        todo = frappe.get_doc('todoz', frappe.form_dict.get("name"))
        context.todo = todo
    except DoesNotExistError:
        context.todo = None
