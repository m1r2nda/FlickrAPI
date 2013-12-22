# coding: utf-8
import urllib2
import sys
import os
import json
from urllib import urlopen, urlencode,urlretrieve
import urllib
import errno
import jinja2
import random
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader,PackageLoader
from bottle import get,post, run, static_file,request

default_encoding = sys.getfilesystemencoding()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(SCRIPT_DIR, 'static/')
STATIC_DIR_JS = os.path.join(SCRIPT_DIR, 'static/js/')
STATIC_DIR_CSS = os.path.join(SCRIPT_DIR, 'static/css/')

photoURL = []
allURL = []

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
def download_image (search_word,number_of_photos):
        API_KEY = '925ddef1c5eb7c895fac3ae06f6277bf'
        URL = 'http://api.flickr.com/services/rest'
        params = {
                'api_key': API_KEY,
                'method': 'flickr.photos.search',
                'format': 'json',
                'nojsoncallback': 1,
                'text':search_word,
                'sort':'relevance'
        }
        query_string = '?{}'.format(urlencode(params))
        request_url = ''.join((URL, query_string))
        response_str = urlopen(request_url).read()
        response = json.loads(response_str)
        with open('ex.json', 'w') as f:
	       f.write(response_str)
        if int(number_of_photos) == 0: return None
        #print response
        photoURL = []
        for k in range(0,int(number_of_photos)):
            try:
                photoURL.append('http://farm' + str(response['photos']['photo'][k]['farm']) + '.static.flickr.com/' + str(response['photos']['photo'][k]['server']) + '/' + str(response['photos']['photo'][k]['id']) + '_' + str(response['photos']['photo'][k]['secret']) + '_m.jpg')
                allURL.append('http://farm' + str(response['photos']['photo'][k]['farm']) + '.static.flickr.com/' + str(response['photos']['photo'][k]['server']) + '/' + str(response['photos']['photo'][k]['id']) + '_' + str(response['photos']['photo'][k]['secret']) + '_m.jpg')
            except Exception, e:
                print e
            print photoURL
        #save_images(photoURL,search_word)


def save_images (list_of_links,search_word):
    k=0
    for i in list_of_links:
        make_sure_path_exists('/FlickrImages/')
        make_sure_path_exists('/FlickrImages/'+str(search_word)+'/')
        urllib.urlretrieve(i,'/FlickrImages/'+str(search_word)+'/'+str(k)+'.jpg')
        k=k+1


def download_images (search_text,number_of_photos):
    if os.path.exists(search_text):
            if os.path.isfile(search_text):
                with open(search_text,'r') as file:
                    lines = file.readlines()
                for i in lines:
                    download_image(i.replace("\n", ""),number_of_photos)
    else:
            print('File was not found.')
    return allURL

def download_images_by_words (words ,number_of_photos):
    for w in words:
        download_image(w.replace("\n", "").replace("\t",""),number_of_photos)
    return allURL

def create_page ():
    env = Environment()
    env.loader = FileSystemLoader('/templates/')
    template = env.get_template('slider.html')
    #template = Template('<html> Hello {{ name }}!</html>')
    templateVars = { "title" : "Photo Gallery",
                 "allURL" : allURL
               }
    site = template.render(templateVars)
    #print site[1:]
    make_sure_path_exists("/templates/")
    with open ('/templates/gallery.html','w+') as file:
        file.write(site.encode('utf-8'))

@get('/')
def index():
    return static_file('gallery.html', root=STATIC_DIR)


@get('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root=STATIC_DIR)

@get('/js/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath,root=STATIC_DIR_JS)

@get('/css/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath,root=STATIC_DIR_CSS)

@get('/photos')
def photos():
    global allURL
    allURL = []
    download_images("text.txt",4)
    return json.dumps(allURL)

@post('/photos')
def get_photos():
    search_photos_line = request.json
    if search_photos_line != "Enter here words to search photos!" and search_photos_line !="":
        search_photos_words = search_photos_line.split()
        global allURL
        allURL = []
        download_images_by_words(search_photos_words,4)
        return json.dumps(allURL)




if __name__ == '__main__':
	run(host='localhost', port=8080)
	#raw_input("Press Enter to continue... ")

