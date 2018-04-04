
from Rice.application import Application
import os
import platform
from definitions import SERVER

commands = __import__('miscellaneous.os_commands')
commands = commands.__dict__['os_commands'].__dict__[platform.system()]


def stage(session, args):
    """
    Args:
        :param args: [{profile_UP: [...],profile_DOWN:[...], r: float}, ..., name, Z]
    :param session:
    :param args:
    :return:
    """
    print('Generating blade')
    name = args[-2]
    z = args[-1]

    app = Application()
    #app.add_part()
    parts = app.get_parts()
    body = parts[0].get_bodies()
    body = body[0]
    name = args[-2]
    z = args[-1]
    args = args[:-2]

    list_profiles_up = [args[i]['profile_UP'] for i in range(len(args))]
    list_profiles_down = [args[i]['profile_DOWN'] for i in range(len(args))]
    spline_extrados = list()
    spline_intrados = list()
    list_z = [args[i]['r'] for i in range(len(args))]
    for i, n, j in zip(list_profiles_up, list_profiles_down, list_z):
        plane = parts[0].plane('Offset from plane', 'XY', j * 1000)
        sketch = body.add_sketch(plane)
        spline = sketch.spline2D([[p[0] * 1000, p[1] * 1000] for p in i])
        spline_extrados.append(spline)
        sketch2 = body.add_sketch(plane)

        spline2 = sketch2.spline2D([[i[0][0] * 1000, i[0][1] * 1000]] + [[p[0] * 1000, p[1] * 1000] for p in n] + [
            [i[-1][0] * 1000, i[-1][1] * 1000]])
        spline_intrados.append(spline2)

    spline_delante = parts[0].spline(
        [[args[i]['profile_UP'][0][0] * 1000, args[i]['profile_UP'][0][1] * 1000, args[i]['r'] * 1000] for i in
         range(len(args))])
    spline_detas = parts[0].spline(
        [[args[i]['profile_UP'][-1][0] * 1000, args[i]['profile_UP'][-1][1] * 1000, args[i]['r'] * 1000] for i in
         range(len(args))])
    # spline_attack = parts[0].spline(attack_points)
    fill = list()
    for i in range(len(spline_intrados) - 1):
        objs = list()
        objs.append(spline_delante)
        objs.append(spline_intrados[i])
        objs.append(spline_detas)
        objs.append(spline_intrados[i + 1])
        fill.append(parts[0].fill(objs))
        objs = list()
        objs.append(spline_delante)
        objs.append(spline_extrados[i])
        objs.append(spline_detas)
        objs.append(spline_extrados[i + 1])
        fill.append(parts[0].fill(objs))
    
    parts[0].update()
    join = parts[0].join(fill)
    parts[0].update()
    print('Blade Created')
    parts[0].export_data(os.path.join(session.abs_path, name), 'stl')
    #parts[0].circular_pattern(z, 360, join, 'X')
    """
    app = Application()

    parts = app.get_parts()
    part = parts[0]

    body = part.get_bodies()[0]

    sketch = body.add_sketch('xy')

    sketch.close_path([[0, 0], [50, 0], [50, 50], [0, 50]])

    pad = body.pad(sketch, 50)

    part.update()

    part.export_data(os.path.join(session.abs_path, name), 'stl')
    """
    session.socket_handler.send(({'enable_blade': ['{}/{}/sessions/{}/{}'.format(SERVER,session.algorithm, session.id, name +'.stl')]}))
