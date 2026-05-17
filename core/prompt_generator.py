from core import grammar_engine
from services import ai_service

def generate_prompt(step, level):
    # Get the content for the current step from the grammar engine
    content = grammar_engine.get_step_content(step, level)
    guide = content['guideword'] 
    learning_objective = content['learning_objective']
    example_sentence = content['example_sentence'] 

    user_prompt = (
        f"Teach the following grammar concept to the learner.\n\n"
        f"Concept: {guide}\n"
        f"Learning objective: {learning_objective}\n"
        f"Example sentence to use: \"{example_sentence}\"\n\n"
        f"Follow your teaching structure: introduce the concept, explain the rule "
        f"using the example, show a contrasting example, then ask one practice question."
        ) 

    # Call the AI service to generate a response based on the step content
    ai_response = ai_service.call_agent(user_prompt)
    
    return ai_response
