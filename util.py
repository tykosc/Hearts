def countSteps(states, start_state):
    step_states = ["continue_step", "step", "mc_question", "trick_question", "play_question"]

    state_id=start_state
    step_count = 0
    while state_id != "done":
        state = states[state_id]
        if state["action"] in step_states:
            step_count += 1
        state_id = state["next_state"]

    return step_count
