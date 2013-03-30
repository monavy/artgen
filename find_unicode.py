text = ''
count = 1
for line in open('source_text.txt'):
    line = line.strip()

    char = 0
    for c in line:
        char += 1
        try:
            text += c.encode('ascii')
        except:
            print count, char

    count += 1
