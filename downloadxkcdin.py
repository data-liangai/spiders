#! python3
# downloadXkcdin.py - Downloads every single XKCDIN comic.
import requests,bs4,os

os.makedirs('xkcdin', exist_ok=True) # store comics in ./xkcdin
for i in range(1,3026+1):
    url = f'https://xkcd.in/comic?lg=cn&id={i}'
    # Download the page.
    print(f'Downloading page {url}')
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text,'lxml')
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
        # Save the image to ./xkcd.
        imageFile = open(os.path.join('xkcdin', os.path.basename(comicUrl)), 'wb')

        for chunk in res.iter_content(10 ** 6):
            imageFile.write(chunk)
        imageFile.close()

print("Done.")