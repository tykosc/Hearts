from ctypes.wintypes import HGDIOBJ
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from itsdangerous import json
from copy import deepcopy
app = Flask(__name__)

from learn import *

# stores the answer to an active question, if necessary
answer = {}

time_entered_page = []

quiz_answers = []

# ROUTES

@app.route('/')
def home():
   return render_template('main_page.html')   

@app.route('/learn')
def learn():
   return render_template('game.html', init=learn_init)

# AJAX ROUTES
def preprocess(state):
   if state["action"] == "mc_question":
      state = deepcopy(state)
      answer["correct"] = state["correct"]
      state["correct"] = None
      answer["explanation"] = state["explanation"]
      state["explanation"] = None
   return state

@app.route('/fetch_state', methods=["POST"])
def fetch_state():
   req = request.get_json()

   return jsonify(preprocess(lesson_states[req]))

@app.route('/submit_mc_answer', methods=["POST"])
def submit_mc_answer():
   ans = request.get_json()
   return jsonify(answer)

def numeric_rank(rank):
   if rank == "A":
      return 14
   elif rank == "K":
      return 13
   elif rank == "Q":
      return 12
   elif rank == "J":
      return 11
   else:
      return int(rank)

@app.route('/submit_trick_answer', methods=["POST"])
def submit_trick_answer():
   ans = request.get_json()

   # determine correct answer
   played = ans['played']
   led = ans['led']
   suit_led = played[led][1]
   highest = 0

   answer = {
      "explanation": "",
      "correct": "0",
   }

   for idx, card in enumerate(played):
      if card[1] != suit_led:
         continue
      n = numeric_rank(card[0])
      if n > highest:
         highest = n
         answer["correct"] = str(idx)

   return jsonify(answer)

def can_lead(card, start, hearts_broken):
   if start:
      return card[0] == "2" and card[1] == "c"
   else:
      return hearts_broken or card[1] != "h"

def can_play(card, led_suit, void):
   if void:
      return True
   else:
      return card[1] == led_suit

@app.route('/submit_play_answer', methods=["POST"])
def submit_play_answer():
   ans = request.get_json()

   # determine correct answer
   hand = ans['hand']
   played = ans['played']
   played_count = 0
   for p in played:
      if p is not None:
         played_count += 1
   lead_index = (4 - played_count) % 4
   
   answer = {
      "explanation": "",
   }
   if lead_index == 0:
      answer["correct"] = list(map(lambda card : can_lead(card, len(hand) == 13, ans['hearts_broken']), hand))
   else:
      void = True
      led_suit = played[lead_index][1]
      for c in hand:
         if c[1] == led_suit:
            void = False
            break
      answer["correct"] = list(map(lambda card : can_play(card, led_suit, void), hand))

   return jsonify(answer)

if __name__ == '__main__':
   app.run(debug = True)
