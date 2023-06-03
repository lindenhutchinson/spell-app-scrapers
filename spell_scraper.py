from utils import output_to_json, get_soup, MAIN_URL, clean_str

CLASSES = [
    "artificer",
    "bard",
    "cleric",
    "druid",
    "paladin",
    "ranger",
    "sorcerer",
    "warlock",
    "wizard",
]


def get_spells():
    soup = get_soup(MAIN_URL + "/spells")
    spells = []
    for table in soup.find_all(class_="wiki-content-table"):
        rows = table.find_all("tr")
        # get the spell level off the current table
        spell_level = int(table.parent.parent.attrs["id"][-1])
        print(f"scraping level {spell_level} spells")

        # skip the header row
        headers = rows[0].find_all("th")
        for row in rows[1:]:
            spell = {"level": spell_level}
            for i, cell in enumerate(row.find_all("td")):
                if a_tag := cell.find("a"):
                    spell["url"] = MAIN_URL + a_tag.attrs["href"]
                    spell["name"] = cell.text
                    spell.update(get_spell_info(spell["url"]))
                else:
                    attr_text = clean_str(headers[i].text)
                    if attr_text == "range":
                        attr_text = "spell_range"
                    spell[attr_text] = cell.text

            spells.append(spell)

    return spells


def get_class_spells():
    class_spells = {}
    for spell_class in CLASSES:
        class_spells[spell_class] = []

        soup = get_soup(MAIN_URL + f"/spells:{spell_class}")
        for table in soup.find_all(class_="wiki-content-table"):
            rows = table.find_all("tr")
            # skip the header row
            for row in rows[1:]:
                if cell := row.find("a"):
                    class_spells[spell_class].append(cell.text)
                    continue

    return class_spells


def get_spell_info(spell_url):
    try:
        soup = get_soup(spell_url)
    except ValueError as e:
        print(f"value error: {e}")
        return {}

    attrs = soup.find_all("strong")
    spell_info = {}

    for attr in attrs:
        attr_text = clean_str(attr.text)
        if attr_text == "spell_lists":
            p = attr.find_parent()
            a_tags = p.find_all("a")
            class_list = map(lambda x: x.text, a_tags)
            spell_info["class_list"] = ",".join(class_list)
        # use duration as a marker
        # as we know the next element will be the description
        elif attr_text == "duration":
            desc_p = attr.find_next("p")
            p_content = []
            while desc_p and "At Higher Levels" not in desc_p.text:
                p_content.append(desc_p.text)
                desc_p = desc_p.find_next("p")
            spell_info["description"] = "<br><br>".join(p_content)

        elif attr_text == "at_higher_levels":
            spell_info[attr_text] = attr.parent.text

    return spell_info


def write_spell_data():
    spells = get_spells()
    # class_spells = get_class_spells()
    # output_to_json(class_spells, "./data/class_spells.json")
    output_to_json(spells, "./data/spells.json")
    # TODO: retrieve extra spell information
    # spell_len = len(spells)
    # for i, spell in enumerate(spells):
    #     spell_info = get_spell_info(spell['url'])
    #     spell.update(**spell_info)
    #     os.system('cls')
    #     print(f'{i}/{spell_len}')
    #     if i > 10:
    #         break

    # return spells


if __name__ == "__main__":
    write_spell_data()
