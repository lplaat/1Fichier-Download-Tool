from fake_useragent import UserAgent
import stem
import stem.control
import requests
import sys

def session(useTor, torSettings, autoRenew, useProxy, proxyIp):
    #create network session with the proxy or tor settings
    #check if only 1 or 0 service is on
    if useTor and useProxy:
        print('Can only use 1 proxy service')
        sys.exit()

    #generate random user agent
    global headers
    headers = { 'User-Agent': UserAgent().random}

    #make a tor session
    if useTor:
        def renewConnection():
            with stem.control.Controller.from_port(port = int(torSettings['controlerIp'].split(':')[2])) as controller:
                controller.authenticate(password = torSettings['controlerPassword'])
                controller.signal(stem.Signal.NEWNYM)
            
            session = requests.session()
            session.headers = headers
            session.proxies = {
                'http': torSettings['proxyIp'],
                'https': torSettings['proxyIp']
            }
            return session

        session = renewConnection()

        if autoRenew:
            return session, renewConnection
        else:
            return session, None
    elif useProxy:
        #create a session with a basic proxy
        session = requests.session()
        session.headers = headers
        session.proxies = {
            'http': proxyIp,
            'https': proxyIp
        }

        return session, None
    else:
        #return a normale session with no proxy
        session = requests.session()
        session.headers = headers
        return session, None

def downloadFile(downloadHref, path, session):
    with session.get(downloadHref, stream=True) as r:
        filename = r.headers['Content-Disposition'].split('filename="')[1].split('"; ')[0]
        size = int(r.headers['Content-Length'])

        print('\n********************************************')
        print('filename: ' + filename)
        print('size: ' + str(round(int(r.headers['Content-Length']) / 1073741824, 3)) + ' GB')
        print('********************************************')

        print('\nDownloading file...\n\n')

        r.raise_for_status()
        i = 0
        with open(path.replace('unknown or hidden', filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if (round(i/20) - i/20) == 0:
                    print('\x1b[1A\x1b[2KJust downloaded: ' + str(round(((i*8192) / size)*100, 2)) + '%, Totaly downloaded: ' + str(round((i * 8192) / 1073741824, 3)) + ' GB')

                f.write(chunk)
                i += 1