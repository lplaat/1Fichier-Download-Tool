import networking
import download
import time
import sys

#download settings
downloadPage = 'download-url'
outputDir = './downloads/'
password = None

#generale network settings
reCheckTime = 10

#network settings for tor
useTor = False
autoRenew = True
torSettings = {
    'proxyIp': 'tor-proxy-ip',

    'controlerIp': 'tor-controler-ip',
    'controlerPassword': 'tor-controler-password'
}


#for a proxy
useProxy = False
proxyIp = None

#create network session
session, renewConnection = networking.session(useTor, torSettings, autoRenew, useProxy, proxyIp)

#get download url
keep = True

while keep:
    try:
        downloadHref, fileInformation = download.information(session, downloadPage, password)

        print('\n********************************************')
        print('filename: ' + fileInformation['filename'])
        print('date: ' + fileInformation['date'])
        print('size: ' + fileInformation['size'])
        print('********************************************')

        if downloadHref == None:
            if autoRenew and useTor:
                print('\nFaild to locate the download url, tying again with a new ip!')
                time.sleep(10)
                session = renewConnection()
            else:
                print('\nFaild to locate the download url, waiting ' + str(reCheckTime) +' seconds!')
                time.sleep(reCheckTime)
        else:
            print('\nSuccessfully located the download url!')
            keep = False
    except KeyboardInterrupt:
        sys.exit()
    except:
        print('\nError')

#download the file
networking.downloadFile(downloadHref, outputDir + fileInformation['filename'], session)