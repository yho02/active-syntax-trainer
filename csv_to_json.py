import pandas as pd
import json 


df = pd.read_csv("grammar_profile_ver2.csv")

grammar_profile = df.to_dict('records')

# reset step to 1 at the beginning of each level
current_level = None
step_counter = 0
for grammar in grammar_profile:
    if grammar["cefr_level"] != current_level:
        current_level = grammar["cefr_level"]
        step_counter = 1
    grammar["step"] = step_counter
    step_counter += 1

with open("data/grammar_profile.json", "w") as f:
    json.dump(grammar_profile, f, indent=2)