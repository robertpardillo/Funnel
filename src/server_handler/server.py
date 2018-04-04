# General imports statements ###############
import hashlib
import json
import os
import re
import random
import xml.etree.ElementTree as ET
import platform
from miscellaneous import os_commands

# Tornado utils ###############
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpclient
import tornado.httpserver
from tornado.options import define, options, parse_command_line

#       Script to receive and parse WebSocket connection.
#       Multi-threading option, Caution barely implemented, see documentation.
import definitions
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



# Global variable to recognize sessions
id_sessions = dict()

# Instantiate server IOLoop
_ioloop = tornado.ioloop.IOLoop()
_ioloop.current()

# Reading and establishing IP to all servers from IP.xml
from change_ip import change_handler_IP
abs_path = os.path.abspath('')
url = dict()

tree = ET.parse(os.path.join(abs_path, 'IP.xml'))
root = tree.getroot()
for i in root:
    url[i.tag] = i.find('ip').text

# Defining port
port = int(re.findall('.*:([1-9]*)', url[definitions.SERVER])[0])
define("port", default=port, help="run on the given port", type=int)


change_handler_IP(url['handler'])


class User(object):
    """

        Class to hand users

    """
    def __init__(self):
        self.name = ''
        self.sessions = list()

    def add_session(self, name, algorithm):
        global id_sessions
        session_id = self.id_session_assign()
        session = Session(name, algorithm, session_id, self)
        self.sessions.append({'{}'.format(session_id): session})
        id_sessions['{}'.format(session_id)] = session
        return session

    def id_session_assign(self):
        global id_sessions
        while True:
            id_ = random.randrange(0,10000000)
            if len("{}".format(id_))<8:
                id_ = "0"*(8-len("{}".format(id_)))+"{}".format(id_)
            else:
                id_ = "{}".format(id_)
            if id_ not in id_sessions:
                return id_
            else:
                continue


class Session(object):
    def __init__(self, name, algorithm, _id, user):
        self.name = name
        self.algorithm = algorithm
        self.user= user
        self.socket_design = socketClient.SocketDesign('ws://' + url['design'] + '/handler?id={}'.format(_id))
        self.socket_model3D = socketClient.SocketModel3D('ws://' + url['model3D'] + '/handler?id={}'.format(_id))
        self.socket_CFD = socketClient.SocketCFD('ws://' + url['CFD'] + '/handler?id={}'.format(_id))
        self.id = _id


if definitions.IS_MULTITHREADING:
    session = SharedClass(Session)
else:
    session = Session


class indexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        """

            Redirection from login to main page

        :param args:
        :param kwargs:
        :return:
        """

        id = self.get_argument("id", None, True)
        global id_sessions
        try: current_session = id_sessions['{}'.format(id)]
        except: current_session = None
        if not current_session:
            self.redirect('/login')
        elif current_session:
            self.render(os.path.join(os.path.abspath(''),'algorithms',current_session.algorithm, 'index.html'))


class get_from_other(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        spl = args[0].split('/')
        server = spl[0]
        path = spl[1:]
        _path = ''
        for i in path:
            _path+='{}/'.format(i)
        else:
            _path=_path[:-1]
        path='/algorithms/{}'.format(_path)
        print('http://' + url[server] + path)
        request = tornado.httpclient.HTTPRequest('http://' + url[server] + path)
        response = tornado.httpclient.HTTPClient().fetch(request)
        self.finish(response.body)


class loginHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('session.html')


class GUISocket(tornado.websocket.WebSocketHandler):
    """

        Class responsible of control socket's connections between Handler server and all the rest parts (web client,
        all the servers)

    """
    def open(self):
        id = self.get_argument("id", None, True)
        if not id:
            self.user = User()
            self.user.GUI_socket = self
        elif id:
            print('Loading User')
            self.current_session = id_sessions['{}'.format(id)]
            self.user = self.current_session.user
            self.current_session.GUI_socket = self
        print('Connection Opened')

    def on_message(self, message):
        json_string = u'%s' %(message)
        msg = json.loads(json_string)
        receiver = msg['receiver']
        try:algorithm = msg['algorithm']
        except: algorithm = None
        if receiver=='handler':
            key = list(msg['method'].keys())[0]
            if algorithm!='session':
                translator = \
                __import__('algorithms.{}.translator'.format(algorithm)).__dict__['{}'.format(algorithm)].__dict__[
                    'translator']
                translator.__dict__[key](self.current_session, msg['method'][key])
            else:
                self.__getattribute__(key)(msg['method'][key])


        else:
            self.current_session.__dict__['socket_{}'.format(receiver)].resend(msg)

    def what_algorithms(self, *args):
        algorithms = list(os.walk(algorithms_path))[0][1]
        self.write_message({"algorithms":algorithms})

    def new_session(self, name):
        abs_path = os.path.abspath('')
        algorithm = name[1]
        name = name[0]
        self.current_session = self.user.add_session(name, algorithm)
        self.current_session.session_path = os.path.join(abs_path, 'algorithms',algorithm,'sessions','{}'.format(self.current_session.id))
        exists = os.path.exists(self.current_session.session_path)
        if not exists:
            os.system(r'{} {}'.format(commands['mkdir'], self.current_session.session_path))
            self.current_session.socket_model3D.send(None, {"session_name": [1, name, algorithm]})
            self.current_session.socket_design.send(None, {"session_name": [1, name, algorithm]})
            self.current_session.socket_CFD.send(None, {"session_name": [1, name, algorithm]})
            self.write_message({"session_check": 1}, binary=False)
            self.write_message({"id_info": self.current_session.id}, binary=False)
        else:

            self.current_session.socket_model3D.send({"session_name": [0, name, algorithm]})

            self.current_session.socket_design.send({"session_name": [0, name, algorithm]})

            self.current_session.socket_CFD.send({"session_name": [0, name, algorithm]})

            self.write_message({"session_check": 1}, binary=False)
            self.write_message({"id_info": self.user.id}, binary=False)

    def check_session(self, name):
        abs_path = os.path.abspath('')
        session_path = os.path.join(abs_path,'sessions','{}_{}'.format(self.user.id, name))
        exists = os.path.exists(session_path)
        if exists:
            print('Loading ....')
            self.write_message({"session_check": 1}, binary=False)
            self.write_message({"id_info": self.user.id}, binary=False)
            self.user.sessioned = True
            self.user.session_name = name
            self.user.session_path = session_path
        else:
            self.write_message({"session_check": 0}, binary=False)
            self.user.session_name = name

    def check_user(self, args):

        user = args[0]
        passw = args[1]
        if user=='guest':
            self.write_message({"check_user": 2}, binary=False)
            self.user.name = user
            self.user.logged = True
            return None

        abs_path = os.path.abspath('')
        try:
            f = open(os.path.join(abs_path, 'static', 'user_pass', '{}.pass'.format(user)), 'r')
            passw_check = f.read()
            f.close()
        except:
            self.write_message({"check_user": 0}, binary=False)
            return None

        passw = hashlib.sha224(passw.encode()).hexdigest()
        if passw == passw_check:
            self.write_message({"check_user": 1}, binary=False)
            return None
        else:
            self.write_message({"check_user": 0}, binary=False)
            return None
        pass

    def on_close(self):
        print('User {} disconnected'.format(self.current_session.id))

    def send_web(self, data):
        self.write_message(data, binary=False)

    def add_algorithm(self, args):
        print(args)


class SocketDesign(base_sockets.SocketDesign):

    def open(self):
        super(SocketDesign, self).open(id_sessions, session)


class SocketCFD(base_sockets.SocketCFD):

    def open(self):
        super(SocketCFD, self).open(id_sessions, session)


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
        try:
            algorithm = msg['algorithm']
        except:
            algorithm = None
        if receiver == 'handler':
            key = list(msg['method'].keys())[0]
            self.__getattribute__(key)(msg['method'][key])

    def init_file(self, args):
        args=args[0]
        self.file = open('{}'.format(args['file_name']), 'ab+')
        self.file.write(bytearray([i for i in args['file']]))
        self.file.close()
        self.write_message('Sent')
        self.redistribute_algorithm(args['file_name'])

    def redistribute_algorithm(self, name):
        self.socket_design = socketClient.SocketDesign('ws://' + url['design'] + '/upload')
        self.socket_model3D = socketClient.SocketModel3D('ws://' + url['model3D'] + '/upload')
        self.socket_CFD = socketClient.SocketCFD('ws://' + url['CFD'] + '/upload')

        zip_path = str()
        _system = platform.system().lower()
        if _system=='windows':
            program = os.environ.get('ProgramFiles')
            programx86 = os.environ.get('ProgramFiles(x86)')
            if os.path.exists(os.path.join(program, '7-Zip')):
                zip_path = os.path.join(program, '7-Zip', '7z')
            elif os.path.exists(os.path.join(programx86, '7-Zip')):
                zip_path = os.path.join(programx86, '7-Zip', '7z')
            else:
                print('Install 7-Zip')
            zip_path = r'"{}"'.format(zip_path)
        elif _system=='linux':
            zip_path = '/usr/bin/unzip'
            if os.path.exists(zip_path):
                pass
            else:
                zip_path = input('Introduce unzip command path or install it')
                if zip_path == "": exit(0)

        unzip_func = os_commands.__dict__['unzip_{}'.format(_system)]
        unzip_func(name, name[0:-4], zip_path,'e')
        name = name[0:-4]
        for i in list(os.walk(os.path.join(os.path.abspath(''), name)))[0][2]:
            name_ = i.split('.')[0]
            if name_=='handler':
                unzip_func(os.path.join(os.path.abspath(''), name, name_+'.zip'), os.path.join(os.path.abspath(''),'algorithms',name),zip_path,'x')
                #os.system('{} x -y {}.zip -o{}'.format(zip_path, os.path.join(os.path.abspath(''), name, name_),
                                                   # os.path.join(os.path.abspath(''),'algorithms',name)))
            else:
                file = open('{}.zip'.format(os.path.join(os.path.abspath(''),name,name_)),'rb')
                data = file.read()
                file.close()
                self.__getattribute__('socket_{}'.format(name_)).send(None, {'init_file':[{'file_name': name, 'file': [i for i in data]}]})

        os_commands.__dict__['rmDir_{}'.format(_system)](name)
        os_commands.__dict__['rmFile_{}'.format(_system)](name+'.zip')

    def on_close(self):
        print('connection close')


class AlexaListener(base_sockets.AlexaSocket):
    def open(self):
        super(AlexaListener, self).open(id_sessions, session)


algorithms_path = os.path.join(os.path.abspath(''), 'algorithms')
static_paths = list()
for i in list(os.walk(algorithms_path))[0][1]:
    static_paths.append((r'/algorithms/{}/static/(.*)'.format(i), tornado.web.StaticFileHandler, {'path':r'{}'.format(os.path.join(algorithms_path, i, 'static'))}))

static_path = os.path.join(os.path.abspath(''), 'static')
app = tornado.web.Application([(r'/', indexHandler),(r'/login', loginHandler), (r'/user/ws', GUISocket), (r'/get_from_other/(.*)', get_from_other),
                               (r'/design', SocketDesign), (r'/CFD', SocketCFD),(r'/model3D', SocketModel3D),
                               (r'/alexa', AlexaListener), (r'/upload', UploadAlg),
                               (r'/static/(.*)', tornado.web.StaticFileHandler, {'path' : r'{}'.format(static_path)}), *static_paths])

"""
algorithms_path = os.path.join(os.path.abspath(''), 'algorithms')
index_handlers = list()
static_paths = list()
for i in list(os.walk(algorithms_path))[0][1]:
    #index_handlers.append((r'/{}'.format(i), vars()['{}Handler'.format(i)]))
    static_paths.append((r'/{}/static/(.*)'.format(i), tornado.web.StaticFileHandler, {'path':r'{}'.format(os.path.join(algorithms_path, i, 'static'))}))
print(index_handlers)
print(static_paths)
print(vars()['designSocket'])c
"""
if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)

_ioloop.start()
