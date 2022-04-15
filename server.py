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
      "next_state": "100",
   }, 
   "100": {
      "action": "set_text",
      "text": " Because Player 2 took the last trick, they lead the next trick by playing a card.",
      "next_state": "110",
   },
   "110": {
      "action": "continue", 
      "next_state": "120",
   },
   "120": {
      "action": "clear_text", 
      "next_state": "130"
   },
   "130": {
      "action": "play_card",
      "card": ("7", "s"),
      "next_state": "140"
   },
   "140": {
      "action": "play_card", 
      "card": ("3", "s"),
      "next_state": "150"
   },
   "150": {
      "action": "set_text",
      "text": "Now you have to play. Because spades (♠) were led, you must follow suit by playing a spade. Play your jack (J♠)",
      "next_state": "160"
   },
   "160": {
      "action": "click_card",
      "card": ("J", "s"),
      "next_state": "170"
   },
    "170": {
      "action": "play_card",
      "card": ("J", "s"),
      "next_state": "180"
   },
    "180": {
      "action": "clear_text",
      "next_state": "190"
   },
   "190": {
      "action": "play_card",
      "card": ("A", "h"),
      "next_state": "200"
   },
     "200": {
      "action": "set_text",
      "text": " What’s this? Player 1 was void in spades, so they could not follow suit. They got to play any card.",
      "next_state": "210"
   },
    "210": {
      "action": "continue",
      "next_state": "220"
   },
    "220": {
      "action": "clear_text",
      "next_state": "230"
   },
    "230": {
      "action": "set_text",
      "text": " Even though Player 1’s card is highest, they did not follow suit. You have the highest card in suit, so you take this trick.",
      "next_state": "240"
   },
   "240": {
      "action": "continue",
      "next_state": "250"
   },
   "250": {
      "action": "take_trick",
      "next_state": "270"
   },
   "270": {
      "action": "clear_text",
      "next_state": "280"
   },
    "280": {
      "action": "set_text",
      "text": "It looks like you took a heart in that last trick.In Hearts, you want to avoid taking points.Each heart is worth one point.",
      "next_state": "290"
   },
   "290": {
      "action": "continue",
      "next_state": "300"
   },
     "300": {
      "action": "clear_text",
      "next_state": "310"
   },
    "310": {
      "action": "set_text",
      "text": "The other card that gives points is the queen of spades (Q♠) which is worth 13 points.You have the queen in your hand, so let’s see if we can make someone else take it.",
      "next_state": "320",
   },
   "320": {
      "action": "continue",
      "next_state": "330",
   },
    "330": {
      "action": "clear_text",
      "next_state": "340",
   },
     "340": {
      "action": "set_text",
      "text": "It’s your lead! Try leading the four of diamonds (4♦)",
      "next_state": "350",
   },
    "350": {
      "action": "click_card",
      "card": ("4", "d"),
      "next_state": "360",
   },
    "360": {
      "action": "play_card",
      "card": ("4", "d"),
      "next_state": "370",
   },
    "370": {
      "action": "play_card",
      "card": ("A", "d"),
      "next_state": "380",
   },
   "380": {
      "action": "play_card",
      "card": ("7", "d"),
      "next_state": "390",
   },
    "390": {
      "action": "play_card",
      "card": ("9", "d"),
      "next_state": "400",
   },
   "400": {
      "action": "set_text",
      "text": "Each player, moving clockwise, plays a card. Player 1 has the highest card, so they take the trick",
      "next_state": "410",
   },
    "410": {
      "action": "continue",
      "next_state": "420",
   },
    "420": {
      "action": "take_trick",
      "next_state": "430",
   }, 
      "430": {
      "action": "clear_text",
      "next_state": "440",
   },
   "440": {
      "action": "play_card",
      "card": ("Q", "d"),
      "next_state": "450",
   },
     "450": {
      "action": "play_card",
      "card": ("3", "d"),
      "next_state": "460",
   }, 
   "460": {
      "action": "play_card",
      "card": ("8", "d"),
      "next_state": "470",
   }, 
    "470": {
      "action": "set_text",
      "text": "Player 1 led diamonds again. But the four was your last diamond, so you are now void! You should play the queen of spades.",
      "next_state": "480",
   }, 
    "480": {
      "action": "click_card",
      "card": ("Q", "s"),
      "next_state": "490",
   }, 
     "490": {
      "action": "play_card",
      "card": ("Q", "s"),
      "next_state": "500",
   },
    "500": {
      "action": "clear_text",
      "next_state": "510",
   }, 
   "510": {
      "action": "set_text",
      "text": "Player 1 takes the trick and 13 points. That’ll show them!",
      "next_state": "520"
   }, 
    "520": {
      "action": "continue",
      "next_state": "530"
   }, 
   "530": {
      "action": "take_trick", 
      "next_state": "540"
   },
   "540": {
      "action": "clear_text", 
      "next_state" : "550"
   },
   "550": {
      "action": "clear_screen", 
      "next_state": "done", 
   },



   
   
   

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
