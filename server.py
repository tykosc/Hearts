from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from copy import deepcopy
app = Flask(__name__)

from learn import *
from test import *
from util import *

#int of correct anwers from user in quiz
score = 0
play_score = 0
trick_score = 0
mc_score = 0


def reset_score():
   global score
   score = 0
   global play_score, trick_score, mc_score
   play_score = 0
   trick_score = 0
   mc_score = 0

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

@app.route('/choose_test')
def choose_test():
   return render_template('choose_test.html')

@app.route('/test/<difficulty>')
def test(difficulty):
   # reset the score
   reset_score()
   if difficulty == "1": 
      return render_template('game.html', init=test_init_1)
   else:
      return render_template('game.html', init=test_init_0)

@app.route('/rules')
def rules():
   return render_template('rules.html')

@app.route('/quiz_end/<difficulty>')
def quiz_end(difficulty):
   # resetting the score
   quiz_score = score
   quiz_t_score = trick_score
   quiz_p_score = play_score
   quiz_mc_score = mc_score
   reset_score()
   if difficulty == "1":
      num_questions = test_init_1["step_count"] 
   else: 
      num_questions = test_init_0["step_count"]

   if int(quiz_score) == int(num_questions):
      grade = "You got an A+ ! You're ready to kill it in Hearts!"
   elif (.9 * float(num_questions)) <= float(quiz_score) < float(num_questions):
      grade = "You got an A ! You're ready to go out and play!"
   elif (.8 * float(num_questions))<= float(quiz_score) < float(num_questions):
      grade = "You got a B ! You're ready to jump in a game of Hearts, but you might want some seasoned players to help along the way!"
   elif(.7 * float(num_questions))<= float(quiz_score) <float(num_questions):
      grade = "You got a C ! Not bad, but you might want to brush up on the rules."
   elif(.6 * float(num_questions))<= float(quiz_score) <float(num_questions):
      grade = "You got a D ! Don't feel bad, try again after brushing up on the rules."
   else:
      grade = "You failed the quiz, have you visited the Learn page yet?"
   return render_template('quiz_end.html', quiz_score = quiz_score, num_questions= num_questions, quiz_t_score = quiz_t_score, quiz_p_score = quiz_p_score, quiz_mc_score = quiz_mc_score, grade = grade)

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

   if req["mode"] == "learn":
      return jsonify(preprocess(lesson_states[req["next_state"]]))
   elif req["mode"] == "test_1":
      return jsonify(preprocess(test_states_1[req["next_state"]]))
   else:
      return jsonify(preprocess(test_states_0[req["next_state"]]))

@app.route('/submit_mc_answer', methods=["POST"])
def submit_mc_answer():
   ans = request.get_json()
   if ans == int(answer["correct"]):
      global score
      score = score + 1
      global mc_score 
      mc_score = mc_score + 1
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

   if int(ans["response"]) == int(answer["correct"]):
      global score
      score = score + 1
      global trick_score
      trick_score = trick_score + 1
      answer["explanation"] = 'Correct!'
   else:
      answer["explanation"] = "Incorrect. Correct cards are green."


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

   isRight = True
   for x in range(len(answer["correct"])):
      if answer["correct"][x] !=  ans["response"][x]:
         isRight = False


   if isRight:
      global score
      score  =  score + 1
      global play_score
      play_score = play_score + 1
      answer["explanation"] = "Correct!"
   else:
      answer["explanation"] = "Incorrect. Correct cards are green."
   

   return jsonify(answer)


if __name__ == '__main__':
   # initialize step counts
   learn_init["step_count"] = str(countSteps(lesson_states, learn_init["start_state"]))
   test_init_1["step_count"]  = str(countSteps(test_states_1,   test_init_1["start_state"]))
   test_init_0["step_count"]  = str(countSteps(test_states_0,   test_init_0["start_state"]))

   app.run(debug = True)
