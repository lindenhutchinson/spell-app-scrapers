import json
from utils import APP_NAME


def create_class_type_fixture(class_data, filename):
    """Create fixtures data for the 'your_app.classtype' model.

    Args:
        class_data: A list of dictionaries containing data for each class.
        filename: The name of the file to save the fixtures data to.

    Returns:
        A dictionary mapping class names (in lowercase) to primary keys (PKs).
    """
    fixture_data = []
    class_pks = {}
    for i, item in enumerate(class_data):
        pk = i + 1
        fields = {"name": item["name"], "has_spells": item["slots"] is not None}
        fixture_item = {"model": f"{APP_NAME}.classtype", "pk": pk, "fields": fields}
        fixture_data.append(fixture_item)
        class_pks[item["name"].lower()] = pk

    with open(filename, "w") as fixture_file:
        json.dump(fixture_data, fixture_file)

    return class_pks


def create_slots_fixture(class_data, filename):
    """Create fixtures data for the 'your_app.spellslotprogression' model.

    Args:
        class_data: A list of dictionaries containing data for each class.
        filename: The name of the file to save the fixtures data to.
    """
    fixture_data = []
    for i, item in enumerate(class_data):
        class_pk = i + 1
        if item["slots"]:
            for level, slots in item["slots"].items():
                for spell_level, slots_at_level in enumerate(slots):
                    if slots_at_level != 0:
                        fields = {
                            "class_type": class_pk,
                            "char_level": int(level),
                            "spell_level": spell_level + 1,
                            "slots": slots_at_level,
                        }
                        fixture_item = {
                            "model": f"{APP_NAME}.spellslotprogression",
                            "pk": None,
                            "fields": fields,
                        }
                        fixture_data.append(fixture_item)

    with open(filename, "w") as fixture_file:
        json.dump(fixture_data, fixture_file)


def create_race_fixture(load_file, save_file):
    """Create fixtures data for the 'your_app.race' model.

    Args:
        load_file: The file to load race data from.
        save_file: The file to save the fixtures data to.
    """
    with open(load_file, "r") as fn:
        race_data = json.load(fn)

    fixture_data = []
    for i, item in enumerate(race_data):
        pk = i + 1
        fixture_item = {"model": f"{APP_NAME}.race", "pk": pk, "fields": item}
        fixture_data.append(fixture_item)

    with open(save_file, "w") as fn:
        json.dump(fixture_data, fn)


def create_class_data_fixtures(load_file, save_class_file, save_slots_file):
    """Create fixtures data for the 'your_app.classtype' and 'your_app.spellslotprogression' models.

    Args:
        load_file: The file to load class data from.
        save_class_file: The file to save the class fixtures data to.
        save_slots_file: The file to save the slots fixtures data to.

    Returns:
        A dictionary mapping class names (in lowercase) to primary keys (PKs).
    """
    with open(load_file, "r") as fn:
        class_data = json.load(fn)

    create_slots_fixture(class_data, save_slots_file)
    return create_class_type_fixture(class_data, save_class_file)


def create_spells_fixture(load_file, save_file):
    """Create fixtures data for the 'your_app.spell' model.

    Args:
        load_file: The file to load spell data from.
        save_file: The file to save the fixtures data to.

    Returns:
        A dictionary mapping spell names to primary keys (PKs).
    """
    with open(load_file, "r") as fn:
        spell_data = json.load(fn)
    fixture_data = []
    spell_pks = {}
    for i, item in enumerate(spell_data):
        pk = i + 1
        fixture_item = {"model": f"{APP_NAME}.spell", "pk": pk, "fields": item}
        spell_pks[item["name"]] = pk
        fixture_data.append(fixture_item)

    with open(save_file, "w") as fn:
        json.dump(fixture_data, fn)

    return spell_pks


def create_spell_class_fixture(class_pks, spell_pks, load_file, save_file):
    """Create fixtures data for the 'your_app.spellclass' model.

    Args:
        class_pks: A dictionary mapping class names (in lowercase) to primary keys (PKs).
        spell_pks: A dictionary mapping spell names to PKs.
        load_file: The file to load spell-class data from.
        save_file: The file to save the fixtures data to.
    """

    with open(load_file, "r") as fn:
        spell_class_data = json.load(fn)

    fixture_data = []
    for class_type, spells in spell_class_data.items():
        for spell in spells:
            fields = {"spell": spell_pks[spell], "class_type": class_pks[class_type]}
            fixture_item = {
                "model": f"{APP_NAME}.spellclass",
                "pk": None,
                "fields": fields,
            }
            fixture_data.append(fixture_item)

    with open(save_file, "w") as fn:
        json.dump(fixture_data, fn)


if __name__ == "__main__":
    class_pks = create_class_data_fixtures(
        "./data/class_data.json",
        "./fixtures/class_type.json",
        "./fixtures/spell_slot_progression.json",
    )
    spell_pks = create_spells_fixture("./data/spells.json", "./fixtures/spell.json")
    create_spell_class_fixture(
        class_pks, spell_pks, "./data/class_spells.json", "./fixtures/spellclass.json"
    )
    create_race_fixture("./data/race_data.json", "./fixtures/race.json")
