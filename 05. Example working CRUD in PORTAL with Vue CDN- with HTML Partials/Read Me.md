# Example 04: Generic CRUD in a Frappe Portal with Vue CDN

This example shows a reusable CRUD page for a Frappe Portal page using **Vue 3 from a CDN** and the **Composition API**.

It also demonstrates **Frappe/Jinja HTML partials** so the Portal page does not become one very large file.

## Architecture

```text
Frappe/Jinja partials
        │
        ▼
    Portal page
        │
        ▼
      Vue 3
        │
   useCrud(config)
        │
    fetch() + JSON
        │
        ▼
 Generic Frappe API
        │
        ▼
    Any DocType
```

The responsibilities are deliberately separated:

- **HTML partials** — page structure and Vue template markup.
- **`config.js`** — resource-specific configuration.
- **`crud.js`** — reusable Composition API CRUD behavior.
- **`app.js`** — connects the Vue app to the page.
- **`api/crud.py`** — generic Frappe CRUD endpoints.

## Files

```text
04. Example working CRUD in PORTAL with Vue CDN/
│
├── Read Me
├── hooks.py
├── api/
│   └── crud.py
├── templates/
│   └── includes/
│       └── vue_crud/
│           ├── header.html
│           ├── messages.html
│           ├── form.html
│           └── list.html
├── public/
│   └── js/
│       └── vue_crud/
│           ├── config.js
│           ├── crud.js
│           └── app.js
└── www/
    └── crud.html
```

## Why partials?

Instead of putting HTML, configuration, Vue logic, API calls, and CRUD behavior into one `crud.html`, the page includes small server-side Jinja partials:

```html
<div id="app">
    {% include "templates/includes/vue_crud/header.html" %}
    {% include "templates/includes/vue_crud/messages.html" %}
    {% include "templates/includes/vue_crud/form.html" %}
    {% include "templates/includes/vue_crud/list.html" %}
</div>
```

The partials contain Vue directives such as `v-for`, `v-if`, `v-model`, and `@click`. Jinja assembles them on the server; Vue manages their reactive behavior in the browser.

This is different from Vue components and is useful to understand when working with Frappe Portal pages.

## Why generic CRUD?

A resource-specific implementation might have:

```text
list_books()
create_book()
update_book()
delete_book()
```

This example instead uses:

```text
list_objects()
get_object()
create_object()
update_object()
delete_object()
```

The requested DocType is supplied as configuration:

```javascript
const config = {
    doctype: "Book",
    object_label: "Book",
    objects_label: "Books",
    title_field: "name",
    fields: [
        { fieldname: "name", label: "Name", type: "text", required: true },
        { fieldname: "author", label: "Author", type: "text", required: true }
    ],
    api: {
        list: "test_app.api.crud.list_objects",
        get: "test_app.api.crud.get_object",
        create: "test_app.api.crud.create_object",
        update: "test_app.api.crud.update_object",
        delete: "test_app.api.crud.delete_object"
    }
};
```

To use the same page for another DocType, change the configuration and fields. The generic CRUD implementation does not need to be copied.

## Composition API

The reusable behavior is in `public/js/vue_crud/crud.js`:

```javascript
function useCrud(config) {
    // reactive state
    // API calls
    // create/update/delete behavior

    return {
        // state and methods
    };
}
```

The page simply does:

```javascript
const crud = useCrud(config);
```

and exposes the returned state and methods to the Vue template.

The generic names are intentional:

```text
objects_list  → collection of records
object        → record being created/edited
```

## Frappe API

The frontend calls the generic methods in `api/crud.py` using JSON. For example:

```json
{
    "doctype": "Book",
    "fields": ["name", "author"]
}
```

Create/update requests contain:

```json
{
    "doctype": "Book",
    "data": {
        "name": "Book 1",
        "author": "Author 1"
    }
}
```

The API validates requested fields against the requested DocType and checks normal Frappe permissions.

## Security lesson

Generic does not mean unrestricted.

The example accepts a DocType from the browser because that makes the generic concept easy to demonstrate. In a production application, consider an explicit allow-list such as:

```python
ALLOWED_DOCTYPES = {
    "Book",
    "Customer",
}
```

Then reject any DocType that is not allowed for that endpoint. Continue to rely on Frappe's normal read/create/write/delete permissions.

## Why Vue CDN?

The page uses:

```html
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
```

There is no npm, Node.js, Vite, webpack, or build step. That keeps this example focused on Vue and makes it easy to use in a Frappe Portal page.

## Suggested exercises

1. Change `Book` to another DocType.
2. Add another configured field.
3. Add a `textarea` field.
4. Add a `read_only` field.
5. Add a DocType allow-list to `api/crud.py`.
6. Add pagination to `list_objects()`.
7. Add a search box and pass filters to `list_objects()`.
8. Split the list into a reusable Vue component after learning the simpler Jinja-partial approach.

## Main lesson

```text
             configuration
                  │
                  ▼
             useCrud()
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   HTML partials        Frappe API
        │                   │
        └─────────┬─────────┘
                  ▼
              Any DocType
```

**Partials** keep the HTML readable.

**Composition API** keeps behavior reusable.

**Configuration** makes the resource-specific choices explicit.

**Generic Frappe methods** keep the server implementation reusable.
