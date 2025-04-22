#! /usr/bin/python3

# start -WindowStyle Minimized py "-m http.server -b 127.0.0.1 8080"

import http.server
#import http.client,json
import os
import subprocess
#import socket, errno
import string
import glob
from datetime import datetime, timezone, timedelta
from html import unescape

def read_rss():
    import requests

    URL = "https://listserv.ua.edu/cgi-bin/wa?RSS&L=IBM-MAIN&v=2%2e0&LIMIT=3"
    CK = {"WALOGIN":"6A70657272796D614070616362656C6C2E6E6574-OE8929FEBCBECECDADBF2DF819C81FE9DD0D392F8D2EB-AOM"}
    response = requests.get(URL, cookies=CK)
    print(response.text)

def process_ibm_main_rss(newRSSFile):

    transTable = " ".maketrans(" ","_",string.punctuation)

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

    if data[0][-3:] == "GMT": 
        work = data[0][:-3] + "+0000"        
    elif data[0][-2:] == " Z":
        work = data[0][:-1] + "+0000"
    else:
        work = data[0]
    work = work.split("<lastBuildDate>",1)[1]
    newBuildDate = datetime.strptime( work ,"%d %b %Y %H:%M:%S %z").strftime("%y%m%d%H%M")

    lastID = False
    lastBuildDate = False
    if os.path.exists("last.id"):
        with open("last.id", "r", encoding="utf-8") as f:
            lastIDList = f.readlines()
        if lastIDList[0].strip() != "":
            lastID = lastIDList.pop(0).split("/")[3].strip()

        if len(lastIDList) > 1:
            print("***** performing cleanup because the previous updates from ibm_main.rss failed")
            print("\n".join(lastIDList))
            print("****************************************************************************")
            print("****** recovering to id=", lastID)
            for work in lastIDList:
                work = work.split("/")
                if len(work) > 1:
                    print("removing files for ", work)
                    eraseCmd = "erase build_*" + work[1].strip() + ".*.html"
                    print( eraseCmd )
                    os.system( eraseCmd )
            print("***** recovery is complete. load of ibm_main.rss will now continue.")

    newLastID = False
    createThreadlistFile = True
    loopCnt = 0
    while True:

        # keep reading until we find the end of the item "</item"
        newRSS = newRSS.split("</item>",1)
        if len(newRSS) == 1:
            data = newRSSFile.read(5000)
            if data:
                newRSS = newRSS[0] + data
                continue   
            # end of file and no more items 
            if not lastID:
                break   
            print("Failed: Last processed thread message " + lastID + " was not in ibm_main.rss")
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
        
        loopCnt += 1
        if loopCnt % 100 == 0:
            print("now processing item ", loopCnt, " itemID=", item["id"])

        if not newLastID:
            newLastID = item["id"]
            with open("last.id", "a", encoding="utf-8") as f:
                f.write("\nbuild: /" + newBuildDate + "/ id: /" + newLastID + "/")
        if lastID == item["id"]:
            print("last id " + lastID + " found")
            print("all new ibm_main.rss items have been loaded")
            break

        # Stip leading "re:" from thread names
        threadName = item["title"].strip()
        while True:
            if "re: fw: aw: sv:".find(threadName[:3].lower()) >= 0:
                threadName = threadName[3:].strip() 
            elif "auto:" == threadName[:5].lower():
                threadName = threadName[5:].strip()
            elif "[external]" == threadName[:10].lower():
                threadName = threadName[10:].strip()
            elif "[extern]" == threadName[:8].lower():
                threadName = threadName[8:].strip()
            else:
                break
        threadID = threadName.encode('ascii', 'ignore').decode('ascii').translate(transTable).lower()

        if item["pubDate"][-3:] == "GMT": 
            work = item["pubDate"][:-3] + "+0000"        
        elif item["pubDate"][-2:] == " Z":
            work = item["pubDate"][:-1] + "+0000"
        else:
            work = item["pubDate"]
        pubDate = datetime.strptime(work, "%a, %d %b %Y %H:%M:%S %z").astimezone(timezone.utc).replace(tzinfo=None)
        indexFilename = "index_" + pubDate.strftime("%y%m%d%H%M") + "_" + threadID + ".html"

        with open("build_" + threadID + "." + newBuildDate + ".show.html", "a", encoding="utf-8") as buildFile:

            if not os.path.exists("thread_" + threadID + ".html"):

                with open(indexFilename, "w", encoding="utf-8") as f:
                    f.write( threadName.replace("<","&lt;").replace("&","&amp;").replace(">","&gt;") )                  
                if createThreadlistFile and not os.path.exists("indexlist.rebuild"):
                    createThreadlistFile = False
                    with open("indexlist.rebuild", "w") as threadlistFile:
                        threadlistFile.close()

                with open("thread_" + threadID + ".html", "w", encoding="utf-8") as f:
                    f.write(threadName.replace("<","&lt;").replace("&","&amp;").replace(">","&gt;"))

            filelist = glob.glob("index_??????????_" + threadID + ".html")
            if len(filelist) != 1:
                print("failed: too many index files found for this thread: ", filelist)
                print("Exactly 1 index file must exist for each message thread")
                print("aborting load of ibm_main.rss")
                exit()

            if filelist[0].split("\\")[-1] < indexFilename:
                os.rename(filelist[0], indexFilename)

            if createThreadlistFile and  not os.path.exists("indexlist.rebuild"):
                createThreadlistFile = False
                with open("indexlist.rebuild", "w") as indexRebuildFile:
                    indexRebuildFile.close()

            itemID = item["id"].replace(".","_")
            buildFile.write("\n\n".join([
                "<div id='itemDiv_" + itemID + "' class='itemDiv' _item='" + threadID + "/" + newBuildDate + "/" + itemID + "'>",

                "<button id='itemButton_" + itemID + "' class='itemButton' onclick='itemShowRead(this, \"" + threadID + "/" + newBuildDate + "/" + itemID + "\");'>read</button>",

                "<a id='itemAnchor_" + itemID + "' class='itemAnchor' href='" + item["link"] + "' target='ibm_main'>",
                            
                "<span id='itemAuthor_" + itemID + "' class='itemAuthor'>" + item["author"] + " " + str(pubDate) + " </span>",

                "<p id='itemText_" + itemID + "' class='itemText'>" + unescape(item["description"]) + "</p>",

                "</a></div>\n\n"]))

    with open("last.id", 'w', encoding="utf-8") as f:
        f.write("build: /" + newBuildDate + "/ id: /" + newLastID + "/")
        
def rss_rebuild_index():

    print("rebuilding the indexlist.html")
    with open("indexlist.html", "w", encoding="utf-8") as indexFile:
        indexFile.write("<h1 id='threadListH1'>IBM-MAIN newsgroup</h1>\n\n" + \
            "<table id='indexTable'>\n\n")
        file_list = glob.glob("index_*.html")
        loopCnt = 0
        for file in reversed(file_list):
            loopCnt += 1
            if loopCnt % 100 == 0:
                print("processing index ", loopCnt, " file=", file)
            work = file[ : -5 ].split("_",2)
            threadID = work[2]
            if len(glob.glob("build_" + threadID + ".??????????.????.html")) == 0:
                os.remove("thread_" + threadID + ".html")
                os.remove(file)
                continue   # thread no longer exists
            threadLastUpdated = work[1][0:2] + "/" + work[1][2:4] + "/" + work[1][4:6] 
            with open(file, "r", encoding="utf-8") as f:
                indexFile.write("\n".join([

                        "<tr id='indexButtonTr_" + threadID + "'  class='threadButtonTr'>",

                        "<td>",
                        "<button id='indexRead_" + threadID + "' class='indexRead' onclick='indexMarkRead(this, \"" + threadID + "\");'>Read</button>",
                        "</td>",

                        "<td>",
                        "<button id='indexDel_" + threadID + "' class='indexDel' onclick='indexDelete(this, \"" + threadID + "\");'>Del</button>",
                        "</td>",

                        "<td>",
                        "<button id='indexDate_" + threadID + "' class='indexDate'>" + threadLastUpdated + + "</button>",
                        "</td>",

                        "<td>",
                        "<button id='index_" + threadID + "' class='index' onclick='indexOpen(this, \"" + threadID + "\");'>" + f.read() + "</button>",
                        "</td>",
                        
                        "<tr>\n\n"
                    ]))
        indexFile.write("</table>")
    os.remove("indexlist.rebuild")

def process_rss():
  
    if os.path.exists("ibm_main.rss") == False:
        print("Failed: ibm_main.rss does not exist\nload new data aborted")
        exit()
    
    print("starting load of ibm_main.rss")

    with open("ibm_main.rss", "r", encoding="utf-8") as f:
        process_ibm_main_rss(f)

    # merge the index files into single file
    if os.path.exists("indexlist.rebuild"):
        rss_rebuild_index()

    print("updated to the current ibm_main.rss file")

    os.system("xcopy /-I /Y " + srcDirectory + "rss_reader.html  .")
    os.system("xcopy /-I /Y " + srcDirectory + "http_server.py  .")
    os.system("xcopy /-I /Y " + srcDirectory + "http_server.bat  $http_server.bat")

    print("rss_reader.py: Successfuly completed rss updates")

def fix_grok_response(filename):
    print("filename: ", filename)
    with open(filename, "r+", encoding="utf-8") as grok:
        lines = grok.read().split("\n")
        cnt = 0
        while cnt < len(lines):
            if lines[cnt][0:1] != "<" and lines[cnt] != "":
                lines[cnt] = "<p>" + lines[cnt] + "</p>"
            cnt += 1
        grok.seek(0,0)
        grok.write("\n".join(lines))

def test():
    testData = "\n".join(["<lastBuildDate>10 Apr 2010 01:01:01 Z</lastBuildDate>",

        "<item>",
        "<pubDate>Tue, 10 Apr 2010 14:09:25 +0200</pubDate>",
        "<link>aaa;10.1</link>",
        "<title>aaa</title>",
        "<description>10-1</description>",
        "<guid>rrr;rrr</guid>",
        "<author>auth</author>",
        "</item>",


        "<item>",
        "<pubDate>Tue, 10 Apr 2010 14:09:25 +0200</pubDate>",
        "<link>aaa;10.2</link>",
        "<title>aaa</title>",
        "<description>10.2</description>",
        "<guid>rrr;rrr</guid>",
        "<author>auth</author>",
        "</item>",

        "<item>",
        "<pubDate>Tue, 10 Apr 2010 14:09:25 +0200</pubDate>",
        "<link>aaa;10.3</link>",
        "<title>aaa</title>",
        "<description>10-3</description>",
        "<guid>rrr;rrr</guid>",
        "<author>auth</author>",
        "</item>"])
    
    testDir = os.path.expanduser("~\\Documents\\jon\\ibm-main-test\\" )
    if not os.path.exists( testDir ):
        os.mkdir(testDir)
    if os.system("pushd " + testDir) != 0:
        print("changeDir to ibm-main-test failed")
        print("aborting test")
        exit(99)

    os.system("erase /Q *.*")

    with open("ibm_main.rss", "w", encoding="utf-8") as f:
        f.write(testData)
    process_rss()

    with open("ibm_main.rss", "w", encoding="utf-8") as f:
        f.write(testData.replace("10","11") + "<item>" + testData.split("<item>")[1].split("</item>")[0] + "</item>")
    process_rss()

    with open("ibm_main.rss", "w", encoding="utf-8") as f:
        f.write(testData.replace("10","12") + "<item>" + testData.split("<item>")[1].split("</item>")[0].replace("10","11") + "</item>")
    process_rss()


srcDirectory = "C:\\Users\\jonpe\\Documents\\git\\jonperryman.github.io\\"
os.chdir( os.path.expanduser("~\\Documents\\jon\\ibm-main\\") )

def main():
    print("running main")
    #start_webserver()
    #read_rss()
    # test()
    process_rss()
    #testPort()
    #fix_grok_response("mainframe_versus_other_computers\\grok_os_usage_riscv.html")
    print("main is finished")

main()