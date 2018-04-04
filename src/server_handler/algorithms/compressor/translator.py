
def get_id(session, args):
    session.GUI_socket.write_message({"set_id":session.id})


def enable_blade(session, args):
    session.GUI_socket.write_message({"enable_blade": args})


def position_z(session, args):
    session.GUI_socket.write_message({"set_z": session.z})

def get_profile(session, args):
    session.GUI_socket.write_message({"get_profile": session.profile})

def set_profile(session, args):
    session.GUI_socket.write_message({"get_profile": session.args})
    session.profile = args

def set_z(session, args):
    session.z = args
    session.GUI_socket.write_message({"set_z": session.z})

def set_camber(session, args):
    session.GUI_socket.write_message({"set_camber": args})