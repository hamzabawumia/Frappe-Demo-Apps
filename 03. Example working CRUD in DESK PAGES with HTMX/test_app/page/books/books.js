frappe.pages['books'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'None',
		single_column: true
	});


    $(wrapper).html(`

        <div id="message"></div>

        <div>
            <button hx-get="/api/method/test_app.api.books.new_book_form" hx-target="#book-form">
                New Book
            </button>
        </div>

        <div id="book-form"></div>
        <div id="book-detail"></div>

        <div id="book-list" hx-get="/api/method/test_app.api.books.list_books" 
                hx-trigger="load">
        </div>

        <script src="https://unpkg.com/htmx.org@1.9.2"></script>

        
    `);


}