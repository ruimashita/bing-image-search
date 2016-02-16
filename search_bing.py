# coding:utf-8
import csv
import glob
import os
import requests

OUTPUT_CSV = "download/images.csv"
OUTPUT_IMAGE_DIR = "download/images"
MS_KEY = '07C0F+LSoFm6J3D/gm8yXnWqVQhsFG1Shrao4moKBN8'
SKIP = 0
NUMBER = 1000
KEYWORD = ''

def clean_dir_csv():
    if os.path.exists(OUTPUT_CSV):
        os.remove(OUTPUT_CSV)

    if os.path.exists(OUTPUT_IMAGE_DIR):
        files = glob.glob(OUTPUT_IMAGE_DIR + '/*.jpg')
        for path in files:
            os.remove(path)
    else:
        os.makedirs(OUTPUT_IMAGE_DIR)


def get_bing_images(query, skip=0):
    bing_url = 'https://api.datamarket.azure.com/Bing/Search/Image'

    payload = {
        '$top': 50,
        '$skip': skip,
        '$format': 'json',
        'Query': "'"+query+"'",
    }
    r = requests.get(bing_url, params=payload, auth=(MS_KEY, MS_KEY))

    return r.json()['d']['results']


def create_csv():
    if not os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=str(','), quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['origin_url', 'skip', 'file_name'])


def write_csv(image_url, file_name, skip):
    with open(OUTPUT_CSV, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=str(','), quoting=csv.QUOTE_MINIMAL)
        writer.writerow([image_url, skip, file_name])


def write_image(image_url, file_name):
    # print "try write image: {0} to {1}".format(image_url, file_name)
    root, ext = os.path.splitext(image_url)
    if ext.lower() != '.jpg':
        return False

    try:
        r = requests.get(image_url, timeout=1)
        if r.status_code != 200:
            return False

        path = "{0}/{1}".format(OUTPUT_IMAGE_DIR, file_name)
        f = open(path, 'wb')
        f.write(r.content)
        f.close()

        print "write image: {0} to {1}".format(image_url, file_name)
        return True

    except Exception:
        print("exception")
        return False

def bing_search():
    count = 0
    skip = SKIP
    create_csv()
    while 1:
        print "while skip: {}".format(skip)
        results = get_bing_images(KEYWORD, skip)

        for item in results:
            image_url = item['MediaUrl']
            file_name = "%07d.jpg" % count

            result = write_image(image_url, file_name)
            if result:
                write_csv(image_url, file_name, skip)
                count += 1

        skip += 50
        if count == NUMBER:
            print "break"
            break


if __name__ == '__main__':
    clean_dir_csv()
    bing_search()
    print("download complete")
