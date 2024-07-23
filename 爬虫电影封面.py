from bs4 import BeautifulSoup
import requests
import os

DOWNLOAD_URL = 'https://movie.douban.com/top250/'
def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        return None

def get_image(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    ol = soup.find('ol',class_= 'grid_view')
    img_urls =[]
    for i in ol.find_all('li'):
        img_tag = i.find('div',class_='item').find('img')
        img_url = img_tag['src']
        img_urls.append(img_url)
    page = soup.find('span', attrs={'class': 'next'}).find('a')
    if page:
        return img_urls, DOWNLOAD_URL + page['href']
    else:
        return img_urls, None

def download_image(url,save_path, filename):

    file_path = os.path.join(save_path, filename)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
                print(f"Download {filename}")
        else:
            print(f"Failed to download {filename}. Status code: {response.status_code}")
    except requests.RequestException as e:
            print(f"Error downloading {filename}: {e}")

def main():
    url = DOWNLOAD_URL
    imge_urls=[]
    save_directory = '' #填入你想保存文件的文件夹路径

    while url:
        data = download_page(url)
        if data is not None:
            new_image_urls, url = get_image(data)
            imge_urls.extend(new_image_urls)
        else:
            break

    for image_url in imge_urls:
        filename = image_url.split('/')[-1]
        download_image(image_url, save_directory, filename)
    print('下载完成')


if __name__ == '__main__':
    main()
