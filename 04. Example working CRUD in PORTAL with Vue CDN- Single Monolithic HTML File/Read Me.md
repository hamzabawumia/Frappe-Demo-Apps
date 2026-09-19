# Example 04: Generic CRUD in a Frappe Portal with Vue CDN

This example shows how to build a **reusable CRUD page for Frappe Portal pages using Vue 3 from a CDN and the Composition API**.

Unlike the earlier Book-specific example, this example does not create functions such as:

```text
list_books()
create_book()
update_book()
delete_book()
```

Instead, it has generic operations:

```text
list_objects()
get_object()
create_object()
update_object()
delete_object()
```

The same Vue page can therefore be configured for different Frappe DocTypes.

---

## 1. What are we building?

The architecture is:

```text
                         Portal Page
                             │
                             ▼
                     Vue 3 Composition API
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

The important idea is that the Vue CRUD code does **not** know what an object represents.

It works with:

```javascript
objects_list
object
loadObjects()
saveObject()
deleteObject()
```

The DocType-specific information lives in a small configuration object.

---

# 2. Files in this example

```text
04. Example working CRUD in PORTAL with Vue CDN/
│
├── Read Me
│
├── hooks.py
│
├── api/
│   └── crud.py
│
└── www/
    └── crud.html
```

### `api/crud.py`

Contains the generic Frappe API:

```text
list_objects()
get_object()
create_object()
update_object()
delete_object()
```

### `www/crud.html`

Contains:

- Vue 3 CDN
- Composition API
- `useCrud(config)`
- dynamic form fields
- object list
- create
- update
- delete
- loading and error states

---

# 3. Why use a generic CRUD API?

A beginner may first write:

```python
def list_books():
    ...

def create_book():
    ...

def update_book():
    ...

def delete_book():
    ...
```

That works, but it couples the API to one DocType.

If we later want Customers, Employees, Tasks, or another DocType, we would have to duplicate the code.

The generic version instead accepts:

```text
doctype
fields
data
name
```

For example:

```text
doctype = "Book"
```

or:

```text
doctype = "Customer"
```

The CRUD implementation remains the same.

This is conceptually similar to the idea behind Django's generic views: the reusable mechanism is separated from the model/resource-specific configuration.

---

# 4. The generic Vue Composition function

The main reusable part is:

```javascript
function useCrud(config) {
    ...
}
```

It exposes generic reactive state:

```javascript
const objects_list = ref([]);
const object = ref({});
const loading = ref(false);
const saving = ref(false);
const editing = ref(false);
```

And generic operations:

```javascript
loadObjects()
startCreate()
editObject()
saveObject()
deleteObject()
resetForm()
```

The Composition API makes this logic independent from the HTML template.

The page then does:

```javascript
const crud = useCrud(config);
```

and exposes it to the template:

```javascript
return {
    ...crud
};
```

---

# 5. The configuration

Near the bottom of `www/crud.html` there is a configuration object:

```javascript
const config = {
    doctype: "Book",

    object_label: "Book",
    objects_label: "Books",

    title_field: "name",

    fields: [
        {
            fieldname: "name",
            label: "Name",
            type: "text",
            required: true
        },
        {
            fieldname: "author",
            label: "Author",
            type: "text",
            required: true
        }
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

This is the part that identifies the resource.

The CRUD implementation itself stays generic.

---

# 6. Using the same page for another DocType

Suppose your application has a `Customer` DocType.

You could change the configuration to:

```javascript
const config = {
    doctype: "Customer",

    object_label: "Customer",
    objects_label: "Customers",

    title_field: "customer_name",

    fields: [
        {
            fieldname: "name",
            label: "ID",
            type: "text",
            required: true
        },
        {
            fieldname: "customer_name",
            label: "Customer Name",
            type: "text",
            required: true
        },
        {
            fieldname: "customer_group",
            label: "Customer Group",
            type: "text",
            required: true
        }
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

No CRUD functions need to be rewritten.

---

# 7. Dynamic forms

One of the important Vue ideas demonstrated here is that the form is generated from configuration.

The HTML does not contain:

```html
<input v-model="object.author">
```

Instead it contains:

```html
<div
    v-for="field in editableFields"
    :key="field.fieldname"
>
    <label>
        {{ field.label }}
    </label>

    <input
        v-model="object[field.fieldname]"
    >
</div>
```

This means the same form can render different fields.

For example:

```javascript
fields: [
    {
        fieldname: "name",
        label: "Name"
    },
    {
        fieldname: "author",
        label: "Author"
    }
]
```

produces a Book form.

Changing the configuration to:

```javascript
fields: [
    {
        fieldname: "name",
        label: "ID"
    },
    {
        fieldname: "customer_name",
        label: "Customer Name"
    },
    {
        fieldname: "customer_group",
        label: "Customer Group"
    }
]
```

produces a Customer form.

---

# 8. Why use `object[field.fieldname]`?

This is an important JavaScript concept.

Instead of:

```javascript
object.author
```

we can use:

```javascript
object[field.fieldname]
```

If:

```javascript
field.fieldname = "author"
```

then:

```javascript
object[field.fieldname]
```

means:

```javascript
object["author"]
```

If the field changes to:

```javascript
field.fieldname = "customer_name"
```

then the exact same code accesses:

```javascript
object["customer_name"]
```

This is what allows the form to be dynamic.

---

# 9. Generic Frappe API

The backend exposes:

```python
@frappe.whitelist()
def list_objects(doctype, fields=None, filters=None):
    ...
```

and:

```python
@frappe.whitelist()
def create_object(doctype, data):
    ...
```

and:

```python
@frappe.whitelist()
def update_object(doctype, name, data):
    ...
```

and:

```python
@frappe.whitelist()
def delete_object(doctype, name):
    ...
```

The Vue application sends JSON such as:

```json
{
    "doctype": "Book",
    "data": {
        "name": "The Hobbit",
        "author": "J.R.R. Tolkien"
    }
}
```

For another DocType:

```json
{
    "doctype": "Customer",
    "data": {
        "customer_name": "Acme",
        "customer_group": "Commercial"
    }
}
```

The same API handles both.

---

# 10. Server-side validation

Generic does **not** mean that the browser gets to execute arbitrary database operations.

The API checks that the requested DocType exists:

```python
frappe.db.exists("DocType", doctype)
```

It also checks the user's Frappe permission:

```python
frappe.has_permission(
    doctype,
    ptype="read"
)
```

For writes, the appropriate permission is checked:

```text
create
write
delete
```

The API also validates the requested fields against the DocType metadata.

This is important because the browser is never a security boundary.

---

# 11. Why this example does not use `allow_guest=True`

The previous Book example used:

```python
@frappe.whitelist(allow_guest=True)
```

because it was demonstrating a very simple public example.

That approach is especially dangerous for a generic API because the client supplies a DocType name.

Imagine exposing:

```text
create_object(doctype="SomeSensitiveDocType")
```

to arbitrary Guest users.

Even though the page might only display Books, the API could potentially be called directly.

This example therefore uses normal authenticated Frappe permissions:

```python
@frappe.whitelist()
```

and:

```python
frappe.has_permission(...)
```

For a real portal application, also think carefully about **which records** a user is allowed to access, not only whether they have permission on the DocType.

For example, a portal user may be allowed to read only their own Customer records.

That kind of ownership/business-rule filtering belongs on the server.

---

# 12. CSRF

Write requests send Frappe's CSRF token:

```javascript
headers: {
    "X-Frappe-CSRF-Token": csrfToken
}
```

The page gets it from:

```javascript
const csrfToken = frappe.csrf_token;
```

This is needed when making POST requests from the browser.

---

# 13. Why use POST for the CRUD methods?

For this beginner example, all API operations are called using POST:

```javascript
fetch("/api/method/...", {
    method: "POST"
})
```

This keeps the example focused on:

```text
Vue state
    ↓
JSON
    ↓
Frappe method
```

Rather than introducing a separate REST routing layer.

Frappe's whitelisted methods are sufficient for this pattern.

---

# 14. Portal URL

Because the file is:

```text
www/crud.html
```

Frappe will expose it as a website route:

```text
/crud
```

depending on your site's normal website routing configuration.

For example:

```text
http://your-site.local/crud
```

---

# 15. How the CRUD flow works

## Read

When Vue mounts:

```javascript
onMounted(() => {
    crud.loadObjects();
});
```

Vue calls:

```text
list_objects()
```

The API returns JSON.

Vue stores it in:

```javascript
objects_list.value
```

and Vue automatically updates the HTML.

---

## Create

The user clicks:

```text
New Book
```

which calls:

```javascript
startCreate()
```

The form is cleared.

On submit:

```javascript
saveObject()
```

calls:

```text
create_object()
```

After creation:

```javascript
loadObjects()
```

is called again.

---

## Update

The user clicks:

```text
Edit
```

which calls:

```javascript
editObject(item)
```

The selected object is copied into:

```javascript
object.value
```

After submitting, the API receives:

```text
update_object()
```

and the list is refreshed.

---

## Delete

The user clicks:

```text
Delete
```

Vue asks for confirmation and then calls:

```text
delete_object()
```

After deletion, the list is loaded again.

This "reload after mutation" approach is intentional.

It is easier for beginners to understand than introducing a client-side cache or manually modifying several pieces of state.

---

# 16. Why `objects_list` instead of `objects`?

The name is deliberately explicit for beginners:

```javascript
const objects_list = ref([]);
```

It represents:

```text
the list of objects returned by the API
```

while:

```javascript
const object = ref({});
```

represents:

```text
the single object currently being created or edited
```

So the mental model is:

```text
objects_list → many records

object       → one record
```

This is also useful when explaining the pattern to someone coming from Django.

---

# 17. Why `ref()`?

Vue's Composition API uses:

```javascript
const loading = ref(false);
```

The actual value is accessed in JavaScript with:

```javascript
loading.value
```

For example:

```javascript
loading.value = true;
```

Inside the Vue template, Vue automatically unwraps refs:

```html
<div v-if="loading">
    Loading...
</div>
```

This is one of the fundamental Composition API concepts demonstrated by this example.

---

# 18. Why use a Composition function?

Without a Composition function, the page could become one large block:

```text
Vue app
 ├── loading
 ├── list
 ├── create
 ├── update
 ├── delete
 ├── error handling
 ├── HTTP requests
 └── form handling
```

With:

```javascript
useCrud(config)
```

the reusable CRUD behavior has its own boundary.

Conceptually:

```text
                    useCrud()
                       │
       ┌───────────────┼───────────────┐
       │               │               │
      READ           WRITE           DELETE
       │               │               │
 listObjects     saveObject      deleteObject
```

The page mainly supplies configuration and presentation.

---

# 19. Why Vue CDN?

This example intentionally does **not** use:

```text
npm
Vite
Webpack
Node.js
package.json
```

Instead:

```html
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
```

is enough to start using Vue 3.

This makes it particularly useful for beginners who are already comfortable with:

```text
Frappe
Jinja
HTML
JavaScript
```

but are not ready to introduce a frontend build system.

For larger Vue applications, a normal Vue project with a build tool may be more appropriate.

---

# 20. Exercises

After understanding this example, try the following.

### Exercise 1 — Change Book to another DocType

Use:

```text
Task
```

or:

```text
Customer
```

and change only `config`.

---

### Exercise 2 — Add another field

For Book:

```javascript
{
    fieldname: "publisher",
    label: "Publisher",
    type: "text"
}
```

Then create the corresponding field in the DocType.

The form and list will use it automatically.

---

### Exercise 3 — Add a textarea

Try:

```javascript
{
    fieldname: "description",
    label: "Description",
    type: "textarea"
}
```

The existing template already demonstrates how to render a textarea.

---

### Exercise 4 — Add a search box

Add:

```javascript
const search = ref("");
```

Then filter `objects_list` using a computed property.

---

### Exercise 5 — Add pagination

Modify `list_objects()` to accept:

```text
limit_start
limit_page_length
```

and expose Next/Previous buttons in Vue.

---

### Exercise 6 — Add filters

Extend the configuration with:

```javascript
filters: {
    status: "Open"
}
```

and send those filters to:

```python
list_objects()
```

---

### Exercise 7 — Add DocType-specific permissions

Do not assume that:

```text
has_permission(doctype, "read")
```

is enough for a portal application.

For example, implement:

```text
Customer
    ↓
only customers belonging to the logged-in portal user
```

This is an important real-world Frappe concept.

---

# 21. The main lesson

The biggest idea in this example is not Vue.

It is **separation between reusable behavior and configuration**.

Instead of writing:

```text
Book CRUD
Customer CRUD
Employee CRUD
Task CRUD
```

we build:

```text
             Generic CRUD
                  │
        ┌─────────┼─────────┐
        │         │         │
       Book    Customer   Employee
        │         │         │
     config     config    config
```

The CRUD mechanism stays the same.

Only the resource configuration changes.

That is the pattern to take away from this example.
