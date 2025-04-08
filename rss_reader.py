#! /usr/bin/python3

# start -WindowStyle Minimized py "-m http.server -b 127.0.0.1 8080"

#import http.client,json
import os
import subprocess
#import socket, errno
import string
import glob
from datetime import datetime, timezone, timedelta
from html import unescape

def test():
    ibmMainDir = os.path.expanduser("~\\Documents\\jon\\ibm-main\\")
    with open(ibmMainDir + 'test.html', 'r+', encoding='utf-8') as f:
        l = f.readlines(3)
        print(l)

        f.seek(2,0)
        f.write("tttaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
        f.seek(0)
        l = f.read()
        print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
        print(l)
        print("zzzzzzzzzzzzzzzzzzzzzzzz")

# Webserver is needed because javascript can't write to disk'
# the javascript needs to delete messages from the RSS feed
def xxstart_webserver():
    ibmMainDir = os.path.expanduser("~\\Documents\\jon\\ibm-main\\")
    with open(ibmMainDir + "test.bat", "w+", encoding="utf-8") as batFile:
        batFile.writelines(["@echo on\n" + \
                            "echo args %~0 %~1 %~2 \n" + \
                            "if '%~1'=='lockFile' goto lockFile\n" + \
                            "if '%~1'=='runServer' goto runServer\n" + \
                            "echo running startup \n" + \
                            "cd " + ibmMainDir + "\n" + \
                            "start /min test.bat lockFile\n" + \
                            "pause 60 \n" + \
                            "goto leaveScript\n" + \
                            " \n" + \
                            ":lockFile\n" + \
                            "test.bat runServer 2>lockx.file\n" + \
                            "goto leaveScript\n" + \
                            " \n" + \
                            ":runServer\n" + \
                            "echo starting server: py -m http.server -b localhost 8080 --cgi\n" + \
                            "echo in directory: " + ibmMainDir + " \n" + \
                            "cd " + ibmMainDir + "\n" + \
                            "py -m http.server -b localhost 8080 --cgi\n" + \
                            "echo 'error: http.server error occurred'\n" + \
                            "pause 500\n" + \
                            "echo script terminating\n" + \
                            ":leaveScript"])
    os.system("start /D" + ibmMainDir + " test.bat")  
    print("running") 

def read_rss():
    import requests

    URL = "https://listserv.ua.edu/cgi-bin/wa?RSS&L=IBM-MAIN&v=2%2e0&LIMIT=3"
    CK = {"WALOGIN":"6A70657272796D614070616362656C6C2E6E6574-OE8929FEBCBECECDADBF2DF819C81FE9DD0D392F8D2EB-AOM"}
    response = requests.get(URL, cookies=CK)
    print(response.text)

def process_rss():
    srcDirectory = "C:\\Users\\jonpe\\Documents\\git\\jonperryman.github.io\\"
    os.chdir( os.path.expanduser("~\\Documents\\jon\\ibm-main\\") )
    
    os.startfile(os.getcwd() + "\\cgi-bin\\http_server_restart.bat")
    exit()
    transTable = " ".maketrans(" ","_",string.punctuation)

    if os.path.exists("ibm_main.rss") == False:
        print("Failed: ibm_main.rss does not exist\nload new data aborted")
        return
    
    print("starting load of ibm_main.rss")

    with open("ibm_main.rss", "r", encoding="utf-8") as newRSSFile:

        data = newRSSFile.read(5000).split("</lastBuildDate>",1)
        if len(data) == 1 and data[0]:
            work = newRSSFile.read(10000)
            if work:
                data = (data[0] + work).split("</lastBuildDate>",1)
        if len(data) == 1:
            print("Failed: </lastBuildDate> not found in ibm_main.rss")
            print("Aborting load of ibm_main.rss")
            exit()
        newRSS = data[1]
        newBuildDate = datetime.strptime( data[0].split("<lastBuildDate>",1)[1] ,"%d %b %Y %H:%M:%S %z").strftime("%y%m%d%H%M")

        if not os.path.exists("last.id"):
            with open("last.id", "w", encoding="utf-8") as lastIDfile:
                lastIDfile.close()
        with open("last.id", "r", encoding="utf-8") as lastIDfile:
            lastID = lastIDfile.readlines()
        if len(lastID) > 1:
            print("previous ibmm_main.rss processing failed. Deleting " + "*_" + lastID[1].rstrip() + ".html")
            os.system("erase " + "*_" + lastID[1].rstrip() + ".html")
            print("Now restarting load of ibm_main.rss")
        if len(lastID) == 0:
            lastID = ""
        else:
            lastID = lastID[0].rstrip()
        with open("last.id", "w", encoding="utf-8") as lastIDfile:
            lastIDfile.writelines(lastID + "\n" + newBuildDate + "\n delete " + "_" + newBuildDate) 

        newLastID = False
        while True:

            # keep reading until we find the end of the item "</item"
            newRSS = newRSS.split("</item>",1)
            if len(newRSS) == 1:
                data = newRSSFile.read(5000)
                if data:
                    newRSS = newRSS[0] + data
                    continue   
                # end of file and no more items 
                if lastID == "":
                    break    
                print("Failed: Last processed thread message " + lastID + " waas not in ibm_main.rss")
                print("Loading messages has been aborted!")
                exit()

            itemText = newRSS[0].split("<item>",1)[1]
            newRSS = newRSS[1]

            # Parse the item's text into each of the item's attributes
            item = {}
            while True:
                endTag = itemText.split("</", 1)
                if len(endTag) == 1:  
                    break   # last tag processed
                tagName = endTag[1].split(">", 1)
                item[tagName[0]] = endTag[0].split(tagName[0] + ">",1)[1]
                itemText = tagName[1]   
            item["id"] = item["link"].split(";",1)[1]
            if not newLastID:
                newLastID = item["id"]

            if lastID == item["id"]:
                print("last id " + lastID + " found")
                print("no more ibm_main.rss to load")
                break

            # Stip leading "re:" from thread names
            threadName = item["title"].split(" ")
            while "re:".find(threadName[0].lower()) == 0:
                del threadName[0]
            threadName = " ".join(threadName)
            threadID = threadName.encode('ascii', 'ignore').decode('ascii').translate(transTable)

            pubDate = datetime.strptime(item["pubDate"],"%a, %d %b %Y %H:%M:%S %z").astimezone(timezone.utc).replace(tzinfo=None)
            indexFilename = "index_" + pubDate.strftime("%y%m%d%H%M") + "_" + threadID + ".html"

            with open("build_" + threadID + "_" + newBuildDate + ".html", "a", encoding="utf-8") as f:

                if not os.path.exists("thread_" + threadID + ".html"):

                    with open(indexFilename, "w", encoding="utf-8") as f2:
                        f2.write("\n".join([

                            "<tr id='indexButtonTr_" + threadID + "'  class='threadButtonTr'>",

                            "<td>",
                            "<button id='indexHide_" + threadID + "' class='indexHide' onclick='indexMarkRead(this, \"" + threadID + "\");'>Read</button>",
                            "</td>",

                            "<td>",
                            "<button id='indexDel_" + threadID + "' class='indexDel' onclick='indexDelete(this, \"" + threadID + "\");'>Del</button>",
                            "</td>",

                            "<td>",
                            "<button id='index_" + threadID + "' class='index' onclick='indexOpen(this, \"" + threadID + "\");'>" + threadName.replace("<","&lt;").replace("&","&amp;").replace(">","&gt;") + "</button>",
                            "</td>",
                            
                            "<tr>\n\n"
                        ]))
                        
                    if not os.path.exists("threadlist.rebuild"):
                        with open("threadlist.rebuild", "w") as f:
                            f.close()

                    with open("thread_" + threadID + ".html", "w", encoding="utf-8") as f3:
                        f3.write("\n".join([

                            "<div id='threadButtonDiv_" + threadID + "' class='threadButtonDiv'>",
                            
                            "<button id='ThreadRead_" + threadID + "' class='threadRead' onclick='threadRead(this, \"" + threadID + "\");'>Read</button>",

                            "<button id='ThreadShow_" + threadID + "' class='threadShow' onclick='threadShow(this, \"" + threadID + "\");'>Show</button>",

                            "<button id='ThreadDelete_" + threadID + "' class='threadDelete' onclick='threadDelete(this, \"" + threadID + "\");'>Delete</button>",

                            "</div>",
                                    
                            "<h1 id='thread_" + threadID + "' class='threadH1'>" + threadName.replace("<","&lt;").replace("&","&amp;").replace(">","&gt;") + "</h1>\n\n"
                        ]))

                filelist = glob.glob("index_??????????_" + threadID + ".html")
                if len(filelist) != 1:
                    print("failed: too many files found for the thread: ", filelist)
                    print("aborting load of ibm_main.rss")
                    exit()

                    if filelist[0].split("\\")[-1] < indexFilename:
                        os.rename(filelist[0], indexFilename)

                    if not os.path.exists("threadlist.rebuild"):
                        with open("threadlist.rebuild", "w") as f:
                            f.close()


                f.write("\n\n".join([
                    "<div id='itemDiv_" + threadID + "' class='itemDiv'>",

                    "<button id='itemButton_" + threadID + "' class='itemButton' _filename='" + f.name.split("\\")[-1] + "' onclick='itemShowHide(this, threadID)'>hide</button>",

                    "<a id='itemAnchor_" + threadID + "' class='itemAnchor' href='" + item["link"] + "' target='_blank'>",
                              
                    "<span id='itemAuthor_" + threadID + "' class='itemAuthor'>",

                    item["author"] + " " + str(pubDate) + " </span>",

                    "<p id='itemText_" + threadID + "' class='itemText'>" + unescape(item["description"]) + "</p>",

                    "</a></div>\n\n"]))

    # merge the index files into single file
    if os.path.exists("threadlist.rebuild"):
        with open("threadlist.html", "w", encoding="utf-8") as indexFile:
            indexFile.write("<h1 id='threadListH1'>IBM-MAIN newsgroup</h1>\n\n" + \
                "<table id='indexTable'>\n\n")
            file_list = glob.glob("index_*.html")
            for file in file_list:
                with open(file, "r", encoding="utf-8") as f:
                    indexFile.write( f.read() )
            indexFile.write("</table>")
        os.remove("threadlist.rebuild")

    with open("last.id", 'w', encoding="utf-8") as lastIDfile:
        lastIDfile.writelines(newLastID)

    print("updated to the current ibm_main.rss file")

    os.system("mkdir cgi-bin")
    os.system("xcopy /-I /Y /E " + srcDirectory + "cgi-bin   cgi-bin")
    os.system("xcopy /-I /Y " + srcDirectory + "rss_reader.html    rss_reader.html")

    os.startfile("cgi-bin\\http_server_restart.bat")

    print("the http server failed")

def fix_grok_response(filename):
    print("filename: ", filename)
    with open(filename, "r+", encoding="utf-8") as f:
        lines = f.read().split("\n")
        cnt = 0
        while cnt < len(lines):
            if lines[cnt][0:1] != "<" and lines[cnt] != "":
                lines[cnt] = "<p>" + lines[cnt] + "</p>"
            cnt += 1
        f.seek(0,0)
        f.write("\n".join(lines))

def main():
    print("running main")
    #start_webserver()
    #read_rss()
    process_rss()
    #testPort()
    #fix_grok_response("mainframe_versus_other_computers\\grok_os_usage_riscv.html")
    print("main is finished")

main()