from utils import output_to_json, get_soup, MAIN_URL, clean_str
import os

def get_spells():
    soup = get_soup(MAIN_URL+'/spells')
    spells = []
    for table in soup.find_all(class_='wiki-content-table'):
        rows = table.find_all('tr')
        # skip the header row
        headers = rows[0].find_all('th')
        for row in rows[1:]:
            spell = {}
            for i, cell in enumerate(row.find_all('td')):
                if a_tag := cell.find('a'):
                    spell['url'] = MAIN_URL + a_tag.attrs['href']
                    spell['name'] = cell.text
                else:
                    attr_text = clean_str(headers[i].text)
                    spell[attr_text] = cell.text

            spells.append(spell)

    return spells

def get_spell_info(spell_url):
    try:
        soup = get_soup(spell_url)
    except ValueError as e:
        print(f'value error: {e}')
        return {}

    attrs = soup.find_all('strong')
    spell_info = {}
    
    for attr in attrs:
        attr_text = clean_str(attr.text)   
        if attr_text == 'spell_lists':
            p = attr.find_parent()
            a_tags = p.find_all('a')
            class_list = map(lambda x: x.text, a_tags)
            spell_info['class_list'] = ','.join(class_list)  
# use duration as a marker as we know the next element will be the description
        elif attr_text == 'duration':
            desc_p = attr.find_next('p')
            p_content = []
            while desc_p and not(desc_p and 'At Higher Levels' in desc_p.text):
                p_content.append(desc_p.text)
                desc_p = desc_p.find_next('p')

            spell_info['description'] = '\n\n'.join(p_content)
            if desc_p:
                spell_info['at_higher_levels'] = desc_p.text

    return spell_info

def get_spell_data():
    spells = get_spells()
    # TODO: retrieve extra spell information
    # spell_len = len(spells)
    # for i, spell in enumerate(spells):
    #     spell_info = get_spell_info(spell['url'])
    #     spell.update(**spell_info)
    #     os.system('cls')
    #     print(f'{i}/{spell_len}')
    #     if i > 10:
    #         break

    return spells

if __name__ == "__main__":
    spells = get_spell_data()

    output_to_json(spells, './data/spells.json')