"""
Generic CRUD API for the Vue CDN portal example.

The API deliberately accepts a DocType name and a dictionary of field values.
This lets the same Vue page work with different Frappe DocTypes.

IMPORTANT:
- This is a learning example.
- Do not expose arbitrary DocTypes to Guest users in a real application.
- Server-side Frappe permissions are checked before every operation.
"""

import json

import frappe


# Frappe's standard fields are available on every normal DocType.
STANDARD_FIELDS = {
    "name",
    "owner",
    "creation",
    "modified",
    "modified_by",
    "docstatus",
    "idx",
}


def _json(value):
    """Turn a JSON string into a Python value."""
    if isinstance(value, str):
        return json.loads(value)
    return value


def _get_meta(doctype):
    """Return DocType metadata and fail clearly for invalid DocTypes."""
    if not doctype:
        frappe.throw("doctype is required.")

    if not frappe.db.exists("DocType", doctype):
        frappe.throw(f"DocType '{doctype}' does not exist.")

    return frappe.get_meta(doctype)


def _check_permission(doctype, permission):
    """Use normal Frappe DocType permissions."""
    if not frappe.has_permission(doctype, ptype=permission):
        frappe.throw(
            f"You do not have permission to {permission} {doctype}.",
            frappe.PermissionError,
        )


def _validate_fields(meta, fields):
    """
    Only allow real fields from the requested DocType.

    This prevents a client from passing arbitrary SQL expressions as fields.
    """
    if not fields:
        return ["name"]

    if not isinstance(fields, list):
        frappe.throw("fields must be a JSON list.")

    allowed = STANDARD_FIELDS | {df.fieldname for df in meta.fields}

    invalid = [field for field in fields if field not in allowed]

    if invalid:
        frappe.throw(
            "Invalid field(s): " + ", ".join(invalid)
        )

    return fields


def _validate_data(meta, data):
    """
    Only accept actual DocType fields.

    'name' is handled by Frappe during create/update and is allowed here.
    """
    if not isinstance(data, dict):
        frappe.throw("data must be a JSON object.")

    # Standard audit fields such as owner and modified are read-only.
    allowed = {"name"} | {df.fieldname for df in meta.fields}
    invalid = [field for field in data if field not in allowed]

    if invalid:
        frappe.throw(
            "Invalid field(s): " + ", ".join(invalid)
        )

    return data


@frappe.whitelist()
def list_objects(doctype, fields=None, filters=None):
    """
    Return a list of objects for any DocType the current user can read.

    Example:
        /api/method/test_app.api.crud.list_objects
    """
    meta = _get_meta(doctype)
    _check_permission(doctype, "read")

    fields = _validate_fields(meta, _json(fields))
    filters = _json(filters) if filters else {}

    return frappe.get_list(
        doctype,
        fields=fields,
        filters=filters,
        order_by="modified desc",
    )


@frappe.whitelist()
def get_object(doctype, name, fields=None):
    """Return one object."""
    meta = _get_meta(doctype)
    _check_permission(doctype, "read")

    fields = _validate_fields(meta, _json(fields))

    doc = frappe.get_doc(doctype, name)

    return {
        field: doc.get(field)
        for field in fields
    }


@frappe.whitelist()
def create_object(doctype, data):
    """Create a document from a generic JSON object."""
    meta = _get_meta(doctype)
    _check_permission(doctype, "create")

    data = _validate_data(meta, _json(data))

    # Do not allow the client to choose the DocType.
    document_data = {
        "doctype": doctype,
        **data,
    }

    doc = frappe.get_doc(document_data)
    doc.insert()

    return doc.as_dict()


@frappe.whitelist()
def update_object(doctype, name, data):
    """Update a document from a generic JSON object."""
    meta = _get_meta(doctype)
    _check_permission(doctype, "write")

    data = _validate_data(meta, _json(data))

    # Never allow the primary key to be changed through this endpoint.
    data.pop("name", None)

    doc = frappe.get_doc(doctype, name)

    for field, value in data.items():
        doc.set(field, value)

    doc.save()

    return doc.as_dict()


@frappe.whitelist()
def delete_object(doctype, name):
    """Delete a document."""
    _get_meta(doctype)
    _check_permission(doctype, "delete")

    frappe.delete_doc(doctype, name)

    return {"name": name}
