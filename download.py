from bs4 import BeautifulSoup

def information(session, downloadPage, password):
    #get information about the download
    request = session.get(downloadPage)

    soup = BeautifulSoup(request.content, 'html.parser')
    
    try:
        table = soup.find(class_ = 'premium').find_all('tr')[0:]
        fileInformation = {        
            'filename': table[0].find_all(class_ = 'normal')[1].contents[0],
            'date': table[1].find_all(class_ = 'normal')[1].contents[0],
            'size': table[2].find_all(class_ = 'normal')[1].contents[0],
        }
    except:
        fileInformation = {        
            'filename': 'unknown or hidden',
            'date': 'unknown or hidden',
            'size': 'unknown or hidden',
        }

    adz = float(soup.find_all(attrs={'name': 'adz'})[0]['value'])
    if password == None:
        secondData = 'adz=' + str(adz)
    else:
        secondData = 'adz=' + str(adz) + '&pass=' + password

    secondRequest = session.post(downloadPage, data=secondData)

    secondSoup = BeautifulSoup(secondRequest.content, 'html.parser')

    downloadHref = None
    for a in secondSoup.find_all('a'):
        if a.contents[0] == 'Click here to download the file':
            downloadHref = a.get('href')

    return downloadHref, fileInformation