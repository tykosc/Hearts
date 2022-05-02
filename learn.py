# States for the 'learn' section

learn_init = {
   # The cards in your hand (probably 13)
   "your_hand": [("2", "c"), ("5", "c"), ("9", "c"), ("K", "c"), ("4", "d"), ("3", "h"), ("8", "h"), ("10", "h"), ("J", "h"), ("3", "s"), ("6", "s"), ("J", "s"), ("Q", "s")],
   # The currently played cards
   "played_cards": [None, None, None, None],
   # The number of points taken by each player
   "points": [0,0,0,0],
   # Have hearts been broken?
   "hearts_broken": False,
   # The current player (0 = you, then 1, 2, 3)
   "current_player": "0",
   # Mode
   "mode": "learn",
   # The start state
   "start_state": "0",
   # How to count steps/questions
   "step_name": "Step",
   "step_count": "auto",
} 

### ACTIONS ###
# format:
# action_name (parameter_names, ...)

# set_hand (hand)
# re-deals the user with the given hand

# set_played (played_cards)
# sets the currently played cards

# set_points (points)
# sets the current points

# set_current_player (current_player)
# sets the current_player field

# set_hearts_broken (hearts_broken)
# sets hearts_broken

# clear_game ()
# equivalent to set_hand([]), set_played([null, null, null, null]), set_points([0,0,0,0]), set_current_player(0), set_hearts_broken(false)

# set_text (text)
# sets the display text to "text"

# clear_text ()
# clears the display text

# click_card (card, show_select)
# waits for the given card to be clicked
# if show_select is true, show only the given card as selectable. otherwise shows all cards in hand as selectable

# continue ()
# adds a continue button and waits for it to be clicked

# play_card (card)
# makes the current_player play the given card, and advances current_player 

# take_trick ()
# gives the current trick to whoever won, and updates their points

# mc_question (prompt, choices, correct, explanation)
# prompts a multiple choice question. Choices is an array of possible choices, correct is the index of the correct one.

lesson_states = {
   "0": {
      "action": "set_text",
      "text": "In Hearts, each round (a trick) consists of each player playing one card. The first trick always starts with the two of clubs (♣️). You have this card, so click on it to play it!",
      "next_state": "10",
   },
   "10": {
      "action": "click_card",
      "card": ("2", "c"),
      "show_select": True,
      "next_state": "15",
   },
   "15": {
      "action": "step",
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
      "action": "continue_step",
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
      "action": "continue_step", 
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
      "card": ("4", "s"),
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
      "show_select": True,
      "next_state": "165",
   },
   "165": {
      "action": "step",
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
      "action": "continue_step",
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
      "action": "continue_step",
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
      "action": "continue_step",
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
      "action": "continue_step",
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
      "show_select": True,
      "next_state": "355",
   },
   "355": {
      "action": "step",
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
      "action": "continue_step",
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
      "show_select": True,
      "next_state": "485",
   },
   "485": {
      "action": "step",
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
      "action": "take_trick", 
      "next_state": "530"
   },
     "530": {
      "action": "continue_step",
      "next_state": "540"
   }, 
   "540": {
      "action": "clear_text", 
      "next_state" : "560"
   },
    "560": {
      "action": "set_text", 
      "text": " The round ends once everyone has played all of their cards, so after 13 tricks in a four-player game.",
      "next_state": "570"
   },
     "570": {
      "action": "set_text", 
      "text": "After each round, you add your points to your points from previous rounds. The game ends when any player reaches some point threshold at the end of a round (e.g., 50 points). Then, the player with the fewest points wins!",
      "next_state": "580"
   },
     "580": {
      "action": "continue_step", 
      "next_state": "590"
   },
    "590": {
      "action": "clear_text", 
      "next_state": "600"
   },
    "600": {
      "action": "set_text", 
      "text": " You’re almost ready to play! There are just a few extra rules to cover.",
      "next_state": "610"
   },
     "610": {
      "action": "continue_step", 
      "next_state": "615"
   },

   "615":{
      "action": "clear_text", 
      "next_state": "616"
   },
   "616": {
      "action": "clear_game",
      "next_state": "620"
   },
   "620": {
      "action": "set_text",
      "text": "The first round is safe. That means no player can play a heart or the queen of spades, even if they are void in clubs.",
      "next_state": "630",
   },
   "630": {
      "action": "continue",
      "next_state": "640"
   },
   "640": {
      "action": "set_hand",
      "hand": [("3", "d"), ("Q", "s"), ("2", "h"), ("3", "h"), ("4", "h"), ("5", "h"), ("7", "h"), ("8", "h"), ("10", "h"), ("J", "h"), ("Q", "h"), ("K", "h"), ("A", "h")],
      "next_state": "650"
   },
   "650": {
      "action": "set_current_player",
      "current_player": "1",
      "next_state": "660"
   },
   "660": {
      "action": "play_card",
      "card": ("2", "c"),
      "next_state": "670"
   },
   "670": {
      "action": "play_card",
      "card": ("A", "c"),
      "next_state": "680"
   },
   "680": {
      "action": "play_card",
      "card": ("K", "c"),
      "next_state": "690"
   },
   "690": {
      "action": "set_text",
      "text": "The first round is safe. That means no player can play a heart or the queen of spades, even if they are void in clubs. With this in mind, click on the card you could play in this (very farfetched) opening hand.",
      "next_state": "700"
   },
   "700": {
      "action": "click_card",
      "card": ("3", "d"),
      "show_select": False,
      "next_state": "710",
   },
   "710": {
      "action": "play_card",
      "card": ("3", "d"),
      "next_state": "720"
   },
   "720": {
      "action": "set_text",
      "text": "Great! Only the three of diamonds was playable. Did you notice that players 2 and 3 took this opportunity to ditch their high clubs?",
      "next_state": "730"
   },
   "730": {
      "action": "continue_step",
      "next_state": "740"
   },
   "740": {
      "action": "clear_text",
      "next_state": "750"
   },
   "750": {
      "action": "clear_game",
      "next_state": "760"
   },
   "760": {
      "action": "set_text",
      "text": 'Hearts cannot be led until hearts have been "broken." Hearts are broken once someone has played a card on trick. Playing the queen of spades does not count as breaking hearts.',
      "next_state": "765"
   },
   "765": {
      "action": "continue",
      "next_state": "770"
   },
   "770": {
      "action": "set_points",
      "points": [0, 13, 0, 0],
      "next_state": "780"
   },
   "780": {
      "action": "set_hand",
      "hand": [("8", "s"), ("3", "h"), ("7", "h"), ("J", "h")],
      "next_state": "790"
   },
   "790": {
      "action": "set_current_player",
      "current_player": "0",
      "next_state": "800"
   },
   "800": {
      "action": "set_text",
      "text": 'Hearts cannot be led until hearts have been "broken." Hearts are broken once someone has played a card on trick. Playing the queen of spades does not count as breaking hearts. With this in mind, click on the card that you could lead in this position. (Check the current points: how do we know if hearts have been broken?)',
      "next_state": "810"
   },
   "810": {
      "action": "click_card",
      "card": ("8", "s"),
      "show_select": False,
      "next_state": "820"
   },
   "820": {
      "action": "play_card",
      "card": ("8", "s"),
      "next_state": "830"
   },
   "830": {
      "action": "set_text",
      "text": "Great! Notice that if you had the lead for the next trick, you would be allowed to lead a heart because you had no other choice.",
      "next_state": "840"
   },
   "840": {
      "action": "continue_step",
      "next_state": "850"
   },
   "850": {
      "action": "clear_text",
      "next_state": "860"
   },
   "860": {
      "action": "clear_game",
      "next_state": "870"
   },
   "870": {
      "action": "set_text",
      "text": "In very rare cases, you might find it is possible to take all 26 points: thirteen hearts and the queen of spades. This is called shooting the moon.",
      "next_state": "880"
   },
   "880": {
      "action": "continue",
      "next_state": "890"
   },
   "890": {
      "action": "set_hand",
      "hand": [("3", "c"), ("A", "h")],
      "next_state": "900"
   },
   "900": {
      "action": "set_points",
      "points": [22, 0, 0, 0],
      "next_state": "910"
   },
   "910": {
      "action": "set_text",
      "text": "It looks like you've taken most of the points so far... Playing the 3 of clubs would be an easy way to avoid taking any more points, but let's see what happens if we lead the ace instead.",
      "next_state": "920"
   },
   "920": {
      "action": "click_card",
      "card": ("A", "h"),
      "show_select": True,
      "next_state": "930"
   },
   "930": {
      "action": "play_card",
      "card": ("A", "h"),
      "next_state": "940"
   },
   "940": {
      "action": "play_card",
      "card": ("Q", "h"),
      "next_state": "950"
   },
   "950": {
      "action": "play_card",
      "card": ("9", "h"),
      "next_state": "960"
   },
   "960": {
      "action": "play_card",
      "card": ("J", "h"),
      "next_state": "970"
   },
   "970": {
      "action": "take_trick",
      "next_state": "980"
   },
   "980": {
      "action": "set_text",
      "text": "Take another look at your points: instead of being at 26 points, you are now at zero and all of your opponents are at 26! This is what happens when you shoot the moon. It's a risky strategy, but with a huge payoff!",
      "next_state": "990"
   },
   "990": {
      "action": "continue_step",
      "next_state": "1000"
   },
   "1000": {
      "action": "set_text",
      "text": "You're now ready to play! But why don't you test your knowledge first?",
      "next_state": "1010"
   },
   "1010": {
      "action": "test_me",
      "next_state": "done"
   }
}