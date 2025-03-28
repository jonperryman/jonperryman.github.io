#! /usr/bin/python3

# start -WindowStyle Minimized py "-m http.server -b 127.0.0.1 8080"

import http.client,json
import os
import socket, errno

def start_webserver():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(("127.0.0.1", 8080))
        s.close()
        print("Starting web server")
        os.system("start /min py -m http.server -b localhost 8080")
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            print("Webserver already running")
        else:
            # something else raised the socket.error exception
            print("socket bind failed: ",e)
        s.close()
    
def read_rss():
    import requests

    URL = "https://listserv.ua.edu/cgi-bin/wa?RSS&L=IBM-MAIN&v=2%2e0&LIMIT=3"
    CK = {"WALOGIN":"6A70657272796D614070616362656C6C2E6E6574-OE8929FEBCBECECDADBF2DF819C81FE9DD0D392F8D2EB-AOM"}
    response = requests.get(URL, cookies=CK)
    print(response.text)

def process_rss():
    import xml.etree.ElementTree as ET
    tree = ET.parse("ibm_main.rss")
    root = tree.getroot()
    for work in root.findall('./channel/item'):
        item = {}
        for child in work:
            item[child.tag] = child.text
        print(item)
    print("end json")

def main():
    print("running main")
    # start_webserver()
    # read_rss()
    process_rss()

main()