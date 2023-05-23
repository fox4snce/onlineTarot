import concurrent.futures
from flask import Flask, request, jsonify
import json
import random
from datetime import datetime
from tarot import (
    ask_for_card,
    get_spread_name,
    send_message,
    save_reading,
)

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/reading', methods=['POST'])
def get_reading():
    data = request.json

    user_name = data.get('user_name', '')
    question = data.get('question', '')
    spread_choice = data.get('spread_choice', '1')

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"{timestamp}_{user_name if user_name else 'reading'}"

    if spread_choice == "1" or spread_choice == "":
        spread_size = 10
    else:
        print("Invalid spread choice. Defaulting to Celtic Cross.")
        spread_size = 10

    hand = data.get('hand', [])

    info = {
        "name": user_name,
        "question": question,
        "spread": get_spread_name(spread_choice),
        "cards": [(card[0], card[1]) for card in hand]
    }

    spread = {}

    # Create a ThreadPoolExecutor. The number of workers should be adjusted based on your API rate limit.
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # For each card in the hand, start a new thread to interpret it.
        future_to_interpretation = {executor.submit(ask_for_card, position, card, orientation, get_spread_name(spread_choice), question): position for position, (card, orientation) in enumerate(hand, start=1)}
        for future in concurrent.futures.as_completed(future_to_interpretation):
            position = future_to_interpretation[future]
            try:
                _, card, orientation, interpretation = future.result()
            except Exception as exc:
                print(f"Generated an exception: {exc}")
            else:
                spread[position] = {"card": card, "orientation": orientation, "interpretation": interpretation}

    overall_interpretation = send_message(f"Given the current spread: {spread} Interpret the entire spread as a whole.")

    return jsonify({
        'overall_interpretation': overall_interpretation,
        'individual_interpretations': spread
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
