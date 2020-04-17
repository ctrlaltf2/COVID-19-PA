import requests, re, sys, csv
from bs4 import BeautifulSoup

data_url = 'https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx'

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'en-US,en;q=0.5',
           'TE': 'Trailers'}

response = requests.get(data_url, timeout=10, headers=headers)

if response.status_code != 200:
    print("Failed to get health dept website")
    sys.exit(1)

content = BeautifulSoup(response.content, 'html.parser')

reg = re.compile('last updated at (\d?\d:\d\d\s[pa]\.?m\.?) on (\d\d?\/\d\d?\/\d\d\d\d)', re.IGNORECASE)

reg_match = reg.search(content.prettify())

if reg_match == None:
    print("Failed to match date string")
    sys.exit(2)

time = reg_match.group(1)
date = reg_match.group(2)
"""
try:
    testing_table = content.find('strong', string='Negative').parent.parent
except AttributeError:
    print("Failed to parse testing table")
    sys.exit(4)
"""
# | Negative | Positive | Deaths |
"""
testing_data = testing_table.contents[1]

negatives = testing_data.contents[0].string
positives = testing_data.contents[1].string
deaths = testing_data.contents[2].string

print(negatives, positives, deaths)
"""

try:
    cases_table = content.find('td', string='Allegheny').parent.parent
except AttributeError:
    print("Failed to parse cases table")
    sys.exit(3)

positives = {
    "Adams": 0,
    "Allegheny": 0,
    "Armstrong": 0,
    "Beaver": 0,
    "Bedford": 0,
    "Berks": 0,
    "Blair": 0,
    "Bradford": 0,
    "Bucks": 0,
    "Butler": 0,
    "Cambria": 0,
    "Cameron": 0,
    "Carbon": 0,
    "Centre": 0,
    "Chester": 0,
    "Clarion": 0,
    "Clearfield": 0,
    "Clinton": 0,
    "Columbia": 0,
    "Crawford": 0,
    "Cumberland": 0,
    "Dauphin": 0,
    "Delaware": 0,
    "Elk": 0,
    "Erie": 0,
    "Fayette": 0,
    "Forest": 0,
    "Franklin": 0,
    "Fulton": 0,
    "Greene": 0,
    "Huntingdon": 0,
    "Indiana": 0,
    "Jefferson": 0,
    "Juniata": 0,
    "Lackawanna": 0,
    "Lancaster": 0,
    "Lawrence": 0,
    "Lebanon": 0,
    "Lehigh": 0,
    "Luzerne": 0,
    "Lycoming": 0,
    "McKean": 0,
    "Mercer": 0,
    "Mifflin": 0,
    "Monroe": 0,
    "Montgomery": 0,
    "Montour": 0,
    "Northampton": 0,
    "Northumberland": 0,
    "Perry": 0,
    "Philadelphia": 0,
    "Pike": 0,
    "Potter": 0,
    "Schuylkill": 0,
    "Snyder": 0,
    "Somerset": 0,
    "Sullivan": 0,
    "Susquehanna": 0,
    "Tioga": 0,
    "Union": 0,
    "Venango": 0,
    "Warren": 0,
    "Washington": 0,
    "Wayne": 0,
    "Westmoreland": 0,
    "Wyoming": 0,
    "York": 0
}

negatives = positives.copy()
deaths = positives.copy()

"""
| County | Positives | Negatives | Deaths |
"""
for row in cases_table.contents[1:]:
    county = row.contents[0].string
    total_pos = row.contents[1].string
    total_neg = row.contents[2].string
    total_deaths = row.contents[3].string

    if positives.get(county.strip()) == None:
        print("Found a county that wasn't recognized, might need to update the master list?")
        print("County was '", county.strip(), "'")
        sys.exit(5)

    try:
        temp = int(total_pos)
        temp = int(total_neg)
        # temp = int(total_deaths)
    except ValueError:
        print("Couldn't parse a number out of the table")
        print("Value was '", total_pos, "'")
        sys.exit(6)

    positives[county.strip()] = total_pos
    negatives[county.strip()] = total_neg
    deaths[county.strip()] = total_deaths

date_str = '{} {}'.format(date, time)

pos_row = [date_str] + [i[1] for i in positives.items()]
neg_row = [date_str] + [i[1] for i in negatives.items()]
death_row = [date_str] + [i[1] for i in deaths.items()]

def append_row(filename, data):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

append_row('positives.csv', pos_row)
append_row('negatives.csv', neg_row)
append_row('deaths.csv', death_row)
