import pprint

from bitrix24 import tokens


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
    events_data = []
    for event in events:
        event_data = event.get("EVENT_DATA", {})
        events_data.append(event_data)

    return events_data


def editing_money_in_number(numb):
    """ Преобразует денежное значение из BX24 в число """

    if numb:
        numb = numb.split("|")[0] or "0"
        return f"{float(numb):.2f}"
    else:
        return None


def get_url_user(id_user):
    domain = tokens.get_secret("domain")
    return f"https://{domain}/company/personal/user/{id_user}/"

