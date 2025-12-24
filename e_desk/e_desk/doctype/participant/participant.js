// Copyright (c) 2025, Anther Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant', {
	//Create button for converting the participant to volunteer
	refresh: function(frm) {
		// connectionlist(frm)
		var hasPermission = frappe.user.has_role('Volunteer'); 
			  if (hasPermission) {

				function addRoleButton(label, role) {
					frm.add_custom_button(__(label), function () {
						let d = new frappe.ui.Dialog({
							title: 'Enter details',
							fields: [
								{
									label: 'Confer List',
									fieldname: 'confer',
									fieldtype: 'Link',
									options: 'Conference',
									reqd: 1,
									get_query: () => ({
										query: "e_desk.e_desk.utils.role.get_filtered_confer",
										filters: { participant: frm.doc.name }
									})
								}
							],
							primary_action_label: 'Submit',
							primary_action(values) {
								console.log("rrrrrrrrrrrrrrr",role)
								frappe.call({
									method: "e_desk.e_desk.utils.role.update_event_participant_role",
									args: {
										participant: frm.doc.name,
										confer: values.confer,
										role_name: role
									},
									callback: () => {
										frappe.msgprint(`${label} Updated Successfully`);
										d.hide();
									}
								});
							}
						});
					d.show();
				}, __("Create"));
			}
		
			addRoleButton('Volunteer', 'Volunteer');
			// if (1 === 1) addRoleButton('Poll Master', 'Poll Master');
		}

		load_contact_html(frm);
		load_address_html(frm);

},
contact(frm) {
	load_contact_html(frm);
},
address(frm) {
	load_address_html(frm);
}
});

function load_contact_html(frm) {
    if (!frm.doc.participant_contact) {
        frm.get_field("contact_html").$wrapper.html(
        );
        return;
    }
    frappe.call({
        method: "e_desk.e_desk.doctype.participant.participant.get_contact_html",
        args: {
            contact_name: frm.doc.participant_contact
        },
        callback: function (r) {
            if (r.message) {
                frm.get_field("contact_html").$wrapper.html(r.message);
            }
        }
    });
}

function load_address_html(frm) {
	if (!frm.doc.participant_address) {
		frm.get_field("address_html").$wrapper.html("");
		return;
	}
	frappe.call({
		method: "e_desk.e_desk.doctype.participant.participant.get_address_html",
		args: {
			address_name: frm.doc.participant_address
		},
		callback: function (r) {
			if (r.message) {
				frm.get_field("address_html").$wrapper.html(r.message);
			}
		}
	});
}
