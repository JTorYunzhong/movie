import sqlite3
import string

def visual():
    '''Word cloud visualization of movie plot data 
        -------------------
        
        Returns
        -------
    
    '''
    conn = sqlite3.connect('info.sqlite')
    cur = conn.cursor()

    cur.execute('SELECT Id, Plot FROM Movies')
    if cur == None:
        print("Empty database. Please stor more data and try again")
        return
    plots = dict()
    for a_row in cur :
        plots[a_row[0]] = a_row[1]

    counts = dict()
    for key in plots :
        text = plots[key]
        if text == None:
            continue
        text = text.translate(str.maketrans('','',string.punctuation))
        text = text.translate(str.maketrans('','','1234567890'))
        text = text.strip()
        text = text.lower()
        words = text.split()
        for word in words:
            if len(word) < 4 : continue
            counts[word] = counts.get(word,0) + 1

    x = sorted(counts, key=counts.get, reverse=True)
    highest = None
    lowest = None
    for k in x[:100]:
        if highest is None or highest < counts[k] :
            highest = counts[k]
        if lowest is None or lowest > counts[k] :
            lowest = counts[k]
    print('Range of counts:',highest,lowest)

    # Spread the font sizes across 20-100 based on the count
    bigsize = 80
    smallsize = 20

    fhand = open('word_visual.js','w')
    fhand.write("word_visual = [")
    first = True
    for k in x[:100]:
        if not first : fhand.write( ",\n")
        first = False
        size = counts[k]
        size = (size - lowest) / float(highest - lowest)
        size = int((size * bigsize) + smallsize)
        fhand.write("{text: '"+k+"', size: "+str(size)+"}")
    fhand.write( "\n];\n")
    fhand.close()

    print("Output written to word_visual.js")
    print("Open word_visual.html in a browser to see the vizualization")
