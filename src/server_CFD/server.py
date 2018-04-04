# General imports statements ###############
import os
import platform
import json
import re
import xml.etree.ElementTree as ET
from miscellaneous import os_commands

# Tornado utils ###############
import tornado.web
from tornado.options import define, options, parse_command_line

# Global variables #########################
import definitions

#       Script to receive and parse WebSocket connection.
#       Multi-threading option, Caution barely implemented, view documentation
is_multi = definitions.IS_MULTITHREADING
if is_multi:
    base_sockets = __import__('base_socketsM')
else:
    base_sockets = __import__('base_sockets')
from sharedClass import SharedClass

#       Script for socket client powers.
socketClient = __import__('socketClient')

#       Generalize commands on windows and linux
commands = __import__('miscellaneous.os_commands')
commands = commands.__dict__['os_commands'].__dict__[platform.system()]

#       Defining some server features


# Dictionary saving all initiated session
id_sessions = dict()

# Starting main loop of server
_ioloop = tornado.ioloop.IOLoop()
_ioloop.make_current()

# Reading and setting server's IP
url = dict()

abs_path = os.path.abspath('..')
handler_ip_path = os.path.join(abs_path, 'server_handler', 'IP.xml')
if os.path.exists(handler_ip_path):
    ip_path = handler_ip_path
else:
    ip_path = os.path.join(os.path.abspath(''), 'IP.xml')


tree = ET.parse(ip_path)
root = tree.getroot()
for i in root:
    url[i.tag] = i.find('ip').text

# Defining port
port = int(re.findall('.*:([1-9]*)', url['CFD'])[0])
define("port", default=port, help="run on the given port", type=int)


class Session(object):
    def __init__(self, _id):
        self.socket_handler = socketClient.SocketHandler('ws://' + url['handler'] + '/CFD?id={}'.format(_id))
        self.socket_design = socketClient.SocketDesign('ws://' + url['design'] + '/CFD?id={}'.format(_id))
        self.socket_model3D = socketClient.SocketModel3D('ws://' + url['model3D'] + '/CFD?id={}'.format(_id))
        self.socket_CFD = socketClient.SocketCFD('ws://' + url['CFD'] + '/CFD?id={}'.format(_id))
        self.id = _id

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm):
        self._algorithm = algorithm
        self.socket_design.algorithm = algorithm
        self.socket_model3D.algorithm = algorithm
        self.socket_CFD.algorithm = algorithm
        self.socket_handler.algorithm = algorithm


if definitions.IS_MULTITHREADING:
    session = SharedClass(Session)
else:
    session = Session


class SocketHandler(base_sockets.SocketHandler):

    def open(self):

        super(SocketHandler, self).open(id_sessions, session)

    def session_name(self, args):
        flag = args[0]
        name = args[1]
        algorithm = args[2]
        self.current_session.algorithm = algorithm
        self.current_session.name = name
        self.current_session.abs_path = os.path.join(os.path.abspath(''), 'algorithms', '{}'.format(algorithm), 'sessions', '{}'.format(self.current_session.id))
        if flag:
            os.system(r'{} {}'.format(commands['mkdir'], self.current_session.abs_path))
        else:
            pass


class SocketDesign(base_sockets.SocketDesign):
    def open(self):
        super(SocketDesign, self).open(id_sessions, session)


class SocketModel3D(base_sockets.SocketModel3D):
    def open(self):
        super(SocketModel3D, self).open(id_sessions, session)


class UploadAlg(tornado.websocket.WebSocketHandler):

    def open(self):
        print('connection')

    def on_message(self, message):
        json_string = u'%s' % (message)
        msg = json.loads(json_string)
        receiver = msg['receiver']
        key = list(msg['method'].keys())[0]
        self.__getattribute__(key)(msg['method'][key])

    def init_file(self, args):
        args = args[0]
        self.file = open('{}.zip'.format(args['file_name']), 'ab+')
        self.file.write(bytearray([i for i in args['file']]))
        self.file.close()
        self.write_message('Sent')

        zip_path = str()
        _system = platform.system().lower()
        if _system == 'windows':
            program = os.environ.get('ProgramFiles')
            programx86 = os.environ.get('ProgramFiles(x86)')
            if os.path.exists(os.path.join(program, '7-Zip')):
                zip_path = os.path.join(program, '7-Zip', '7z')
            elif os.path.exists(os.path.join(programx86, '7-Zip')):
                zip_path = os.path.join(programx86, '7-Zip', '7z')
            else:
                print('Install 7-Zip')
            zip_path = r'"{}"'.format(zip_path)
        elif _system == 'linux':
            zip_path = '/usr/bin/unzip'
            if os.path.exists(zip_path):
                pass
            else:
                zip_path = input('Introduce unzip command path or install it')
                if zip_path == "": exit(0)

        name = args['file_name']

        os_commands.__dict__['unzip_{}'.format(_system)](os.path.join(os.path.abspath(''), name + '.zip'),
                                                         os.path.join(os.path.abspath(''), 'algorithms', name),
                                                         zip_path, 'x')
        os_commands.__dict__['rmFile_{}'.format(_system)](name + '.zip')

algorithms_path = os.path.join(os.path.abspath(''), 'algorithms')
static_paths = list()
for i in list(os.walk(algorithms_path))[0][1]:
    static_paths.append((r'/algorithms/{}/sessions/(.*)'.format(i), tornado.web.StaticFileHandler, {'path':r'{}'.format(os.path.join(algorithms_path, i, 'sessions'))}))

static_path = os.path.join(os.path.abspath(''), 'static')
app = tornado.web.Application([(r'/handler', SocketHandler), (r'/design', SocketDesign), (r'/model3D', SocketModel3D),
                               (r'/upload', UploadAlg), *static_paths])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)

_ioloop.start()
