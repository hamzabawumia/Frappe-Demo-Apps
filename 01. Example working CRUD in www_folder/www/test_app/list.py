import frappe
from frappe.model.document import Document

def get_context(context):
    todos = frappe.get_all('todoz',
            fields=["name", "title", "description", "status"])
    context.todos = todos



@frappe.whitelist(allow_guest=True)
def todo_list():
    todos = frappe.get_all("todoz", 
        fields=["name", "title", "description", "status"]
        )
    return frappe.render_template("test_app/www/list.html", {"todos": todos})