import requests
from bs4 import BeautifulSoup


official_channel_pages=['https://www.aparat.com/official','https://www.aparat.com/official/real']


def  OfficialChannelsUsernames(urllist=official_channel_pages):
    details_divs=[]
    for url in urllist:
        response = requests.get(url)
        html_content = response.content
        detlis=BeautifulSoup(html_content, 'html.parser').find_all('div', class_='details')
        for detli in detlis:
            details_divs.append(detli.find('a', class_='name').get('href').replace("/",''))
    details_divs=list(set(details_divs))
    return details_divs


