from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from itsdangerous import json
app = Flask(__name__)

from learn import *

# stores the answer to an active question
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
      answer["correct"] = state["correct"]
      state["correct"] = None
      answer["explanation"] = state["explanation"]
      state["explanation"] = None
   return state

@app.route('/fetch_state', methods=["POST"])
def fetch_state():
   req = request.get_json()

   return jsonify(preprocess(lesson_states[req]))

@app.route('/submit_answer', methods=["POST"])
def submit_answer():
   ans = request.get_json()
   return jsonify(answer)

if __name__ == '__main__':
   app.run(debug = True)
