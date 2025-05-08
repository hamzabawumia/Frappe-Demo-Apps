import frappe
from frappe.model.document import Document
from werkzeug.wrappers import Response
from frappe.sessions import get_csrf_token
import frappe
from frappe.sessions import get_csrf_token

@frappe.whitelist(allow_guest=True)
def list_books():

    books = frappe.get_all("Book", fields=["name", "author"])

    csrf_token = get_csrf_token() if get_csrf_token() else 'no_token_available'

    html = "<ul>"
    for book in books:
        html += f"""
        <li>
            {book.name} by {book.author}
            <button hx-get="/api/method/test_app.api.books.view_book?name={book.name}" 
            hx-target="#book-detail">View</button>

            <button hx-get="/api/method/test_app.api.books.edit_book_form?name={book.name}" 
            hx-target="#book-form">Edit</button>

            <button hx-post="/api/method/test_app.api.books.delete_book" 
            hx-vals='{{"name": "{book.name}", "csrf_token": "{csrf_token}"}}' 
            hx-target="#message" 
            hx-swap="innerHTML">Delete</button>
        </li>
        """
    html += "</ul>"

    return Response(html, content_type='text/html')



@frappe.whitelist(allow_guest=True)
def view_book(name):
    book = frappe.get_doc("Book", name)
    html = f"""
    <div id="book-detail">
        <h3>{book.name}</h3>
        <p>Author: {book.author}</p>
    </div>
    """
    return Response(html, content_type='text/html')
    # This returns the html with the werkzeug.wrappers


@frappe.whitelist(allow_guest=True)
def new_book_form():

    csrf_token = get_csrf_token() # Get it from server session

    html = f"""
    <form hx-post="/api/method/test_app.api.books.create_book" hx-target="#message">

        <input type="hidden" name="csrf_token" value="{csrf_token}">
        
        <label>Name:</label>
        <input type="text" name="name">
        <label>Author:</label>
        <input type="text" name="author">
        <button type="submit">Create</button>
    </form>
    """

    return Response(html, content_type='text/html')
    # This returns the html with the werkzeug.wrappers


@frappe.whitelist(allow_guest=True)
def edit_book_form(name):
    book = frappe.get_doc("Book", name)

    csrf_token = get_csrf_token()

    html = f"""
    <form hx-post="/api/method/test_app.api.books.update_book" hx-target="#message">

    <!-- CSRF Token input field -->
    <input type="hidden" name="csrf_token" value="{csrf_token}">

    <input type="hidden" name="name" value="{book.name}">

        <label>Name:</label>
        <input type="text" name="name" value="{book.name}" readonly>
        <label>Author:</label>
        <input type="text" name="author" value="{book.author}">
        <button type="submit">Update</button>
    </form>
    """
    return Response(html, content_type='text/html')
    # This returns the html with the werkzeug.wrappers


@frappe.whitelist(allow_guest=True)
def create_book():
    # Get the form data, including the CSRF token
    csrf_token = frappe.form_dict.get('csrf_token')

    data = frappe.form_dict
    book = frappe.new_doc("Book")
    book.name = data.get("name")
    book.author = data.get("author")
    book.insert()

    html = f"<div id='message'>Book '{book.name}' created successfully.</div>"
    return Response(html, content_type='text/html')
    # This returns the html with the werkzeug.wrappers


@frappe.whitelist(allow_guest=True)
def update_book():

    # Get the form data, including the CSRF token
    csrf_token = frappe.form_dict.get('csrf_token')

    data = frappe.form_dict
    book = frappe.get_doc("Book", data.get("name"))
    book.author = data.get("author")
    book.save()

    html = f"<div id='message'>Book '{book.name}' updated successfully.</div>"
    return Response(html, content_type='text/html')
    # This returns the html with the werkzeug.wrappers


@frappe.whitelist(allow_guest=True)
def delete_book():
    name = frappe.form_dict.get("name")
    frappe.delete_doc("Book", name)
    html = f"<div id='message'>Book '{name}' deleted.</div>"

    return Response(html, content_type='text/html')
    # This returns the html with the werkzeug.wrappers