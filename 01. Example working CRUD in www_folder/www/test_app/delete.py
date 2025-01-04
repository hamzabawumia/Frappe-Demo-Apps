import frappe


@frappe.whitelist(allow_guest=True)  # Allow access from the frontend
def get_context():
    # Get the form data, including the CSRF token
    csrf_token = frappe.form_dict.get('csrf_token')

    # Get the specified object and delete it
    todo = frappe.get_doc("todoz", frappe.form_dict.get("name")) # retrieve the specified record 
    todo.delete()

    return {"message": "Todo deleted successfully"}