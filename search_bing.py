# coding:utf-8
import csv
import glob
import os
import requests

OUTPUT_CSV = "download/images.csv"
OUTPUT_IMAGE_DIR = "download/images"
MS_KEY = ''
START = 0
END = 1000
KEYWORD = 'ハンバーグ'

def clean_dir_csv():
    if os.path.exists(OUTPUT_CSV):
        os.remove(OUTPUT_CSV)

    if os.path.exists(OUTPUT_IMAGE_DIR):
        files = glob.glob(OUTPUT_IMAGE_DIR + '/*.jpg')
        for path in files:
            os.remove(path)
    else:
        os.mkdir(OUTPUT_IMAGE_DIR)


def bing_search(query, skip=0):
    clean_dir_csv()

    bing_url = 'https://api.datamarket.azure.com/Bing/Search/Image'

    payload = {
        '$top': 50,
        '$skip': skip,
        '$format': 'json',
        'Query': "'"+query+"'",
    }
    r = requests.get(bing_url, params=payload, auth=(MS_KEY, MS_KEY))

    count = skip + 1

    if not os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=str(','), quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['origin_url', 'file_name'])

    with open(OUTPUT_CSV, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=str(','), quoting=csv.QUOTE_MINIMAL)

        for item in r.json()['d']['results']:
            image_url = item['MediaUrl']
            root, ext = os.path.splitext(image_url)
            if ext.lower() == '.jpg':
                print "." # image_url
                try:
                    r = requests.get(image_url)
                    if r.status_code == 200:
                        file_name = "%04d.jpg" % count
                        path = "{0}/{1}".format(OUTPUT_IMAGE_DIR, file_name)
                        f = open(path, 'wb')
                        f.write(r.content)
                        f.close()
                        writer.writerow([image_url, file_name])
                except Exception:
                    pass
            count += 1

if __name__ == '__main__':
    for skip in range(START, END, 50):
        bing_search(KEYWORD, skip)
