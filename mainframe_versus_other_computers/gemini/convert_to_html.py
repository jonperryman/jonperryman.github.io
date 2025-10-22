# VSCODE ctrl-1 invokes this script against the Gemini responses saved in the current file

import sys
import glob
import re

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

    # create <h3> </h3>
    dataSplit = data.split(b'\n**')
    data = dataSplit.pop(0)
    for segment in dataSplit:
        work = segment.split(b'**',1)
        if work[1].split(b'\n')[0].strip() == b'':
            data += b'\n<h3>' + work[0] + b'</h3>' + work[1]
        else:
            data += b'\n**' + segment

    # replace ** with <b> </b>
    dataSplit = data.split(b'**')
    data = dataSplit.pop(0)
    cnt = 0
    while cnt < len(dataSplit):
        data += b'<b>' + dataSplit[cnt] + b'</b>' + dataSplit[cnt+1]
        cnt += 2

    # handle tables 
    dataSplit = data.split(b'```')
    data = dataSplit.pop(0)
    while len(dataSplit) != 0:
        segments = dataSplit.pop(0).split(b'\n')
        data += b'<table style="border: 1px solid;"><tr style="border: 1px solid; background-color: lightgreen;"><td>' + segments.pop(0) + b'</td></tr>'
        for segment in segments:
            data += b'<tr><td>' + segment + b'</td></tr>'
        data += b'</table>\n'

        data += dataSplit.pop(0)

    # replace \n*  with <li> </li>
    dataSplit = data.split(b'\n')
    if dataSplit[0][:4] == b'<h2>':
        data = dataSplit.pop(0)
    else:
        data = b'<h2>I asked Gemini: ""</h2>\n'
    liLevel = -4
    startLI = False
    for line in dataSplit:

        if line == b'':
            data += b'\n'
            continue
    
        indentation = re.match(b'^ *', line).span()[1]
        indentChar = line[indentation:indentation+1]

        if indentChar == b'*':
            if liLevel < indentation:
                if indentation - liLevel != 4:
                    print("failed: invalid indentation: ", line)
                    exit()
                data += b'\n<ul>\n<li>' + line[indentation+1:]
                liLevel = indentation
            else:
                data += b'</li></ul>' * int( (liLevel - indentation)/4 )
                data += b'</li>\n<li>' + line[indentation+1:]
            
            liLevel = indentation
            continue

        if liLevel >= indentation:
            data += b'</li></ul>' * int( (liLevel + 4 - indentation)/4 )
            liLevel = indentation - 4
        
        if line[:4] == b'<h3>':
            data += b'\n' + line 
        else:
            data += b'\n<p>' + line + b'</p>'

    data = b'\n\n'.join( data.split(b'\n\n\n') )
    data = b'</tr>\n'.join( data.split(b'</tr>') )

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