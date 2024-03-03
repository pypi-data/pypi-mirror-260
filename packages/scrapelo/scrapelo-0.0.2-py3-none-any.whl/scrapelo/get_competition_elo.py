import pandas as pd
import requests
from bs4 import BeautifulSoup


country_dict = {
    'Spain': 'ESP',
    'Italy': 'ITA',
    'Germany': 'GER',
    'France': 'FRA',
    'England': 'ENG',
    'Portugal': 'POR',
    'Netherlands': 'NED',
    'Belgium': 'BEL',
    'Scotland': 'SCO',
    'Turkey': 'TUR',
    'Czechia': 'CZE',
    'Greece': 'GRE',
    'Switzerland': 'SUI',
    'Denmark': 'DEN',
    'Sweden': 'SWE',
    'Austria': 'AUT',
    'Ukraine': 'UKR',
    'Croatia': 'CRO',
    'Serbia': 'SRB',
    'Slovakia': 'SVK',
    'Norway': 'NOR',
    'Russia': 'RUS',
    'Poland': 'POL',
    'Israel': 'ISR',
    'Romania': 'ROU',
    'Azrbaijan': 'AZE',
    'Ukraine': 'UKR',
    'Serbia': 'SRB',
    'Bulgaria': 'BUL',
    'Cyprus': 'CYP',
    'Hungary': 'HUN',
    'Moldova': 'MDA',
    'Slovenia': 'SVN',
    'Slovakia': 'SLK',
    'Kazakhstan': 'KAZ',
    'Finland': 'FIN',
    'Ireland': 'IRL',
    'Iceland': 'ISL',
    'Lithuania': 'LIT',
    'Latvia': 'LAT',
    'Estonia': 'EST',
    'Luxembourg': 'LUX',
    'Malta': 'MLT',
    'Andorra': 'AND',
    'San Marino': 'SMR',
    'Gibraltar': 'GIB',
    'Georgia': 'GEO',
    'Armenia': 'ARM',
    'Faroe Islands': 'FAR',
    'Wales': 'WAL',
    'Northern Ireland': 'NIR',
    'Belarus': 'BLR',
    'Albania': 'ALB',
    'Macedonia': 'MAC',
    'Montenegro': 'MNE',
    'Kosovo': 'KOS',
    'Iceland': 'ISL',
    'Bosnia-Herzegovina': 'BHZ',
    'Champions League': 'UCL',
    'Europa League': 'UEL',
    'Europa Conference League': 'ECL',
    'Europe': 'All'
}


def get_competition_elo(country):
    """
    Returns the current club ranking for a given country or competition.
    """
    if country in country_dict.keys():
        country = country_dict[country]
    elif country in country_dict.values():
        pass
    else:
        raise ValueError('Invalid country name or code. Use english names or 3-letter codes.')
    
    response = requests.get(f"http://clubelo.com/{country}")
    if response.status_code != 200:
        raise ValueError("Can't reach the website. Try again later.")
    
    soup = BeautifulSoup(response.content, 'html.parser')

    ranking_table = soup.find('table', class_='ranking')
    rows = ranking_table.find_all('tr')
    data = []
    for row in rows:
        cells = row.find_all('td')
        if cells:
            data.append([cell.get_text(strip=True) for cell in cells])
            data[-1].pop(3)


    df = pd.DataFrame(data, columns=['Country Rank', 'Club', 'Elo', 'Last Match', 'Coach'])
    df['Europe Rank'] = df['Club'].str.extract(r'^(\d+)', expand=False)
    df['Europe Rank'] = df['Europe Rank'].fillna('')
    df['Club'] = df['Club'].apply(lambda x: x.lstrip('0123456789'))
    df['Coach'] = df['Coach'].apply(lambda x: x.replace('(', ' ('))
    return df
