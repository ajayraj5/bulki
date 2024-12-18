# Copyright (c) 2024, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PermissionSetter(Document):
    def validate(doc):

        for user in doc.user:
            for permission in doc.user_permission_item:
                filters = {
                    'user': user.user,
                    'allow': permission.allow,
                    'for_value': permission.for_value,
                    'apply_to_all_doctypes': permission.apply_to_all_doctypes,
                    'is_default': permission.is_default
                }

                if not permission.apply_to_all_doctypes:
                    filters['applicable_for'] = permission.applicable_for

                # Check if a matching document exists
                existing_doc = frappe.db.get_value(
                    "User Permission",
                    filters,
                    "name"
                )

                if not existing_doc:
                    # Insert the document if it doesn't exist
                    user_per_doc = frappe.get_doc({
                        'doctype': "User Permission",
                        **filters
                    })
                    user_per_doc.insert()
                # 	frappe.msgprint("User Permission has been created.")
                # else:
                # 	frappe.msgprint(f"User Permission already exists: {existing_doc}")
        frappe.msgprint("User permissions have been successfully created.")



                    

    
@frappe.whitelist()
def get_user_permissions(users, allows, get_all_user_permissions):
    users = frappe.parse_json(users)
    allows = frappe.parse_json(allows)
    get_all_user_permissions = frappe.parse_json(get_all_user_permissions)
    

    user_list = [u['user'] for u in users if 'user' in u]

    permissions = None

    if (get_all_user_permissions) :
        permissions = frappe.get_all("User Permission",
            filters={
                "user":["in",user_list],
            },
            fields=["allow", "for_value", "apply_to_all_doctypes", "is_default"]
        )

    else:
        allow_list = [a['allow'] for a in allows if 'allow' in a]

        permissions = frappe.get_all("User Permission",
            filters={
                "user":["in",user_list],
                "allow":["in", allow_list]
            },
            fields=["allow", "for_value", "apply_to_all_doctypes", "is_default"]
        )


    union_of_permissions = list({frozenset(perm.items()) for perm in permissions})
    union_of_permissions = [dict(d) for d in union_of_permissions]

    return union_of_permissions





@frappe.whitelist()
def remove_user_permissions(users, user_permissions):
    users = frappe.parse_json(users)
    user_permissions = frappe.parse_json(user_permissions)

    user_list = [u['user'] for u in users if 'user' in u]
    for user in user_list:
        for permission in user_permissions:
            filters = {
                    'user': user,
                    'allow': permission['allow'],
                    'for_value': permission['for_value'],
                    'apply_to_all_doctypes': permission['apply_to_all_doctypes'],
                    'is_default': permission['is_default']
                }
            
            if not permission['apply_to_all_doctypes']:
                filters['applicable_for'] = permission.applicable_for

            existing_doc = frappe.db.get_value(
                    "User Permission",
                    filters,
                    "name"
                )

            if existing_doc:
                frappe.delete_doc('User Permission', existing_doc)
            #     frappe.msgprint("User Permission removed.")
            # else:
            #     frappe.msgprint("User Permission not exists.")


    return "The selected User permissions have been successfully removed."
    
    