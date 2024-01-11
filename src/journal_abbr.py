import requests
from bs4 import BeautifulSoup

def find_abb_wiki(name):
    url = "https://en.wikipedia.org/wiki/%s" % name
    url = url.replace(' ', '_')
    
    #mw-content-text > div.mw-content-ltr.mw-parser-output > table > tbody > tr:nth-child(12) > td > i  
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")

    # The image you want is inside a img HTML element which is contained inside a "div" element: 
    div_element = soup.find_all("td", class_="infobox-data identifier")

    # Print the "src" value of the img HTML element found on the div
    journal_abbr = div_element[0].find("i").string
    # print(journal_abbr)
    
    return journal_abbr


if __name__ == "__main__":
    name = 'Journal of Applied Meteorology and Climatology'
    journal_abbr = find_abb_wiki(name)
    