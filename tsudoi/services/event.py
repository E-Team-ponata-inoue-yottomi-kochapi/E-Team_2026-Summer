from models.event import find_open_event_by_id, get_owner_by_event_id, get_fee_rules_by_event_id

def get_event_detail(event_id):
    event = find_open_event_by_id(event_id)
    if event is None:
        return None
    owner = get_owner_by_event_id(event_id)
    fee_rules = get_fee_rules_by_event_id(event_id)
    return {"event": event, "owner": owner, "fee_rules": fee_rules}