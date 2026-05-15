import json
all_levels = ["A1", "A2", "B1", "B2"]
with open("data/grammar_profile.json") as f:
    curriculum = json.load(f)
def get_next_level(level):
    if level in all_levels:
        return all_levels[all_levels.index(level) + 1] if all_levels.index(level) + 1 < len(all_levels) else None
    return None
def get_step_content(step):
    return next((d for d in curriculum if d['step'] == step), None)
def get_total_steps(level):
    return len([d for d in curriculum if d['cefr_level'] == level])


print(get_next_level("A1"))
print(get_step_content(1))
print(get_total_steps("A1"))