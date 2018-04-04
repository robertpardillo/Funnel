
import re
import threading


def parse_text(session, args):
    bytes_list = args[0].split(',')
    bytes_array = bytearray([int(i) for i in bytes_list]).decode()
    sentences = bytes_array.split('\n')
    var_dict = dict()
    executable_file = ''

    for i in range(3):
        try:result_apis = re.findall("^(.*) += *(.*)\('(.*)'\)", sentences[i])[0]
        except:break
        if result_apis[1] == 'GetModel3D':
            model_name = [result_apis[0], result_apis[2]]
        elif result_apis[1] == 'GetSimulation':
            simulation_name = [result_apis[0], result_apis[2]]
    in_block=False
    blocks = list()
    session.blocks = blocks
    for i in range(3,len(sentences)):
        sentence = sentences[i]
        server_result = re.findall("(\t*)(.*) \((.*)\) {}".format('{'), sentence)
        if len(server_result)>0:
            in_block = True
            sentences_block = ''
            current_args = ''
            current_sep = server_result[0][0]
            if server_result[0][1]==model_name[0]:
                current_block = Block('model3D', model_name[1], session, blocks)
            elif server_result[0][1]==simulation_name[0]:
                current_block = Block('CFD', simulation_name[1],session, blocks)
            if len(server_result[0][2].split(','))>0:
                current_args = server_result[0][2]
                current_block.set_args(current_args)
            current_block.return_string = ''
            current_block.return_values = ''
            continue
        if re.search(".*}.*", sentence):
            in_block=False
            current_block.set_string(sentences_block)
            blocks.append(current_block)
            index = blocks.index(current_block)
            executable_file += current_sep + current_block.return_string + "blocks[{}]({})\n".format(index, current_args)
            continue
        elif re.search('.*return \((.*)\)',sentence):
            current_block.return_values = re.findall('.*return \((.*)\)', sentence)[0]
            current_block.return_string = re.findall('.*return \((.*)\)', sentence)[0]+"," + " = "
            continue
        if in_block:
            sentences_block += sentence+'\n'
            continue
        executable_file += sentence + "\n"

    t = threading.Thread(target=run_exec, name='Execute',args=(executable_file,blocks))
    t.start()


def run_exec(executable_file, blocks):
    blocks = blocks
    exec(compile(executable_file, '<string>', 'exec'))


class Block(object):
    def __init__(self, server, API, session, blocks_list):
        self.server = server
        self.API = API
        self.session = session
        self.blocks_list = blocks_list
        self.return_values = None

    def set_string(self, string):
        self.block_string = string

    def set_args(self, args):
        self.args = args

    def __call__(self, *args):
        self.run_thread(*args)
        self.flag = True
        while self.flag:
            import time

            time.sleep(5)
            pass
        return self.return_values

    def run_thread(self, *args):
        var_dict = dict()
        index = self.blocks_list.index(self)
        if len(args)>0:
            args_name = self.args.split(',')
            for i in range(len(args_name)):
                if isinstance(args[i], str):
                    var_dict['{}'.format(args_name[i])] = "'" + args[i] + "'"
                else:
                    var_dict['{}'.format(args_name[i])] = args[i]
        var_dict['return_values'] = self.return_values
        var_dict['index'] = index
        var_dict['receiver'] = 'design'

        socket = self.session.__getattribute__('socket_{}'.format(self.server))

        socket.send({'execute_block': [self.block_string, var_dict]})


def response_blocks(session, args):
    session.blocks[args[0]].return_values = args[1::]
    session.blocks[args[0]].flag = False


class Model3DVar(object):
    def __init__(self, session, API):
        self.session = session
        self.API = API


class SimulationVar(object):
    def __init__(self, session, API):
        self.session = session
        self.API = API
