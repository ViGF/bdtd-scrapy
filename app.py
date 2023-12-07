import requests
from bs4 import BeautifulSoup

arq_csv = open('fase3.csv', 'w', encoding='utf-8')
maxQuantity = 25

splitDelimiter = '/vufind'
# Substitua o link da sua pesquisa
completeUrl = 'https://bdtd.ibict.br/vufind/Search/Results?lookfor=atendimento+ubs&type=AllFields&filter%5B%5D=format%3A%22masterThesis%22'.split(splitDelimiter, 1)

baseUrl = completeUrl[0]
query = splitDelimiter + completeUrl[1]

pageNumber = 1
researchCounter = 0

def getHTML(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    return soup

def writeInfos(soup, remainingQuantity):
    researchQuantityInPage = 0

    authors = soup.select('.author a')
    years = soup.find_all('div', {'id': 'datePublish'})
    titles = soup.find_all('a', {'class': 'title'}, limit=remainingQuantity)
    links = soup.find_all('a', {'class': 'fulltext'})

    for (author, year, title, link) in zip(authors, years, titles, links):
        author = author.text
        year = year.text.split()[-1]
        title = title.text.strip()
        link = link.get('href')

        arq_csv.write(f"{author};{year};{title};{link}\n")
        researchQuantityInPage += 1

    return researchQuantityInPage

arq_csv.write("Autor;Ano de Defesa;Título;Link\n")

url = baseUrl + query
soup = getHTML(url)

while researchCounter < maxQuantity:
  remaining = maxQuantity - researchCounter
  quantityAdded = 0
  if pageNumber == 1:
    print("Página:", pageNumber)

    quantityAdded = writeInfos(soup, remaining)

    print("Trabalhos coletados:", quantityAdded)
  elif remaining > 0:
    print("Página:", pageNumber)

    try:
      nextQueryLink = soup.select('ul.pagination > li.active + li > a')[0].get('href')
      url = baseUrl + nextQueryLink
      soup = getHTML(url)
    except:
      print(f"Parece que a sua busca não retorna {maxQuantity} resultados")
      break

    quantityAdded = writeInfos(soup, remaining)
    print("Trabalhos coletados:", quantityAdded)

  pageNumber = pageNumber + 1
  researchCounter += quantityAdded

arq_csv.close()

print(f"Foram coletados {researchCounter} trabalhos. Seu arquivo está pronto!")