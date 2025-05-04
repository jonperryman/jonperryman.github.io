import sys
import glob

def main(file):

    print("converting ", file, "to html")
    
    if file[-5:] != ".html":
        print("failed: ",file," must be an HTML file type")
        return

    with open(file, "rb") as f:
        data = f.read()

    if data.find(b'<p>') > 0:
        print("failed: file ", file, " appears to be converted")
        return

    data = b''.join(data.split(b'\r')) # remove carriage returns - not needed & simplifies conversion

    # create <h2> </h2>
    dataSplit = data.split(b'\n**')
    data = b'<h2>I asked Gemini: ""</h2>\n\n' + dataSplit.pop(0)
    for segment in dataSplit:
        splitPosition = segment.find(b'\n')
        if segment[splitPosition-2:splitPosition] != b'**':
            print("failed: expected **\\n not found at ", splitPosition, " in: ", segment)
            exit
        data += b'\n<h2>' + segment[:splitPosition-2] + b'</h2>' + segment[splitPosition:]

    # replace ** with <b> </b>
    dataSplit = data.split(b'**')
    data = b''
    Flag = False
    for segment in dataSplit:
        if Flag:
            Flag = False
            data += b'<b>' + segment + b'</b>'
        else:
            Flag = True
            data += segment

    # replace \n*  with <li> </li>
    dataSplit = data.split(b'\n* ')
    data = dataSplit.pop(0)         # not an <li>
    startLIgroup = True
    for segment in dataSplit:

        if startLIgroup:                 # first <li> in a list group
            startLIgroup = False
            data += b'\n<ul>'  
        
        # start of an <li>
        liItem = segment.split(b'\n',1)  # end of <ul> list@
        data += b'\n<li>' + liItem.pop(0) + b'</li>\n'
        if len(liItem) == 0:
            continue
        if liItem[0][:6] == b'    * ':
            liItem = liItem[0].split(b'\n')
            data += b'\n<ul>\n'
            while len(liItem) > 0:
                if liItem[0][:6] == "    * ":
                    data += b'<li>' + liItem.pop(0) + b'</li>\n'
                else:
                    break
            data += b'/ul>'
        if len(liItem) > 1:
            data += b'</ul>\n\n' + b'\n'.join(liItem)
            startLIgroup = True

    # all other lines not in html use <p> </p>
    dataSplit = data.split(b'\n')
    data = b''
    table = False
    for element in dataSplit:

        #if line not enclosed in html tags, then enclose it in <p> </p>
        if len(element) == 0 or element[:1] == b'<':
            data += element + b'\n'
        else:
            data += b'<p>' + element + b'</p>\n'

    with open(file, "wb") as f:
        f.write(data)
        
    print("conversion complete for ", file)

    return

if len(sys.argv) == 2:
    main(sys.argv[1])
else:
    import os
    fileList = glob.glob(os.path.dirname(sys.argv[0]) + "\\*.html")
    for cnt in range(len(fileList)):
        print(cnt," ", fileList[cnt])
    fileNum = -1
    while fileNum < 0 or fileNum > len(fileList):
        fileNum = int( input("enter #") )
    main( fileList[fileNum] )