from django import template

register = template.Library()

@register.filter
def status_progress(status):
    """
    Convert a ticket status string into a numeric percentage
    for the progress bar in ticket_list.html.
    """
    mapping = {
        "Open": 10,
        "New": 10,
        "In Progress": 50,
        "Awaiting User": 70,
        "Pending Approval": 85,
        "Resolved": 100,
        "Closed": 100,
    }

    # Make sure we can handle None or unexpected values
    if status is None:
        return 0

    return mapping.get(str(status), 20)
