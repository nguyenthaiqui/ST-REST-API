'''
@author: Kabaji
@email: nguyenthaiqui233@gmail.com
@version: 1.0
@since: Feb 27, 2019
'''

import base64

def decodeText(filename1,filename2):
    f = open(filename1, "r")
    temp = f.readline()
    a = temp.encode("UTF-8")
    decoded = base64.b64decode(a)
    temp2 = str(decoded, encoding="UTF-8")

    f2 = open(filename2, 'w')
    f2.write(temp2)
