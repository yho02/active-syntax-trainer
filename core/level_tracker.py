from core import grammar_engine
def track_level(current_step: int, current_level: str, score: int):
    # This is a placeholder function. In a real implementation, this would update a database or data store.
    total_steps = grammar_engine.get_total_steps(current_level)
    
    new_level = None
    if score == 3 and current_step < total_steps:  # Assuming a score of 3 means the learner has mastered the current step
        current_step += 1
    elif score == 3 and current_step >= total_steps:  # If the learner has completed all steps in the current level
        new_level = grammar_engine.get_next_level(current_level)  # You would implement this function
    
    return current_step, new_level if new_level else current_level
