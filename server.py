from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)

# played_cards represents the cards in order of player 1, 2, 3, 4 (you are 4).  When a card doesn't exist for a player, there is None instead of the card tuple

# cards are represented as tuples of strings, with the first entry 1-10 or J Q K A, and the second entry c, d, s, or h for clubs, diamonds, spades, hearts

# your_hand has max size of seven cards, but can be smaller if cards are removed from your hand.

# num_points is the number of hearts/points each player has for a given lesson

#clickable_card is None if none of the cards are clickable to reach the next page, otherwise, it is the index of the card that is clickable

#continue is None if there is no continue button (this means that a card is clickable) or it is 1 if there is a continue button to advance to the next page

lessons = {
   "1": {
      "lesson_id": "1",
      "text": "In Hearts, each round (a trick) consists of each player playing one card. The first trick always starts with the two of clubs (♣️). You have this card, so click on it to play it!",
      "played_cards": [None, None, None, None],
      "your_hand": [("2", "c"),("4", "d"), ("Q", "s"), ("10", "h"),("J", "s"), ("3", "s"), ("8", "h")],
      "num_points": [0,0,0,0],
      "continue": None, 
      "clickable_card": 0,
      "next_lesson": "2"
   },
    "2": {
      "lesson_id": "2",
      "text": "Each player, moving clockwise, plays a card. Player 2 has the highest card, so they take the trick.",
      "played_cards": [("J", "c"), ("A", "c"), ("Q", "c"), ("2", "c")],
      "your_hand": [("4", "d"), ("Q", "s"), ("10", "h"),("J", "s"), ("3", "s"), ("8", "h")],
      "num_points": [0,0,0,0],
      "continue": "1",
      "clickable_card": None, 
      "next_lesson": "3",
   }, 
   "3": {
      "lesson_id": "3",
      "text": "Because Player 2 took the last trick, they lead the next trick by playing a card",
      "played_cards": [None, ("7", "s"), ("3", "s"), None],
      "your_hand": [("4", "d"), ("Q", "s"), ("10", "h"),("J", "s"), ("3", "s"), ("8", "h")],
      "num_points": [0,0,0,0],
      "continue": "1",
      "clickable_card": None, 
      "next_lesson": "4"
   },
     "4": {
      "lesson_id": "3",
      "text": "Now you have to play. Because spades (♠️) were led, you must follow suit by playing a spade. Play your jack (J♠️)",
      "played_cards": [None, ("7", "s"), ("3", "s"), None],
      "your_hand": [("4", "d"), ("Q", "s"), ("10", "h"),("J", "s"), ("3", "s"), ("8", "h")],
      "continue": None,
      "clickable_card": 3, 
      "num_points": [0,0,0,0],
      "next_lesson": "5"
   },
   "5": {
      "lesson_id": "5",
      "text": "What’s this? Player 1 was void in spades, so they could not follow suit. They got to play any card.",
      "played_cards": [("A", "h"), ("7", "s"), ("3", "s"), ("J", "s")],
      "your_hand": [("4", "d"), ("Q", "s"), ("10", "h"), ("3", "s"), ("8", "h")],
      "num_points": [0,0,0,0],
      "continue": "1",
      "clickable_card": None, 
      "next_lesson": "6"
   },
      "6": {
      "lesson_id": "6",
      "text": "Even though Player 1’s card is highest, they did not follow suit. You have the highest card in suit, so you take this trick.",
      "played_cards": [("A", "h"), ("7", "s"), ("3", "s"), ("J", "s")],
      "your_hand": [("4", "d"), ("Q", "s"), ("10", "h"), ("3", "s"), ("8", "h")],
      "num_points": [0,0,0,0],
      "continue": "1",
      "clickable_card": None, 
      "next_lesson": "7"
   },
       "7": {
      "lesson_id": "7",
      "text": "It looks like you took a heart in that last trick. In Hearts, you want to avoid taking points. Each heart is worth one point.",
      "played_cards": [None, None, None, None],
      "your_hand": [("4", "d"), ("Q", "s"), ("10", "h"), ("3", "s"), ("8", "h")],
      "num_points": [0,0,0,1],
      "continue": "1",
      "clickable_card": None, 
      "next_lesson": "8"
   },
      "8": {
      "lesson_id": "8",
      "text": "The other card that gives points is the queen of spades (Q♠️) which is worth 13 points.You have the queen in your hand, so let’s see if we can make someone else take it.",
      "played_cards": [None, None, None, None],
      "your_hand": [("4", "d"), ("Q", "s"), ("10", "h"), ("3", "s"), ("8", "h")],
      "num_points": [0,0,0,1],
      "continue": "1",
      "clickable_card": None, 
      "next_lesson": "9"
   },
     "9": {
      "lesson_id": "9",
      "text": "It’s your lead! Try leading the four of diamonds (4♦️)",
      "played_cards": [None, None, None, None],
      "your_hand": [("4", "d"), ("Q", "s"), ("10", "h"), ("3", "s"), ("8", "h")],
      "num_points": [0,0,0,1],
      "continue": None,
      "clickable_card": 0, 
      "next_lesson": "10"
   },
    "10": {
      "lesson_id": "10",
      "text": "Each player, moving clockwise, plays a card. Player 1 has the highest card, so they take the trick.",
      "played_cards": [("A", "d"), ("7", "d"), ("9", "d"), ("4", "d")],
      "your_hand": [("Q", "s"), ("10", "h"), ("3", "s"), ("8", "h")],
      "num_points": [0,0,0,1],
      "continue": "1",
      "clickable_card": None, 
      "next_lesson": "11"
   },
    "11": {
      "lesson_id": "11",
      "text": "Player 1 led diamonds again. But the four was your last diamond, so you are now void! You should play the queen of spades",
      "played_cards": [("Q", "d"), ("3", "d"), ("8", "d"), None],
      "your_hand": [("Q", "s"), ("10", "h"), ("3", "s"), ("8", "h")],
      "num_points": [0,0,0,1],
      "continue": None,
      "clickable_card": 0, 
      "next_lesson": "12"
   },
     "12": {
      "lesson_id": "12",
      "text": "Player 1 takes the trick and 13 points. That’ll show them!",
      "played_cards": [("Q", "d"), ("3", "d"), ("8", "d"), ("Q", "s")],
      "your_hand": [("10", "h"), ("3", "s"), ("8", "h")],
      "num_points": [13,0,0,1],
      "continue": "1",
      "clickable_card": None, 
      "next_lesson": "end"
   },
   
}

time_entered_page = []

quiz_answers = []


# ROUTES

@app.route('/')
def home():
   return render_template('main_page.html')   

@app.route('/learn/<lesson_id>')
def learn(lesson_id):
   lesson = lessons[lesson_id]
   return render_template('learn.html', lesson=lesson)

if __name__ == '__main__':
   app.run(debug = True)
