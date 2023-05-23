import sys
import json
import random
from openai_utils import send_message_to_openai

sofia = ("Tarot card reader.")


def get_tarot_deck():
    major_arcana = [f"{name}" for i, name in enumerate(["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"])]
    minor_arcana = [f"{rank} of {suit}" for i, suit in enumerate(["Wands", "Cups", "Swords", "Pentacles"]) for rank in ["Ace"] + [str(n) for n in range(2, 11)] + ["Page", "Knight", "Queen", "King"]]
    deck = major_arcana + minor_arcana
    return [(card, 'upright' if random.randint(0, 1) == 0 else 'reversed') for card in deck]

def deal_cards(deck, num_cards):
    return random.sample(deck, num_cards)

def ask_for_card(position, card, orientation, spread, question):
    interpretation = send_message(f"Interpret the following card {card} in the {orientation} position for the {position} position in the {spread} spread. If the user has a question, consider the question: {question}. If it makes sense, tell a short story or analogy.")
    return position, card, orientation, interpretation

def save_reading(folder_name, spread, overall_interpretation, spread_name):
    position_names = get_position_names(spread_name)
    reading_data = {"reading": []}

    for position, card_data in spread.items():
        reading_data["reading"].append({
            "card": card_data['card'],
            "position": position_names[str(position)],
            "orientation": card_data['orientation'],
            "interpretation": card_data['interpretation']
        })

    reading_data["overall"] = overall_interpretation

    with open(f"{folder_name}/reading.json", "w") as f:
        json.dump(reading_data, f)


def send_message(user_content):
    messages = [
        {"role": "system", "content": sofia},
        {"role": "user", "content": user_content}
    ]
    response = send_message_to_openai(messages)
    
    return response

def get_position_names(spread_name):
    with open('spreads.json', 'r') as f:
        spreads = json.load(f)
    
    if spread_name in spreads.keys():  # Change this line
        return spreads[spread_name]
    else:
        raise ValueError(f"Spread '{spread_name}' not found.")


def get_spread_name(spread_choice):
    spread_names = {
        "1": "celtic_cross",
        # Add more spread choices and their names here
    }

    spread_name = spread_names.get(spread_choice)
    return spread_name
