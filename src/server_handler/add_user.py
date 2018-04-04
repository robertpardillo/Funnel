
import sys
import os
import hashlib


def help():
    string="""\nAdd user to use PyBaDE.\n
    Usage:  add_user user password\n"""
    print(string)
    sys.exit()

try:
    user = sys.argv[1]
    if user=='-help':
        help()
    else:
        pass
except IndexError:
    help()

try:
    password = sys.argv[2].encode()
except IndexError:
    help()

abs_path = os.path.abspath('')
f = open(os.path.join(abs_path, 'static', 'user_pass','{}.pass'.format(user)), 'w')
print('Encoding ....')

password = hashlib.sha224(password).hexdigest()
f.write(password)
f.close()
print('User Created')

