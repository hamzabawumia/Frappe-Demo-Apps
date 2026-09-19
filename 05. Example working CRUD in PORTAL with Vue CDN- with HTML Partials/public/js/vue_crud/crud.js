/* Generic CRUD Composition API. */
const { ref, computed } = Vue;

function useCrud(config) {
    const objects_list = ref([]);
    const object = ref({});
    const loading = ref(false);
    const saving = ref(false);
    const editing = ref(false);
    const message = ref({ text: "", type: "success" });
    const csrfToken = frappe.csrf_token;

    function showMessage(text, type = "success") { message.value = { text, type }; }
    function clearMessage() { message.value = { text: "", type: "success" }; }

    function newObject() {
        const values = {};
        for (const field of config.fields) values[field.fieldname] = field.default ?? "";
        object.value = values;
    }

    function resetForm() { editing.value = false; newObject(); }

    function getErrorMessage(result) {
        if (result._server_messages) {
            try {
                const messages = JSON.parse(result._server_messages);
                if (Array.isArray(messages) && messages.length) {
                    return messages.map(message => {
                        try { return JSON.parse(message).message; }
                        catch { return message; }
                    }).join("\n");
                }
            } catch { /* fall through */ }
        }
        return result.exception || result.message || "The server returned an error.";
    }

    async function request(method, payload = {}) {
        const response = await fetch(`/api/method/${method}`, {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-Frappe-CSRF-Token": csrfToken
            },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        if (!response.ok || result.exc) throw new Error(getErrorMessage(result));
        return result.message;
    }

    async function loadObjects(showErrors = true) {
        loading.value = true;
        try {
            objects_list.value = await request(config.api.list, {
                doctype: config.doctype,
                fields: config.fields.map(field => field.fieldname)
            });
        } catch (error) {
            if (showErrors) showMessage(error.message, "error");
        } finally { loading.value = false; }
    }

    function startCreate() { clearMessage(); editing.value = false; newObject(); }
    function editObject(item) { clearMessage(); editing.value = true; object.value = { ...item }; }

    async function saveObject() {
        saving.value = true;
        clearMessage();
        try {
            const data = {};
            for (const field of config.fields) {
                if (field.read_only && field.fieldname !== "name") continue;
                data[field.fieldname] = object.value[field.fieldname];
            }
            if (editing.value) {
                const name = object.value.name;
                await request(config.api.update, { doctype: config.doctype, name, data });
                showMessage(`${config.object_label} '${name}' updated successfully.`);
            } else {
                const created = await request(config.api.create, { doctype: config.doctype, data });
                showMessage(`${config.object_label} '${created.name}' created successfully.`);
            }
            resetForm();
            await loadObjects(false);
        } catch (error) { showMessage(error.message, "error"); }
        finally { saving.value = false; }
    }

    async function deleteObject(name) {
        if (!confirm(`Delete '${name}'?`)) return;
        saving.value = true;
        clearMessage();
        try {
            await request(config.api.delete, { doctype: config.doctype, name });
            showMessage(`${config.object_label} '${name}' deleted successfully.`);
            if (object.value.name === name) resetForm();
            await loadObjects(false);
        } catch (error) { showMessage(error.message, "error"); }
        finally { saving.value = false; }
    }

    const editableFields = computed(() => config.fields.filter(field => !field.read_only));
    const listFields = computed(() => config.fields);
    function displayValue(item, fieldname) {
        const value = item[fieldname];
        return value === null || value === undefined || value === "" ? "—" : value;
    }

    return {
        objects_list, object, loading, saving, editing, message,
        editableFields, listFields, displayValue,
        loadObjects, startCreate, editObject, saveObject, deleteObject, resetForm
    };
}
