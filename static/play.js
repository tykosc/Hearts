// Shared .js file for all interactive displays

// Global variables
let your_hand = _init.your_hand
let played_cards = _init.played_cards
let points = _init.points
let current_player = parseInt(_init.current_player)
let next_state = _init.start_state
let state = {}

function create_card(rank, suit) {
    card_div = $(`<div>${rank}${suit}</div>`)
    card_div.data("rank", rank)
    card_div.data("suit", suit)
    card_div.click(onCardClicked)
    return card_div
}

function display_your_hand() {
    your_hand.forEach(function(card, _){
        let rank = card[0]
        let suit = card[1]
        let card_added = create_card(rank, suit)
        $("#your_hand").append(card_added)
    })
}

function findCardInHand(rank, suit) {
    let out = null
    $("#your_hand").children().each(function(_) {
        if ($(this).data("rank") == rank && $(this).data("suit") == suit) {
            out = $(this) 
            return false // break
        }
    })
    return out
}

function setTextState() {
    $("#text").text(state.text)
    nextState()
}

function clearTextState() {
    $("#text").text("")
    nextState()
}

function clickCardState() {
    // setup here
}

function playCardState() {
    if (current_player == 0) {
        card = findCardInHand(state.card[0], state.card[1])
        card.remove()
    }
    else {
        // ...
    }
    current_player = (current_player + 1) % 4
    nextState()
}

function processState() {
    next_state = state.next_state
    switch (state.action) {
        case "set_text": setTextState(); break;
        case "click_card": clickCardState(); break;
        case "play_card": playCardState(); break;
        case "clear_text": clearTextState(); break;
        default: console.error(`unknown state action ${state.action}`); break;
    }
}

function nextState() {
    if (next_state == "done") {
        console.log("done")
        return
    }

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
function onCardClicked() {
    if (state == {}) return

    let rank = $(this).data("rank")
    let suit = $(this).data("suit")

    switch (state.action) {
        case "click_card":
            if (state.card[0] == rank && state.card[1] == suit) {
                nextState()
            }
            break;
        default:
            break;
    }
}

// Entry point
function ready() {
    display_your_hand()
    nextState()
}
$(ready)