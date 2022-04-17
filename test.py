# States for the 'test' section

test_init = {
   # The cards in your hand (probably 13)
   "your_hand": [("2", "c"), ("3", "c"), ("7", "c"), ("6", "d"), ("8", "d"), ("10", "d"), ("A", "d"), ("3", "h"), ("5", "h"), ("K", "h"), ("5", "s"), ("10", "s"), ("J", "s")],
   # The currently played cards
   "played_cards": [None, None, None, None],
   # The number of points taken by each player
   "points": [0,0,0,0],
   # Have hearts been broken?
   "hearts_broken": False,
   # The current player (0 = you, then 1, 2, 3)
   "current_player": "0",
   # Mode
   "mode": "test",
   # The start state
   "start_state": "0005",
}

test_states = {
    "0005": {
        "action": "play_question",
        "next_state": "0010"
    },
    "0010": {
        "action": "play_card",
        "card": ("2", "c"),
        "next_state": "0020"
    },
    "0020": {
        "action": "play_card",
        "card": ("Q", "c"),
        "next_state": "0030"
    },
    "0030": {
        "action": "play_card",
        "card": ("A", "c"),
        "next_state": "0040"
    },
    "0040": {
        "action": "play_card",
        "card": ("K", "c"),
        "next_state": "0050"
    },
    "0050": {
        "action": "trick_question",
        "next_state": "0060"
    },
    "0060": {
        "action": "take_trick",
        "next_state": "0110"
    },
    
    "0110": {
        "action": "play_card",
        "card": ("9", "s"),
        "next_state": "0120"
    },
    "0120": {
        "action": "play_card",
        "card": ("6", "s"),
        "next_state": "0125"
    },
    "0125": {
        "action": "play_question",
        "next_state": "0130",
    },
    "0130": {
        "action": "play_card",
        "card": ("J", "s"),
        "next_state": "0140"
    },
    "0140": {
        "action": "play_card",
        "card": ("K", "s"),
        "next_state": "0145"
    },
    "0145": {
        "action": "mc_question",
        "prompt": "Why is playing the king of spades advantageous for player 1?",
        "choices": ["They want to take a trick with the king and may not be able to do it later", "They want to take the jack of spades you played", "They want to avoid having to take the queen of spades", "They want to lead hearts on the next trick"],
        "correct": "2",
        "explanation": "Because player 1 played the last card, they know that they aren't risking taking the queen. If they kept the king, they might be forced to take the queen later on.",
        "next_state": "0150"
    },
    "0150": {
        "action": "trick_question",
        "next_state": "0160"
    },
    "0160": {
        "action": "take_trick",
        "next_state": "0210"
    },

    "0210": {
        "action": "play_card",
        "card": ("J", "d"),
        "next_state": "0220"
    },
    "0220": {
        "action": "play_card",
        "card": ("K", "d"),
        "next_state": "0230"
    },
    "0230": {
        "action": "play_card",
        "card": ("9", "d"),
        "next_state": "0235"
    },
    "0235": {
        "action": "play_question",
        "next_state": "0240",
    },
    "0240": {
        "action": "play_card",
        "card": ("A", "d"),
        "next_state": "0250"
    },
    "0250": {
        "action": "trick_question",
        "next_state": "0260"
    },
    "0260": {
        "action": "take_trick",
        "next_state": "0305"
    },

    "0305": {
        "action": "play_question",
        "next_state": "0310"
    },
    "0310": {
        "action": "play_card",
        "card": ("3", "c"),
        "next_state": "0320"
    },
    "0320": {
        "action": "play_card",
        "card": ("A", "h"),
        "next_state": "0315"
    },
    "0315": {
        "action": "mc_question",
        "prompt": "What can we determine about the cards in player 1's hand?",
        "choices": ["They only have hearts", "They have no clubs", "They only have clubs higher than the 3", "The ace is their only heart"],
        "correct": "1",
        "explanation": "Because they didn't follow suit, they must be void in clubs.",
        "next_state": "0330"
    },
    "0330": {
        "action": "play_card",
        "card": ("5", "c"),
        "next_state": "0340"
    },
    "0340": {
        "action": "play_card",
        "card": ("4", "c"),
        "next_state": "0350"
    },
    "0350": {
        "action": "trick_question",
        "next_state": "0360"
    },
    "0360": {
        "action": "take_trick",
        "next_state": "0410"
    },

    "0410": {
        "action": "play_card",
        "card": ("2", "s"),
        "next_state": "0420"
    },
    "0420": {
        "action": "play_card",
        "card": ("A", "s"),
        "next_state": "0425"
    },
    "0425": {
        "action": "mc_question",
        "prompt": "Which of the following NOT a reasonable possibility regarding player 3:",
        "choices": ["They only had one spade, and had to play it", "They only had the ace and queen of spades", "They have many spades, including the queen", "They want to shoot the moon"],
        "correct": "3",
        "explanation": "Unless they have the queen, playing the ace was likely forced. They definitely can't shoot the moon because player 2 took a heart.",
        "next_state": "0435"
    },
    "0435": {
        "action": "play_question",
        "next_state": "0430"
    },
    "0430": {
        "action": "play_card",
        "card": ("10", "s"),
        "next_state": "0440"
    },
    "0440": {
        "action": "play_card",
        "card": ("8", "s"),
        "next_state": "0445"
    },
    "0445": {
        "action": "mc_question",
        "prompt": "Assuming they are playing optimally, is it likely that player 1 has the queen of spades?",
        "choices": ["Yes, but they want to give it to player 2", "Yes, but they want to take it themselves", "No, because otherwise they would've played it", "No, because player 2 definitely has the queen"],
        "correct": "2",
        "explanation": "Giving the queen to player 3 would be optimal if they had it in hand, because it makes it less likely that player 1 is forced to take it.",
        "next_state": "0450"
    },
    "0450": {
        "action": "trick_question",
        "next_state": "0460"
    },
    "0460": {
        "action": "take_trick",
        "next_state": "0510"
    },


    "0510": {
        "action": "play_card",
        "card": ("2", "h"),
        "next_state": "0512"
    },
    "0512": {
        "action": "mc_question",
        "prompt": "Why was player 3 able to lead hearts?",
        "choices": ["Because hearts were broken", "No reason, it is always allowed", "Because it is not the first trick", "Because they are currently breaking hearts"],
        "correct": "0",
        "explanation": "Hearts were broken when player 2 took a heart, so hearts can be led.",
        "next_state": "0515"
    },
    "0515": {
        "action": "play_question",
        "next_state": "0520"
    },
    "0520": {
        "action": "play_card",
        "card": ("3", "h"),
        "next_state": "0530"
    },
    "0530": {
        "action": "play_card",
        "card": ("4", "h"),
        "next_state": "0540"
    },
    "0540": {
        "action": "play_card",
        "card": ("Q", "h"),
        "next_state": "0550"
    },
    "0550": {
        "action": "trick_question",
        "next_state": "0560"
    },
    "0560": {
        "action": "take_trick",
        "next_state": "0610"
    },


    "0610": {
        "action": "play_card",
        "card": ("Q", "d"),
        "next_state": "0620"
    },
    "0620": {
        "action": "play_card",
        "card": ("Q", "s"),
        "next_state": "0625"
    },
    "0625": {
        "action": "play_question",
        "next_state": "0630"
    },
    "0630": {
        "action": "play_card",
        "card": ("10", "d"),
        "next_state": "0640"
    },
    "0640": {
        "action": "play_card",
        "card": ("7", "d"),
        "next_state": "0650"
    },
    "0650": {
        "action": "trick_question",
        "next_state": "0660"
    },
    "0660": {
        "action": "take_trick",
        "next_state": "0710"
    },


    "0710": {
        "action": "play_card",
        "card": ("J", "c"),
        "next_state": "0720"
    },
    "0720": {
        "action": "play_card",
        "card": ("6", "c"),
        "next_state": "0725"
    },
    "0725": {
        "action": "play_question",
        "next_state": "0730"
    },
    "0730": {
        "action": "play_card",
        "card": ("7", "c"),
        "next_state": "0740"
    },
    "0740": {
        "action": "play_card",
        "card": ("3", "s"),
        "next_state": "0745"
    },
    "0745": {
        "action": "mc_question",
        "prompt": "Often, when people are void, they take the opportunity to play a heart. Assuming they are playing optimally, is it possible that player 1 had a heart and chose not to play it?",
        "choices": ["Yes", "No"],
        "correct": "0",
        "explanation": "Only player 2 has taken points, so player 1 might be worried that they are trying to shoot the moon. If so, they wouldn't want to play a heart here.",
        "next_state": "0750"
    },
    "0750": {
        "action": "trick_question",
        "next_state": "0760"
    },
    "0760": {
        "action": "take_trick",
        "next_state": "0810"
    },


    "0810": {
        "action": "play_card",
        "card": ("10", "c"),
        "next_state": "0820"
    },
    "0820": {
        "action": "play_card",
        "card": ("8", "c"),
        "next_state": "0825"
    },
    "0825": {
        "action": "play_question",
        "next_state": "0830"
    },
    "0830": {
        "action": "play_card",
        "card": ("5", "s"),
        "next_state": "0840"
    },
    "0840": {
        "action": "play_card",
        "card": ("2", "d"),
        "next_state": "0850"
    },
    "0850": {
        "action": "trick_question",
        "next_state": "0860"
    },
    "0860": {
        "action": "take_trick",
        "next_state": "0910"
    },


    "0910": {
        "action": "play_card",
        "card": ("J", "h"),
        "next_state": "0920"
    },
    "0920": {
        "action": "play_card",
        "card": ("6", "h"),
        "next_state": "0925"
    },
    "0925": {
        "action": "play_question",
        "next_state": "0927"
    },
    "0927": {
        "action": "mc_question",
        "prompt": "Why might playing the king of hearts be the best move?",
        "choices": ["It means we take at least three hearts, which means we're beating players 1 and 3", "It makes it impossible for player 2 to shoot the moon", "It makes it possible for us to shoot the moon", "There is no reason, we should play the five to avoid taking the trick"],
        "correct": "1",
        "explanation": "Taking a hearts trick is usually not good, but the benefits of preventing player 2 from shooting are high.",
        "next_state": "0930"
    },
    "0930": {
        "action": "play_card",
        "card": ("K", "h"),
        "next_state": "0940"
    },
    "0940": {
        "action": "play_card",
        "card": ("7", "s"),
        "next_state": "0950"
    },
    "0950": {
        "action": "trick_question",
        "next_state": "0960"
    },
    "0960": {
        "action": "take_trick",
        "next_state": "1005"
    },

    "1005": {
        "action": "play_question",
        "next_state": "1010"
    },
    "1010": {
        "action": "play_card",
        "card": ("5", "h"),
        "next_state": "1020"
    },
    "1020": {
        "action": "play_card",
        "card": ("5", "d"),
        "next_state": "1030"
    },
    "1030": {
        "action": "play_card",
        "card": ("8", "h"),
        "next_state": "1040"
    },
    "1040": {
        "action": "play_card",
        "card": ("7", "h"),
        "next_state": "1050"
    },
    "1050": {
        "action": "trick_question",
        "next_state": "1060"
    },
    "1060": {
        "action": "take_trick",
        "next_state": "1110"
    },


    "1110": {
        "action": "play_card",
        "card": ("3", "d"),
        "next_state": "1120"
    },
    "1120": {
        "action": "play_card",
        "card": ("10", "h"),
        "next_state": "1125"
    },
    "1125": {
        "action": "play_question",
        "next_state": "1130"
    },
    "1130": {
        "action": "play_card",
        "card": ("6", "d"),
        "next_state": "1140"
    },
    "1140": {
        "action": "play_card",
        "card": ("4", "d"),
        "next_state": "1150"
    },
    "1150": {
        "action": "trick_question",
        "next_state": "1160"
    },
    "1160": {
        "action": "take_trick",
        "next_state": "1205"
    },

    "1205": {
        "action": "play_question",
        "next_state": "1210"
    },
    "1210": {
        "action": "play_card",
        "card": ("8", "d"),
        "next_state": "1220"
    },
    "1220": {
        "action": "play_card",
        "card": ("4", "s"),
        "next_state": "1230"
    },
    "1230": {
        "action": "play_card",
        "card": ("9", "h"),
        "next_state": "1240"
    },
    "1240": {
        "action": "play_card",
        "card": ("9", "c"),
        "next_state": "1250"
    },
    "1250": {
        "action": "trick_question",
        "next_state": "1260"
    },
    "1260": {
        "action": "take_trick",
        "next_state": "done"
    },
}