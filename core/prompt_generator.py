from core import grammar_engine
from services import ai_service

def generate_prompt(step, level):
    # Get the content for the current step from the grammar engine
    content = grammar_engine.get_step_content(step, level)
    guide = content['guideword'] 
    learning_objective = content['learning_objective']
    example_sentence = content['example_sentence'] 

    user_prompt = (
        f"Grammar concept: {guide}\n"
        f"Example: \"{example_sentence}\"\n\n"
        f"Show the example, then ask the student to make a similar sentence."
        ) 

    # Call the AI service to generate a response based on the step content
    ai_response = ai_service.call_agent(user_prompt)
    
    return ai_response
