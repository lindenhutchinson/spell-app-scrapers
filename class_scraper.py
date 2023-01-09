from utils import output_to_json, get_soup, MAIN_URL

def get_class_urls():
    soup = get_soup(MAIN_URL)
    class_urls = {}
    for ident in soup.find_all('sup'):
        if ident.contents[0].text == 'The':
            class_type = ident.find_next_sibling()
            if class_type and 'href' in class_type.attrs:
                class_url  = MAIN_URL + class_type.attrs['href']
                class_urls[class_type.text] = class_url

    return class_urls

def get_class_slots(class_url):
    soup = get_soup(class_url)
    spell_th = soup.find("th", string="Spell Slots per Spell Level")
    if spell_th:
        next_row = spell_th.find_next("tr")
        slot_level_count = 0
        start_count = False
        for i, th in enumerate(next_row.find_all('th')):
            if not start_count and th.text == '1st':
                start_count = True
                
            if start_count:
                slot_level_count +=1

        # initialise a slots data structure for all 20 levels
        slots = {x:[] for x in range(1, 21)}
        rows = next_row.find_all_next("tr")
        at_end_row = False
        for row_num, row in enumerate(rows):
            for i, cell in enumerate(row.find_all('td')[::-1]):
                at_end_row = cell.string == '20th'
                if i < slot_level_count:
                    if cell.text == '-':
                        slots[row_num+1].insert(0, 0)
                    else:
                        slots[row_num+1].insert(0, int(cell.text))

            if at_end_row:
                break
        
        return slots

def get_class_data():
    class_urls = get_class_urls()
    class_data = []
    for name, url in class_urls.items():
        slots = get_class_slots(url)
        class_data.append({
            'url':url,
            'name':name,
            'slots':slots
        })

    return class_data

if __name__ == "__main__":
    class_data = get_class_data()
    output_to_json(class_data, './data/class_data.json')