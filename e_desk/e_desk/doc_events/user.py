import frappe
from e_desk.e_desk.doctype.registration_desk.registration_desk import RegistrationDesk

def after_insert(doc,method=None):
    qr = RegistrationDesk.create_qr_participant(doc) 
    doc.db_set("custom_qr", qr)
   