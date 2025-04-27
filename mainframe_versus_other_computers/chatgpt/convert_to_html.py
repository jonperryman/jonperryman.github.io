import sys

def main(file):
    file = ["", "mainframe_versus_other_computers\\chatgpt\\maximum_distance_between_mainframes"]
    with open(file[1], "rb") as f:
        dataSplit = f.read().split(b'**')
    
    # replace ## with <b> </b>
    data = b''
    Flag = False
    for segment0 in dataSplit:
        if Flag:
            Flag = False
            data += b'<b>' + segment0 + b'</b>'
        else:
            Flag = True
            data += segment0

    data = b''.join(data.split(b'\r'))      # remove carriage returns, we only use new lines \n

    # Replace ### with <h2> </h2>
    dataSplit = data.split(b'\n### ')
    data = dataSplit.pop(0)
    h2 = False
    for segment0 in dataSplit:
        splitPosition = segment0.find(b'\n')
        data += b'\n<h2>' + segment0[:splitPosition] + b'</h2>' + segment0[splitPosition:]

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

    dataSplit = data.split(b'\n')
    data = b''
    for element in dataSplit:
        if len(element) == 0 or element[:1] == b'<' or element[:1] == b' ':
            data += element + b'\n'
        else:
            data += b'<p>' + element + b'</p>\n'


    with open(file[1]+".html", "wb") as f:
        f.write(data)
    print(data)

print("running", sys.argv)

# main(sys.argv)