#! python3
# downloadXkcdin2.py - Downloads XKCDIN comic using multiple threads.
import requests,bs4,os,threading,time

os.makedirs('xkcdin2', exist_ok=True) # store comics in ./xkcdin2

def downloadXkcdin(startpage,endpage):
    for urlNumber in range(startpage, endpage + 1):
        url = f'https://xkcd.in/comic?lg=cn&id={urlNumber}'
        # Download the page.
        print(f'Downloading page {url}')
        res = requests.get(url)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'lxml')
        # Find the URL of the comic image.
        comicElem = soup.find_all('img')
        if comicElem == []:
            print("Could not find the image.")
        else:
            comicUrl = 'https://xkcd.in' + comicElem[0].get('src')
            # Download the image.
            print(f"Downloading image {comicUrl}")
            res = requests.get(comicUrl)
            res.raise_for_status()
            # Save the image to ./xkcdin2
            imageFile = open(os.path.join('xkcdin2', os.path.basename(comicUrl)), 'wb')

            for chunk in res.iter_content(10 ** 6):
                imageFile.write(chunk)
            imageFile.close()

startTime = time.time()
# Create and start the Thread objects.
downloadThreads = []    # a list of all the Thread objects
for i in range(1,3024+1,189):   # loops 16 times, creates 16 threads
    start = i
    end = i + 188
    downloadThread = threading.Thread(target=downloadXkcdin,args=(start,end))
    downloadThreads.append(downloadThread)
    downloadThread.start()
# Wait for all threads to end.
for downloadThread in downloadThreads:
    downloadThread.join()

print("Done.")

endTime = time.time()
print(f"The program takes {round(endTime - startTime,2)} seconds.")
