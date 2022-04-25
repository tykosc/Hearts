// Shared .js file for all interactive displays

// Global variables
let your_hand = _init.your_hand                         // List of cards currently in your hand
let played_cards = _init.played_cards                   // For each player, a card if they have played one, otherwise null
let points = _init.points                               // For each player, their total points this round
let hearts_broken = _init.hearts_broken                 // Whether or not hearts have been broken
let current_player = parseInt(_init.current_player)     // The index of the current player (or who led the current trick if all four cards have been played)
let next_state = _init.start_state                      // The id of the next state
let mode = _init.mode                                   // "learn" or "test"
let state = {}                                          // The currently loaded state
let question = {}                                       // The currently loaded question, including the response, if any

let cardInHandCallback = null                           // What to do if a card in hand is clicked
let cardInPlayCallback = null                           // What to do if a card in play is clicked

let question_status = 1                         
let quiz_number = 1

function playerName(index) {
    if (index == 0) return "you"
    return `player ${index}`
}

/*** CARDS & ANIMATION ***/

let card_objects = []
let cards_animating = 0
let next_state_deferred = false

const card_width = 70.27
const card_height = 100

function findCardObject(rank, suit) {
    out_object = null
    card_objects.forEach(function(obj, _) {
        if (obj.rank == rank && obj.suit == suit) {
            out_object = obj
            return false //break
        }
    })
    return out_object
}

function playerCardOffset(who, card_div) {
    let points_div = $(`#player_name_${who}`)
    let pos = points_div.offset()
    return {top: pos.top + points_div.height() * 0.5 - card_height * 0.5, left: pos.left + points_div.width() * 0.5 - card_width * 0.5}
}

function createCardObject(rank, suit) {
    let card_div = $(`
        <img class="card-in-hand" style="margin:3px" src=
        "https://uid-playing-cards.s3.amazonaws.com/${rank.toLowerCase()}${suit.toLowerCase()}.png"></img>
        `)
        .css("position", "relative")
    return {
        rank: rank,
        suit: suit,
        div: card_div,
        start: playerCardOffset(current_player, card_div),
        autoanim: true
    }
}

function deleteCardObject(rank, suit) {
    del_object = null
    del_index = 0
    card_objects.forEach(function(obj, idx) {
        if (obj.rank == rank && obj.suit == suit) {
            del_object = obj
            del_index = idx
            return false //break
        }
    })
    del_object.div.remove()
    card_objects.splice(del_index, 1)
}

// Gets a card object's div, creating it if necessary. Adds the given click handler
function getCard(rank, suit, handler) {
    let card_object = findCardObject(rank, suit)
    if (card_object == null) {
        card_object = createCardObject(rank, suit)
        card_objects.push(card_object)
    }
    // Add data (.empty() clears it)
    card_object.div.data("rank", rank).data("suit", suit)

    // Attach click handler
    card_object.div.click(handler)

    // Clear highlight classes
    card_object.div.removeClass("highlight correct incorrect")

    return card_object.div
}

function cardMoveCompleteAndDelete(card_div) {
    deleteCardObject(card_div.data('rank'), card_div.data('suit'))
    cardMoveComplete()
}

function cardMoveComplete() {
    cards_animating -= 1
    if (cards_animating == 0) {
        if (next_state_deferred) {
            next_state_deferred = false
            nextState()
        }
    }
}

function deleteCardAfterMove(rank, suit) {
    deleteCardObject(rank, suit)
    cardMoveComplete()
}

// Gets an ordered, numeric rank from a string rank.
// Notice that Ace is 14, NOT 1.
function numericRank(string_rank) {
    switch (string_rank) {
        case "A": return 14
        case "K": return 13
        case "Q": return 12
        case "J": return 11
        default:
            return parseInt(string_rank)
    }
}

/*** DRAW FUNCTIONS ***/

// Displays your hand, optionally adding classes for highlights using highlight_selector
// highlight_selector should be a function (card, index) -> class(es) to add
function _displayYourHand(highlight_selector=null) {
    $("#your_hand").empty()

    your_hand.forEach(function(card, idx){
        let [rank, suit] = card
        // let card_added = createCard(rank, suit, onCardInHandClicked).data("index", idx)
        let card_div = getCard(rank, suit, onCardInHandClicked).data("index", idx)
        if (highlight_selector != null) {
            card_div.addClass(highlight_selector(card, idx))
        }
        $("#your_hand").append(card_div)
    })
}

// Displays the currently played cards, optionally adding classes for highlights using highlight_selector
// highlight_selector should be a function (card, index) -> class(es) to add
function _displayPlayedCards(highlight_selector=null) {

    played_cards.forEach(function(card, idx) {
        $(`#played_cards_${idx}`).empty()
      //  $(`#played_cards_${idx}`).append($("<span>").text(playerName(idx) + ": "))
      //  played_row = $("<div class='row'>")
        if (card != null) {
            // let card_added = createCard(card[0], card[1], onCardInPlayClicked).data("player", idx)
            let card_div = getCard(card[0], card[1], onCardInPlayClicked).data("player", idx)
            if (highlight_selector != null) {
                card_div.addClass(highlight_selector(card, idx))
            }
            $(`#played_cards_${idx}`).append(card_div)
        }
       // $(`#played_cards_${idx}`).append(played_row)
    })
}

function moveCard(card_obj, completion) {
    let start = card_obj.start
    let end = card_obj.div.offset()
    let dtop = end.top - start.top
    let dleft = end.left - start.left
    let sqr_magnitude = dtop * dtop + dleft * dleft

    if (sqr_magnitude < 5) {
        return // hardly moves, don't animate
    }

    card_obj.div.offset(start)
    cards_animating += 1
    card_obj.div.animate({
        left: `+=${dleft}`,
        top: `+=${dtop}`,
    }, 600, completion)
}

function drawCards(hand_highlight=null, played_highlight=null) {
    card_objects.forEach(function(card_obj, _) {
        if (card_obj.autoanim) card_obj.start = card_obj.div.offset()
    })

    _displayYourHand(hand_highlight)
    _displayPlayedCards(played_highlight)

    card_objects.forEach(function(card_obj, _) {
        if (card_obj.autoanim) moveCard(card_obj, cardMoveComplete)
    })
}

function prepDisplayTrickTaken(trick, taken_by) {
    let trick_objects = []

    trick.forEach(function(card, _) {
        let card_object = findCardObject(card[0], card[1])
        card_object.autoanim = false
        card_object.start = card_object.div.offset()
        trick_objects.push(card_object)
    })

    return trick_objects
}

function displayTrickTaken(trick_objects, taken_by) {
    let target = playerCardOffset(taken_by, trick_objects[0].div)

    trick_objects.forEach(function(card_object, _) {
        card_object.div.offset(target)
    })

    trick_objects.forEach(function(card_object, _) {
        moveCard(card_object, () => deleteCardAfterMove(card_object.rank, card_object.suit))
    })
}

// Displays each player's current points
function displayPoints() {

    points.forEach(function(pt, idx) {
        $(`#points_${idx}`).empty()
        points_row = $(`<div id=points_row_${idx}>`)
            .append($("<span>").text(pt))

        $(`#points_${idx}`).append(points_row)
    })
}


function displayContinueButton(){
    b = $("<button>")
        .text("Continue")
        .click(function(){
        question_status = question_status+1
        $("#result").text(question_status)
        //remove the button 
        $("#continue").empty()
        nextState()
    })

    $("#continue").append(b)
}

function displaySubmitButton(action) {
    $("#sidebar").append($("<button>").text("Submit").click(action))
}

// Draws the multiple choice question in using answer if non-null to mark correct response
function drawMultipleChoiceQuestion(answer=null) {
    $("#sidebar").empty().text(state.prompt)

    state.choices.forEach(function(choice, index) {
        let choice_div = $("<div>").text(choice)
        if (answer == null) {
            choice_div.click(() => multipleChoiceResponse(index))
        }
        else {
            if (index == answer.correct) {
                choice_div.text(choice + " (correct)")
            }
            else if (index == question.response) {
                choice_div.text(choice + " (your answer)")
            }
        }
        $("#sidebar").append(choice_div)
    })

    if (answer != null) {
        $("#sidebar").append($("<div style='padding-top:10px;'>").text(answer.explanation))
        displayContinueButton()
    }
}

function trickQuestionHighlightSelector (answer, card, idx) {
    let str = idx.toString()
    if (str == answer.correct) return "correct"
    if (str == question.response) return "incorrect"
    return ""
}

// Draws the take trick question in using answer if non-null to mark correct response
function drawTakeTrickQuestion(answer=null) {
    $("#sidebar").empty().text("Click the card that takes this trick.")
    if (answer != null) {
        $("#sidebar").append($("<div>").text(answer.explanation))
        displayContinueButton()

        // displayPlayedCards((card, idx) => trickQuestionHighlightSelector(answer, card, idx))
        drawCards(null, (card, idx) => trickQuestionHighlightSelector(answer, card, idx))
    }
}

function legalPlayQuestionAnswerSelector(answer, card, idx) {
    if (answer.correct[idx]) return "correct"
    if (question.response[idx]) return "incorrect"
    return ""
}

function legalPlayQuestionResponseSelector(card, idx) {
    return question.response[idx] ? "highlight" : ""
}

// Draws the legal play question in using answer if non-null to mark correct response
function drawLegalPlayQuestion(answer=null) {
    $("#sidebar").empty().text("Click ALL the cards that are legal plays.")
    if (answer != null) {
        // displayYourHand((card, idx) => legalPlayQuestionAnswerSelector(answer, card, idx))
        drawCards((card, idx) => legalPlayQuestionAnswerSelector(answer, card, idx))
        $("#sidebar").append($("<div>").text(answer.explanation))
        displayContinueButton()
    }
    else {
        // displayYourHand(legalPlayQuestionResponseSelector)
        drawCards(legalPlayQuestionResponseSelector)
        displaySubmitButton(legalPlayResponse)
    }
}

/*** PROCESS STATE ***/
// Each of these functions performs setup for a certain state, and calls nextState() if applicable

function setTextState() {
    $("#sidebar").text(state.text)
    nextState()
}

function clearTextState() {
    $("#sidebar").text("")
    nextState()
}

function clickCardState() {
    cardInHandCallback = card_div => {
        // Move to the next state if the card selected is the indicated card
        if (state.card[0] == card_div.data("rank") && state.card[1] == card_div.data("suit")) nextState();
    }
}

function playCardState() {
    if (current_player == 0) {
        let splice_index = -1
        your_hand.forEach(function(card, idx) {
            if (card[0] == state.card[0] && card[1] == state.card[1]) {
                splice_index = idx
                return false
            }
        })
        your_hand.splice(splice_index, 1)
        //displayYourHand()
    }
    played_cards[current_player] = state.card
    // displayPlayedCards()
    drawCards()

    current_player = (current_player + 1) % 4
    nextState()
}

function continueState(){
    displayContinueButton()
}

function takeTrickState() {
    // current_player is guaranteed to be the player who led this trick
    let led_suit = played_cards[current_player][1]
    let best_rank = 0
    let best_idx = -1
    let trick_points = 0

    let trick_taken = []
    // Add up points taken and determine who took the trick
    played_cards.forEach(function(card, idx) {
        let rank = card[0]
        let suit = card[1]

        if (suit == led_suit) {
            let nrank = numericRank(rank)
            if (nrank > best_rank) {
                best_rank = nrank
                best_idx = idx
            }
        }
        if (suit == "h") {
            hearts_broken = true
            trick_points ++
        }
        else if (suit == "s" && rank == "Q") {
            trick_points += 13
        }
        trick_taken.push(card)
    })

    // player that took the trick has the lead
    current_player = best_idx
    points[current_player] += trick_points

    displayPoints()
    trick_objects = prepDisplayTrickTaken(trick_taken, best_idx)
    drawCards()
    displayTrickTaken(trick_objects, best_idx)
    nextState()
}

function multipleChoiceState() {
    question = {
        prompt: state.prompt,
        choices: state.choices,
        response: null
    }
    drawMultipleChoiceQuestion()
}

function takeTrickQuestionState() {
    cardInPlayCallback = card_div => {
        if (question.response != null) return
        // Submit response
        takeTrickResponse(card_div.data("player"))
    }

    question = {
        response: null
    }
    drawTakeTrickQuestion()
}

function legalPlayQuestionState() {
    cardInHandCallback = card_div => {
        if (question.submitted) return;
        // Toggle the state of this card
        let index = parseInt(card_div.data("index"))
        question.response[index] = !question.response[index]
        drawLegalPlayQuestion()
    }

    question = {
        response: Array(your_hand.length).fill(false),
        submitted: false
    }
    drawLegalPlayQuestion()
}

function clearScreenState(){
    $("#game-content").empty()
    nextState()
}

function testMeState(){
    displayStateButton()
}

function displayStateButton(){
    b = $("<button>")
    .text("Test Me! ")
    .click(function(){
        window.location.href = "/test" 
    })
    $("#continue").append(b)
}

function displayQuestionStatus(){
    $("#result").text(question_status)
}

/*** STATE FLOW ***/

function processState() {
    next_state = state.next_state
    switch (state.action) {
        case "set_text": setTextState(); break;
        case "clear_text": clearTextState(); break;
        case "click_card": clickCardState(); break;
        case "play_card": playCardState(); break;
        case "continue": continueState(); break; 
        case "take_trick": takeTrickState(); break;
        case "clear_screen": clearScreenState(); break;
        case "mc_question": multipleChoiceState(); break;
        case "trick_question": takeTrickQuestionState(); break;
        case "play_question": legalPlayQuestionState(); break;
        case "test_me": testMeState(); break;
        default: console.error(`unknown state action ${state.action}`); break;
    }
    $("#quiz-number").empty()
    $("#quiz-number").append($(`<b>Quiz #${quiz_number}</b>`))
}

function cleanUpState() {
    cardInHandCallback = null
    cardInPlayCallback = null

    switch (state.action) {
        case "take_trick":
            played_cards = [null, null, null, null]
            drawCards()
            break;
        case "mc_question":
            $("#sidebar").empty()
            break;
        case "trick_question":
            // displayPlayedCards()
            drawCards()
            $("#sidebar").empty()
            break;
        case "play_question":
            // displayYourHand()
            drawCards()
            $("#sidebar").empty()
            break;
    }  
}

function done(){
    if(mode == "test")
        window.location.assign('/quiz_end')
}

function nextState() {
    if (cards_animating > 0) {
        next_state_deferred = true
        return
    }

    if (next_state == "done") {
        console.log("done")
        done()
        return
    }

    cleanUpState()
    
    $.ajax({
        type: "POST",
        url: "/fetch_state",           
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify({next_state: next_state, mode: mode}),
        success: function(result){
            state = result
            processState()
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}

/** CALLBACKS **/
function onCardInHandClicked() {
    if (cardInHandCallback != null)
        cardInHandCallback($(this))
}

function onCardInPlayClicked() {
    if (cardInPlayCallback != null)
        cardInPlayCallback($(this))
}

/*** QUESTION RESPONSE AJAX CALLS ***/
function multipleChoiceResponse(index) {
    quiz_number += 1
    question.response = index

    $.ajax({
        type: "POST",
        url: "/submit_mc_answer",           
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(index),
        success: function(result){
            let answer = result
            answer.correct = parseInt(answer.correct)
            drawMultipleChoiceQuestion(answer)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    })
}

function takeTrickResponse(index) {
    quiz_number += 1
    question.response = index

    $.ajax({
        type: "POST",
        url: "/submit_trick_answer",           
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify({response: index, played: played_cards, led: current_player}),
        success: function(result){
            let answer = result
            drawTakeTrickQuestion(answer)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    })
}

function legalPlayResponse() {
    quiz_number += 1
    $.ajax({
        type: "POST",
        url: "/submit_play_answer",           
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify({response: question.response, hand: your_hand, played: played_cards, hearts_broken: hearts_broken}),
        success: function(result){
            drawLegalPlayQuestion(result)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    })
}


/*** ENTRY POINT ***/
function ready() {
    //displayYourHand()
    //displayPlayedCards()
    displayQuestionStatus()
    drawCards()
    displayPoints()
    nextState()
}
$(ready)