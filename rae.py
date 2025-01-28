import json
import os


def get_types(cards):
    types = []

    for card in cards:
        if card["type"] not in types:
            types.append(card["type"])

    print(types)


def get_allowed_cards(raw_cards):
    allowed_types = ["Unit", "Landmark"]

    formatted_cards = []

    for card in raw_cards:
        if card["type"] in allowed_types:
            formatted_card = {}
            formatted_card["code"] = card["cardCode"]
            formatted_card["img"] = card["assets"][0]["fullAbsolutePath"]
            formatted_card["name"] = card["name"]
            formatted_card["regions"] = card["regions"]
            if card["supertype"] != "Champion":
                if not any(
                    d["name"] == formatted_card["name"] for d in formatted_cards
                ):
                    formatted_cards.append(formatted_card)
            else:
                formatted_cards.append(formatted_card)

    return formatted_cards


def write_formatted_json(raw_cards):
    with open("data/cards.json", "w") as f:
        json.dump(get_allowed_cards(raw_cards), f)


def get_all_cards():
    files = os.listdir("data")
    files.remove("cards.json")

    all_cards = []

    for file in files:
        with open(f"data/{file}") as f:
            temp_cards = json.load(f)
            all_cards.extend(temp_cards)

    return all_cards


cards = get_all_cards()
get_types(cards)
write_formatted_json(cards)
