/* Resource-specific configuration. */
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
