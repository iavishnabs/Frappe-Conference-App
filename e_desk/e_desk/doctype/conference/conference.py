# Copyright (c) 2025, Anther Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
# from frappe.utils import get_timezones
from datetime import date,datetime


class Conference(WebsiteGenerator):

	def before_save(self):
        # Create a folder for this conference if it doesn't already exist
		if self.registration_close_date>=self.end_date:
			frappe.throw("The registration closing date cannot be greater than the event end date.")
		self.create_confer_folder()

	def  on_update(self):
		
		self.move_category_files_to_folder()
		
	def create_confer_folder(self):

		folder_name = self.title
		print(folder_name,"folder_namefolder_namefolder_name")
		
        # Check if the folder already exists
		
		existing_folder = frappe.db.exists('File', {'file_name': folder_name, 'is_folder': 1})
		print("existing_folderexisting_folderexisting_folderexisting_folder......................................................")
		
		if not existing_folder:
			
			
			new_folder = frappe.get_doc({
                "doctype": "File",
                "file_name": folder_name,
                "is_folder": 1,
                "folder": "Home", # Root folder or modify if necessary
				"is_private": 1
            })
			
			new_folder.insert()
			frappe.msgprint(f"Folder '{folder_name}' created successfully!")


	def move_category_files_to_folder(self):
		
		folder_name = self.title
		print(folder_name,"folder name.......................")
		
		folder_path = frappe.db.get_value('File', {'file_name': folder_name, 'is_folder': 1})
		print(folder_path,"folder path")
		
		if folder_path:
			for category_file in self.attach_files:
				
				if category_file.attach:
					print(category_file.attach,"category_file.attach_filescategory_file.attach_files")
					# file_doc = frappe.get_doc('File', {'file_url': category_file.attach}, 'name')
					file_list = frappe.get_list('File', filters={'file_url': category_file.attach}, fields=['name'])
					if file_list:
						# Get the latest document's name
						file_doc_name = file_list[-1].name  # Get the last document (if needed)
						
						# Now, get the actual document using the name
						file_doc = frappe.get_doc('File', file_doc_name)
					
					# file_doc = frappe.get_doc("File", category_file.attach)
					print(file_doc,"file_doc ....................this is file_doc............................")
					if file_doc.folder != folder_path:  
						file_doc.folder = folder_path	
						file_doc.save()
						frappe.msgprint(f"File '{file_doc.file_name}' moved to folder '{folder_name}'")
						
	def before_insert(self):
		# Reset is_default when duplicating
		if self.is_new() and self.is_default:
			self.is_default = 0

	def get_context(self, context):
		context.agenda_list = get_agenda_data(self)
		context.speakers = get_speakers_for_event(self.name)
		context.registration_types = get_registration_types()
		return context


@frappe.whitelist()
def update_is_default_for_others(confer_name):

	confer_list = frappe.get_all("Confer", filters={"is_default": 1, "name": ["!=", confer_name]}, fields=["name"])
	frappe.db.set_value("Conference Settings", None, "event", confer_name)
	for confer in confer_list:
		frappe.db.set_value("Confer", confer['name'], "is_default", 0)

	frappe.db.commit()

def get_agenda_data(self):
	agenda = self.agenda or []
	result = []

	for item in agenda:
		result.append({
			"program_agenda": item.program_agenda or "",
			"description": item.description or "",
			"start_date": item.start_date or "",
			"end_date": item.end_date or "",
		})
	return result


def get_speakers_for_event(event_name):
	print("\n\n\n\n")
	speakers = frappe.get_all(
		"Event Speakers",
		filters={"conference": event_name},
		fields=["participant", "full_name"]
	)
	speaker_list = []
	for s in speakers:
		event_participant = frappe.get_doc("Event Participant", s.participant)
		print("event participnt::",event_participant) 
		partc = event_participant.participant
		participant_doc = frappe.get_doc("Participant", partc)
		speaker_list.append({
			"full_name": s.full_name,
			"event_participant_docname": s.participant,
			"photo": participant_doc.profile_photo,
			"participant_id": partc,
		})
	return speaker_list

@frappe.whitelist()
def create_event_registration(data):
	print("hhhhhhhhh")
	# frappe.throw("kkkk")

	# data = frappe.parse_json(data)

	# doc = frappe.get_doc({
	# 	"doctype": "Event Registration",
	# 	"event": data.get("event"),
	# 	"full_name": data.get("full_name"),
	# 	"email": data.get("email"),
	# 	"phone": data.get("phone"),
	# 	# "address": data.get("address"),
	# 	"registration_type": data.get("registration_type"),
	# 	"company_name": data.get("company_name"),
	# 	"gstn": data.get("gstn"),
	# })

	# doc.insert(ignore_permissions=True)
	# frappe.db.commit()

	return {"status": "success"}

import frappe

def get_registration_types():
    return frappe.get_all(
        "Registration Type",
        fields=["name"],
        order_by="idx asc"
    )
