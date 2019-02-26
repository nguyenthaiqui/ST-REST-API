import base64

def decodeText(filename1,filename2):
    f = open(filename1, "r")
    temp = f.readline()
    a = temp.encode("UTF-8")
    decoded = base64.b64decode(a)
    temp2 = str(decoded, encoding="UTF-8")

    f2 = open(filename2, 'w')
    f2.write(temp2)
