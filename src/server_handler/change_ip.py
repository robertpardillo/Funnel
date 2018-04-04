
import re


def change_handler_IP(new_ip):

    with open('static/js/webSocket.js', 'r+') as f:
        text0 = f.read()
        string = '// IP \nvar IP = "{}";'.format(new_ip)
        text=re.sub('.*//.*IP.*\\n.*var.*IP.*=.*', string,text0)
        f.seek(0)
        f.write(text)
        f.close()



