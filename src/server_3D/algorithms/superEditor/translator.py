
from collections import deque
import threading


def execute_block(session, args):

    try: env = session.env
    except:
        session.env = Environment(session)
        env = session.env
    env.deque.append(args)


class Environment(object):
    def __init__(self, session):
        self.t = threading.Thread(target=self.main)
        self.deque = deque()
        self.is_imported = False
        self.t.start()
        self.session = session

    def main(self):
        while True:
            try:operation = self.deque.popleft()
            except:
                continue
            if not self.is_imported:
                from API.Rice.application import Application
                self.is_imported = True

            args_dict = operation[1]
            for i in args_dict:
                if i=='return_values' or i=='index' or i=='receiver':
                    continue
                exec(compile("{}={}".format(i, args_dict[i]), "<string>", 'exec'))
            exec(compile(operation[0], "<string>", 'exec'))

            return_list = list()
            if not operation[1]['return_values'] == "":
                for i in operation[1]['return_values'].split(','):
                    return_list.append(eval(i))
            self.session.__getattribute__('socket_{}'.format(args_dict['receiver'])).send({"response_blocks": [operation[1]['index']]+return_list})


