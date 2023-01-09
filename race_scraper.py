from utils import output_to_json, get_soup, MAIN_URL

LINEAGE_TYPES = [
    'Standard',
    'Exotic'
]

def get_race_urls():
    race_urls = {}
    soup = get_soup(MAIN_URL+'/lineage')
    for lin in LINEAGE_TYPES:
        lineage = soup.find('h1', string=f'{lin} Lineages')
        table = lineage.find_next(class_='wiki-content-table')
        race_tags = table.find_all('a')
        for race_tag in race_tags:
            race_urls[race_tag.text] = MAIN_URL + race_tag.attrs['href']

    return race_urls


def get_race_data():
    race_urls = get_race_urls()
    race_data = []
    for name, url in race_urls.items():
        # currently only using the names for races
        # can expand on data later by accessing the url
        race_data.append({
            'url':url,
            'name':name,
        })

    return race_data

if __name__ == "__main__":
    races = get_race_data()
    output_to_json(races, './data/race_data.json')
