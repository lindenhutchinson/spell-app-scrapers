import json

# open the spells.json file and read the data
with open('spells.json', 'r') as f:
    spells = json.load(f)

# open the races.json file and read the data
with open('races.json', 'r') as f:
    races = json.load(f)

# open the class_data.json file and read the data
with open('class_data.json', 'r') as f:
    class_data = json.load(f)

# create the spells fixture data
spells_fixture = [{'model': 'app_name.spell', 'pk': index+1, 'fields': spell} for index, spell in enumerate(spells)]

# create the races fixture data
races_fixture = [{'model': 'app_name.race', 'pk': index+1, 'fields': race} for index, race in enumerate(races)]

# create the class_types fixture data
class_types_fixture = [{'model': 'app_name.class_type', 'pk': index+1, 'fields': {'name': class_data['name']}} for index, class_data in enumerate(class_data)]

# create the spell_slot_progression fixture data
spell_slot_progression_fixture = []
for class_data in class_data:
    for level, slots in class_data['slots'].items():
        spell_slot_progression_fixture.append({'model': 'app_name.spell_slot_progression', 'pk': len(spell_slot_progression_fixture)+1, 'fields': {'class_type': class_data['name'], 'level': level, 'slots': slots}})

# create the final fixture data
fixture = spells_fixture + races_fixture + class_types_fixture + spell_slot_progression_fixture

# write the fixture data to a file
with open('fixture.json', 'w') as f:
    json.dump(fixture, f)
