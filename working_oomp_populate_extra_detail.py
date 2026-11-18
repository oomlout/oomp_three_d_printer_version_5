"""Attach optional verified evidence to existing IDs before they are written."""
def main(**kwargs):
    extras = kwargs.get("extras", [])
    details_by_id = kwargs.get("details_by_id", {})
    by_id = {part["oomp_id"]: part for part in extras}
    for part_id, details in details_by_id.items():
        by_id[part_id]["specifications"].update(details)
