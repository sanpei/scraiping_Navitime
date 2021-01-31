import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')

search_url = conf['URL']['url'].lower()