// Shared .js file for all interactive displays

// Global variables
let your_hand = _init.your_hand
let played_cards = _init.played_cards
let points = _init.points
let hearts_broken = _init.hearts_broken
let current_player = parseInt(_init.current_player)
let next_state = _init.start_state
let state = {}
let question = {}

function playerName(index) {
    if (index == 0) return "you"
    return `player ${index}`
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

function createCard(rank, suit, handler) {
    return $(`<span style="margin:3px">${rank}${suit}</span>`)
        .data("rank", rank)
        .data("suit", suit)
        .click(handler)
}

function displayYourHand(highlight_selector=null) {
    $("#your_hand").empty()

    your_hand.forEach(function(card, idx){
        let [rank, suit] = card
        let card_added = createCard(rank, suit, onCardInHandClicked).data("index", idx)
        if (highlight_selector != null) {
            card_added.addClass(highlight_selector(card, idx))
        }
        $("#your_hand").append(card_added)
    })
}

function displayPlayedCards(highlight_selector=null) {
    $("#played_cards").empty()

    played_cards.forEach(function(card, idx) {
        played_row = $("<div>")
            .append($("<span>").text(playerName(idx) + ": "))
        if (card != null) {
            let card_added = createCard(card[0], card[1], onCardInPlayClicked).data("player", idx)
            if (highlight_selector != null) {
                card_added.addClass(highlight_selector(card, idx))
            }
            played_row.append(card_added)
        }
        $("#played_cards").append(played_row)
    })
}

function displayPoints() {
    $("#points").empty()

    points.forEach(function(pt, idx) {
        points_row = $("<div>")
            .append($("<span>").text(playerName(idx) + ": "))
            .append($("<span>").text(pt))

        $("#points").append(points_row)
    })
}

function setTextState() {
    $("#sidebar").text(state.text)
    nextState()
}

function clearTextState() {
    $("#sidebar").text("")
    nextState()
}

function clickCardState() {
    // setup here
}

function playCardState() {
    if (current_player == 0) {
        your_hand.splice(your_hand.indexOf(state.card), 1)
        displayYourHand()
    }
    played_cards[current_player] = state.card
    displayPlayedCards()

    current_player = (current_player + 1) % 4
    nextState()
}

function continueState(){
    displayContinueButton()
}

function displayContinueButton(){
    b = $("<button>")
        .text("Continue")
        .click(function(){
        //remove the button 
        $("#continue").empty()
        nextState()
    })

    $("#continue").append(b)
}

function displaySubmitButton(action) {
    $("#sidebar").append($("<button>").text("Submit").click(action))
}

function takeTrickState() {
    // current_player is guaranteed to be the player who led this trick
    let led_suit = played_cards[current_player][1]
    let best_rank = 0
    let best_idx = -1
    let trick_points = 0
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
    })

    // player that took the trick has the lead
    current_player = best_idx
    points[current_player] += trick_points
    played_cards = [null, null, null, null]

    displayPlayedCards()
    displayPoints()
    nextState()
}

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
        $("#sidebar").append($("<div>").text(answer.explanation))
        displayContinueButton()
    }
}

function multipleChoiceState() {
    question = {
        prompt: state.prompt,
        choices: state.choices,
        response: null
    }
    drawMultipleChoiceQuestion()
}

function trickQuestionHighlightSelector (answer, card, idx) {
    let str = idx.toString()
    if (str == answer.correct) return "correct"
    if (str == question.response) return "incorrect"
    return ""
}

function drawTakeTrickQuestion(answer=null) {
    $("#sidebar").empty().text("Click the card that takes this trick.")
    if (answer != null) {
        $("#sidebar").append($("<div>").text(answer.explanation))
        displayContinueButton()

        displayPlayedCards((card, idx) => trickQuestionHighlightSelector(answer, card, idx))
    }
}

function takeTrickQuestionState() {
    question = {
        response: null
    }
    drawTakeTrickQuestion()
}

function legalPlayQuestionAnswerSelector(answer, card, idx) {
    if (answer.correct[idx]) return "correct"
    if (question.response[idx]) return "incorrect"
    return ""
}

function legalPlayQuestionResponseSelector(card, idx) {
    return question.response[idx] ? "highlight" : ""
}

function drawLegalPlayQuestion(answer=null) {
    $("#sidebar").empty().text("Click ALL the cards that are legal plays.")
    if (answer != null) {
        displayYourHand((card, idx) => legalPlayQuestionAnswerSelector(answer, card, idx))
        $("#sidebar").append($("<div>").text(answer.explanation))
        displayContinueButton()
    }
    else {
        displayYourHand(legalPlayQuestionResponseSelector)
        displaySubmitButton(legalPlayResponse)
    }
}

function legalPlayQuestionState() {
    question = {
        response: Array(your_hand.length).fill(false),
        submitted: false
    }
    drawLegalPlayQuestion()
}

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
        default: console.error(`unknown state action ${state.action}`); break;
    }
}

function cleanUpState() {
    switch (state.action) {
        case "mc_question":
            $("#sidebar").empty()
            break;
        case "trick_question":
            displayPlayedCards()
            $("#sidebar").empty()
            break;
        case "play_question":
            displayYourHand()
            $("#sidebar").empty()
            break;
    }  
}

function clearScreenState(){
    $("#game-content").empty()
}

function nextState() {
    if (next_state == "done") {
        console.log("done")
        window.location.href()
        return
    }

    cleanUpState()
    
    $.ajax({
        type: "POST",
        url: "/fetch_state",           
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(next_state),
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
    if (state == {}) return

    let rank = $(this).data("rank")
    let suit = $(this).data("suit")

    switch (state.action) {
        case "click_card":
            if (state.card[0] == rank && state.card[1] == suit) {
                nextState()
            }
            break;
        case "play_question":
            if (question.submitted) return;
            let index = parseInt($(this).data("index"))
            question.response[index] = !question.response[index]
            drawLegalPlayQuestion()
        default:
            break;
    }
}

function onCardInPlayClicked() {
    if (state == {}) return

    switch (state.action) {
        case "trick_question":
            if (question.response != null) return

            takeTrickResponse($(this).data("player"))
            break;
        default:
            break;
    }
}

function multipleChoiceResponse(index) {
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

// Entry point
function ready() {
    displayYourHand()
    displayPlayedCards()
    displayPoints()
    nextState()
}
$(ready)