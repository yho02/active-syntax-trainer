import pandas as pd
import json 


df = pd.read_csv("grammar_profile_ver2.csv")

grammar_profile = df.to_dict('records')
with open("data/grammar_profile.json", "w") as f:
    json.dump(grammar_profile, f, indent=2)

# reset first step at each level to 1, and add a field for total steps in each level
for entry in grammar_profile:
    entry['current_step'] = 1
    level = entry['level']
    if 'total_steps' not in entry:
        entry['total_steps'] = sum(1 for e in grammar_profile if e['level'] == level)
with open("data/grammar_profile.json", "w") as f:
    json.dump(grammar_profile, f, indent=2)