
frappe.views.calendar["Conference"] = {
    field_map: {
        "start": "start_date", 
        "end": "end_date", 
        "title": "title", 
        "eventColor": "color"
    },
    gantt: true,
    
    get_events_method: "e_desk.e_desk.doctype.conference.conference.get_confer_agenda_events"
};
