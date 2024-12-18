// Copyright (c) 2024, AjayRaj Mahiwal and contributors
// For license information, please see license.txt


frappe.query_reports["User Permissions Summary"] = {
    "filters": [
        {
            "fieldname": "user",
            "label": __("User"),
            "fieldtype": "Link",
            "options": "User"
        },
        {
            "fieldname": "allow",
            "label": __("Allow"),
            "fieldtype": "Link",
            "options": "DocType"
        },
        {
            "fieldname": "for_value",
            "label": __("For Value"),
            "fieldtype": "Dynamic Link",
            "options": "allow",
            "depends_on": "eval:doc.allow"
        }
    ]
};