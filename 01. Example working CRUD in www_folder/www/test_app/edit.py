import frappe



@frappe.whitelist(allow_guest=True)  # Allow access from the frontend
def get_context():
    # Get the form data, including the CSRF token
    csrf_token = frappe.form_dict.get('csrf_token')

    title = frappe.form_dict.get("title")
    description = frappe.form_dict.get("description")

    # Your update logic here
    todo = frappe.get_doc("todoz", frappe.form_dict.get("name")) # retrieve the specified record 
    todo.title = title
    todo.description = description
    todo.save()

    return {"message": "Todo updated successfully"}




# @frappe.whitelist(allow_guest=True)
# def update(name):
#     # Access form data from frappe.local.form_dict
#     name_input = frappe.local.form_dict.get("name")
#     description_input = frappe.local.form_dict.get("description")

#     try:
#         # Fetch the existing record
#         record = frappe.get_doc('todoz', name)

#         # Update the fields
#         record.title = name_input
#         record.description = description_input

#         # Save the updated record
#         record.save()

#         # Commit changes to the database
#         frappe.db.commit()

#         # Return a success message
#         return frappe.render_template('edit.html', {
#             'message': 'Record updated successfully!',
#             'record': record
#         })

#     except Exception as e:
#         # Handle errors and return the error message
#         return frappe.render_template('edit.html', {
#             'message': f'Error: {str(e)}',
#             'record': frappe.get_doc('todoz', name)
#         })
