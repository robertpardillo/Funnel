import tornado.websocket
import json

import definitions

SERVER = definitions.SERVER


class SuperBaseSocket(tornado.websocket.WebSocketHandler):
    def open(self, id_sessions, Session):
        _id = self.get_argument("id", None, True)
        if not _id:
            self.current_session = Session()
        elif _id:
            try : self.current_session = id_sessions['{}'.format(_id)]
            except: self.current_session = None
            if self.current_session:
                pass
            else:
                self.current_session = Session(_id)

                id_sessions['{}'.format(_id)] = self.current_session

    def on_message(self, message):
        json_string = u'%s' % (message)
        message = json.loads(json_string)
        receiver = message['receiver']
        algorithm = message['algorithm']
        method = message['method']
        key = list(method.keys())[0]
        if receiver == SERVER:
            if algorithm:
                translator = __import__('algorithms.{}.translator'.format(algorithm)).__dict__['{}'.format(algorithm)].__dict__['translator']
                translator.__dict__[key](self.current_session, method[key])
            else:
                self.__getattribute__(key)(method[key])
        else:
            self.current_session.__getattribute__('socket_{}'.format(receiver)).send(message)
        self.write_message('Sent')

    def on_close(self):
        pass


class SocketCFD(SuperBaseSocket):
    def open(self, id_sessions, Session):
        super(SocketCFD, self).open(id_sessions, Session)
        print('CFD connection open')

    def on_close(self):
        print('Closing CFD connection')


class SocketModel3D(SuperBaseSocket):
    def open(self, id_sessions, Session):
        super(SocketModel3D, self).open(id_sessions, Session)
        print('3D connection open')

    def on_close(self):
        print('Closing 3D connection')


class SocketDesign(SuperBaseSocket):
    def open(self, id_sessions, Session):
        super(SocketDesign, self).open(id_sessions, Session)
        print('Design connection open')

    def on_close(self):
        print('Closing Design connection')


class SocketHandler(SuperBaseSocket):
    def open(self, id_sessions, Session):
        super(SocketHandler, self).open(id_sessions, Session)
        print('Handler connection open')

    def on_close(self):
        print('Closing Handler connection')