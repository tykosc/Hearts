from crypt import methods
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from itsdangerous import json
app = Flask(__name__)

lesson_init = {
   # The cards in your hand (probably 13)
   "your_hand": [("2", "c"), ("4", "d"), ("Q", "s"), ("10", "h"),("J", "s"), ("3", "s"), ("8", "h")],
   # The currently played cards
   "played_cards": [None, None, None, None],
   # The number of points taken by each player
   "points": [0,0,0,0],
   # The current player (0 = you, then 1, 2, 3)
   "current_player": "0",
   # The start state
   "start_state": "0",
}

### ACTIONS ###
# format:
# action_name (parameter_names, ...)

# set_text (text)
# sets the display text to "text"

# click_card (card)
# waits for the given card to be clicked

# play_card (card)
# makes the current_player play the given card, and advances current_player 

lesson_states = {
   "0": {
      "action": "set_text",
      "text": "In Hearts, each round (a trick) consists of each player playing one card. The first trick always starts with the two of clubs (♣️). You have this card, so click on it to play it!",
      "next_state": "10",
   },
   "10": {
      "action": "click_card",
      "card": ("2", "c"),
      "next_state": "20",
   },
   "20": {
      "action": "play_card",
      "card": ("2", "c"),
      "next_state": "30",
   },
   "30": {
      "action": "clear_text",
      "next_state": "40",
   },
   "40": {
      "action": "play_card",
      "card": ("J", "c"),
      "next_state": "50",
   },
   "50": {
      "action": "play_card",
      "card": ("A", "c"),
      "next_state": "60",
   },
   "60": {
      "action": "play_card",
      "card": ("Q", "c"),
      "next_state": "70",
   },
    "70": {
      "action": "set_text",
      "text": "Each player, moving clockwise, plays a card. Player 2 has the highest card, so they take the trick.",
      "next_state": "80",
   },
   "80": {
      "action": "continue",
      "next_state": "90"
   },
   "90": {
      "action": "take_trick",
      "text": "got here!",
      "next_state": "done",

   }
}

time_entered_page = []

quiz_answers = []


# ROUTES

@app.route('/')
def home():
   return render_template('main_page.html')   

@app.route('/learn')
def learn():
   return render_template('game.html', init=lesson_init)

# AJAX ROUTES
@app.route('/fetch_state', methods=["POST"])
def fetch_state():
   req = request.get_json()

   return jsonify(lesson_states[req])

if __name__ == '__main__':
   app.run(debug = True)
