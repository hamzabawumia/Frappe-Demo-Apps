import frappe


@frappe.whitelist(allow_guest=True)  # Allow access from the frontend
def get_context():
    csrf_token = frappe.form_dict.get('csrf_token')

    title = frappe.form_dict.get("title")
    description = frappe.form_dict.get("description")


    # Create a new Todo document
    todo = frappe.get_doc({
        "doctype": "todoz",  # Specify the Doctype
        "title": title ,
        "description": description
    })
    
    # Insert the new document into the database
    todo.save()


    return {"message": "Todo created successfully"}



