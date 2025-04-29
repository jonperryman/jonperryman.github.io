import sys

def main(file):

    print("converting ", file, "to html")
    
    if file[-5:] != ".html":
        print("failed: ",file," must be an HTML file type")
        return

    with open(file, "rb") as f:
        dataSplit = f.read().split(b'**')

    if dataSplit[0][:1] == "<":
        print("failed: file ", file, " appears to be converted")
        return

    # replace ## with <b> </b>
    data = b'<h2>I asked ChatGPT: ""</h2>\n\n'
    Flag = False
    for segment0 in dataSplit:
        if Flag:
            Flag = False
            data += b'<b>' + segment0 + b'</b>'
        else:
            Flag = True
            data += segment0

    data = b''.join(data.split(b'\r'))      # remove carriage returns, we only use new lines \n
    data = b'\n'.join([line.strip() for line in data.split(b'\n')])

    # Replace ### with <h2> </h2>
    dataSplit = data.split(b'\n#')
    data = dataSplit.pop(0)
    for segment0 in dataSplit:
        splitPosition = segment0.find(b'\n')
        data += b'\n<h2>' + segment0[:splitPosition].split(b' ',1)[1] + b'</h2>' + segment0[splitPosition:]

    data = b''.join(data.split(b'\n---\n')) # remove useless sepeerator line

    # replace \n- with <li> </li>
    dataSplit = b'\n-'.join(data.split(b'\n\n-')).split(b'\n-')      # remove preceeding blank line on <li> itemscarriage returns, we only use new lines \n
    data = dataSplit.pop(0)         # not an <li>
    startLIgroup = True
    while len(dataSplit) > 0:

        if startLIgroup:                 # first <li> in a list group
            startLIgroup = False
            data += b'\n<ul>'  
        
        # start of an <li>
        liItem = dataSplit.pop(0).split(b'\n\n',1)  # end of <ul> list@
        data += b'\n<li>' + b'<br/>\n'.join(liItem[0].split(b'\n')) + b'</li>\n'
        if len(liItem) == 2:
            data += b'</ul>\n\n' + liItem[1]
            startLIgroup = True

    # all other lines not in html use <p> </p>
    dataSplit = data.split(b'\n')
    data = b''
    table = False
    for element in dataSplit:

        # process table lines
        if element[:1] == b'|':
            work = element.split(b'|')
            work.pop(0)   # remove non-table blanks
            work.pop(-1)         # remove non-table blanks
            element = b'<tr><td>' + b'</td><td>'.join( work ) + b'</td></tr>'
            if not table:
                element = b'<table>\n' + element
            table = True
        elif table:
            data += b'</table>\n'
            table = False

        #if line not enclosed in html tags, then enclose it in <p> </p>
        if len(element) == 0 or element[:1] == b'<':
            data += element + b'\n'
        else:
            data += b'<p>' + element + b'</p>\n'

    with open(file, "wb") as f:
        f.write(data)
        
    print("conversion complete for ", file)

    return

main(sys.argv[1])