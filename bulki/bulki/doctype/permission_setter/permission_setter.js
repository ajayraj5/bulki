// Copyright (c) 2024, AjayRaj Mahiwal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Permission Setter", {
	refresh(frm) {
        frm.page.btn_primary.hide();
        frm.page.wrapper.find('.btn.btn-default.icon-btn').hide();
        if (frm.page.btn_more) {
            frm.page.btn_more.hide();
        }
        

        frm.add_custom_button(__("Get Permissions Of"), function(){
            let d = new frappe.ui.Dialog({
                title:"Enter Details",
                fields:[
                    {
                        "fieldname": "user",
                        "fieldtype": "Table MultiSelect",
                        "label": "User",
                        "options": "User Selector Item",
                        "reqd": 1
                    },
                    {
                        "fieldname":'get_all_user_permissions',
                        "fieldtype": "Check",
                        "label":"Get All User Permissions",
                        "default":"0"
                    },
                    {
                        "fieldname": "allow",
                        "fieldtype": "Table MultiSelect",
                        "label": "Allow",
                        "options": "Allowed DocTypes Item",
                        "depends_on": "eval:doc.get_all_user_permissions==0",
                        "mandatory_depends_on": "eval: doc.get_all_user_permissions==0"
                    },
                ],
                size: 'extra-large',
                primary_action_label: 'Get User Permissions',
                primary_action(values){
                    frappe.call({
                        method: "bulki.bulki.doctype.permission_setter.permission_setter.get_user_permissions",
                        args:{
                            users: values.user || [],
                            allows: values.allow || [],
                            get_all_user_permissions: values.get_all_user_permissions
                        },
                        callback: function(response){
                            if(response.message){
                                frappe.msgprint({
                                    title: __("Permissions Retrieved"),
                                    message: "All User Permissions Retrieved Successfully !",
                                    indicator: 'green'
                                });

                                for(let r of response.message){
                                    // Check if a row with the same values already exists
                                    
                                    let exists = frm.doc.user_permission_item.some(row => {
                                        // If apply_to_all_doctypes is not true, compare applicable_for as well
                                        if (row.apply_to_all_doctypes !== true) {
                                            return row.allow === r.allow &&
                                                   row.for_value === r.for_value &&
                                                   row.apply_to_all_doctypes === r.apply_to_all_doctypes &&
                                                   row.is_default === r.is_default &&
                                                   row.applicable_for === r.applicable_for; // Compare applicable_for
                                        } else {
                                            // If apply_to_all_doctypes is true, only compare the other fields
                                            return row.allow === r.allow &&
                                                   row.for_value === r.for_value &&
                                                   row.apply_to_all_doctypes === r.apply_to_all_doctypes &&
                                                   row.is_default === r.is_default;
                                        }
                                    });

                                    // If the row doesn't exist, add it
                                    if (!exists) {
                                        frm.add_child('user_permission_item', {
                                            user: r.user,
                                            allow: r.allow,
                                            for_value: r.for_value,
                                            apply_to_all_doctypes: r.apply_to_all_doctypes,
                                            is_default: r.is_default
                                        });
                                    }
                                }
                                frm.refresh_field('user_permission_item');
                            }
                        }
                    })
                    d.hide();
                }
            });
            d.show();
        },"Actions")


        frm.add_custom_button(__("Remove User Permissions"), function(){
            frappe.call({
                method: "bulki.bulki.doctype.permission_setter.permission_setter.remove_user_permissions",
                args:{
                    users: frm.doc.user || [],
                    user_permissions: frm.doc.user_permission_item || []
                },
                callback: function(response){
                    if(response.message){
                        frappe.msgprint({
                            title: "Permission Removed",
                            message: response.message,
                            indicator: 'green'
                        })
                    }
                }
            })
        },"Actions");


        frm.add_custom_button(__("Set Permissions"), function(){
            frm.doc.__unsaved = 1;
            frm.save();
        });
	},
    user(frm){
        if (frm.page.btn_primary) {
            frm.page.btn_primary.text('Set Permissions');
        }
        
    },
});