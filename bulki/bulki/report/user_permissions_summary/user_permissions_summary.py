# Copyright (c) 2024, AjayRaj Mahiwal and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    """
    Generate a report of user permissions across the system
    
    :param filters: Dictionary of filters to apply to the report
    :return: Columns and data for the report
    """
    columns = [
        {
            "label": _("Name"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "User Permission",
            "width": 100
        },
        {
            "label": _("User"),
            "fieldname": "user",
            "fieldtype": "Link",
            "options": "User",
            "width": 200
        },
        {
            "label": _("Allow"),
            "fieldname": "allow",
            "fieldtype": "Link",
            "options": "DocType",
            "width": 150
        },
        {
            "label": _("Value"),
            "fieldname": "for_value",
            "fieldtype": "Dynamic Link",
            "options": "allow",
            "width": 200
        },
        {
            "label": _("Apply to All DocTypes"),
            "fieldname": "apply_to_all_doctypes",
            "fieldtype": "Check",
            "width": 170
        },
        {
            "label": _("Applicable For"),
            "fieldname": "applicable_for",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Is Default"),
            "fieldname": "is_default",
            "fieldtype": "Check",
            "width": 130
        }
    ]
    
    # Prepare conditions
    conditions = []
    values = {}
    
    if filters:
        if filters.get('user'):
            conditions.append("user = %(user)s")
            values['user'] = filters['user']
        
        if filters.get('allow'):
            conditions.append("allow = %(allow)s")
            values['allow'] = filters['allow']
        
        if filters.get('for_value'):
            conditions.append("for_value = %(for_value)s")
            values['for_value'] = filters['for_value']
    
    # Construct WHERE clause
    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    # Main query to fetch user permissions
    query = f"""
    SELECT 
        name,
        user,
        allow,
        for_value,
        is_default,
        apply_to_all_doctypes,
        applicable_for
    FROM 
        `tabUser Permission` main
    {where_clause}
    ORDER BY 
        user, allow, for_value
    """
    
    # Execute the query
    data = frappe.db.sql(query, values, as_dict=1)
    
    return columns, data