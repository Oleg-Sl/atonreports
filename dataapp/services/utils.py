import pprint


def get_events(bx24, event_name, limit):
    response = bx24.call("event.offline.get", {
        "filter": {
            "EVENT_NAME": event_name
        },
        "order": {"TIMESTAMP_X": "ASC"},
        "limit": limit
    })
    if not response or "result" not in response or not "events" in response["result"]:
        return

    events = response["result"]["events"]
    # pprint.pprint(events)

    events_data = []
    for event in events:
        # event_data = event.get("EVENT_DATA", {}).get("FIELDS", {}).get("ID", {})
        event_data = event.get("EVENT_DATA", {})
        events_data.append(event_data)

    return events_data


def editing_money_in_number(numb):
    """ Преобразует денежное значение из BX24 в число """
    numb = numb.split("|")[0] or "0"
    if numb:
        return f"{float(numb):.2f}"
    else:
        return None
