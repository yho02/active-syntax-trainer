import json

cirriculum_file = json.load(open("data/grammar_profile.json"))
def get_next_level(level):
    return curriculum_file.key() #retrieve next level from file 
def get_step_content(step):
    return curriculum_file[step] #retrieve content from file
def get_total_steps(level):
    return #retrieve total steps for a level from file