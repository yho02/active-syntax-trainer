import pandas as pd
import json 

df = pd.read_csv("grammar_profile_ver2.csv")
grammar_profile = df.to_dict('records')
with open("data/grammar_profile.json", "w") as f:
    json.dump(grammar_profile, f, indent=2)