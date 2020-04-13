import requests, re, sys
from bs4 import BeautifulSoup

data_url = 'https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx'

response = requests.get(data_url, timeout=10)

if response.status_code != 200:
    print("Failed to get health dept website")
    sys.exit(1)

content = BeautifulSoup(response.content, 'html.parser')

reg = re.compile('last updated at (\d?\d:\d\d\s[pa]\.?m\.?) on (\d\d?\/\d\d?\/\d\d\d\d)', re.IGNORECASE)

reg_match = reg.search(content.prettify())

if reg_match == None:
    print("Failed to match date string")
    sys.exit(2)
"""
try:
    testing_table = content.find('strong', string='Negative').parent.parent
except AttributeError:
    print("Failed to parse testing table")
    sys.exit(4)
"""
| Negative | Positive | Deaths |
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

"""
| County | Total Cases | Deaths |
"""

for row in cases_table.contents[1:]:
    county = row.contents[0].string
    total_cases = row.contents[1].string
    deaths = row.contents[2].string

    print(county, total_cases, deaths)
