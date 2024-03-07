#!/usr/bin/env python3
# Author: Jonathan Külz
# Date: 25.05.22
# Resource: https://www.zimmer-group.com/de/technologien-komponenten/komponenten/handhabungstechnik/greifer/elektrisch/2-backen-parallelgreifer/serie-gep2000/produkte/gep2010io-00-b
from argparse import ArgumentParser
from pathlib import Path
import sys

import numpy as np
import pinocchio as pin

height = 78 / 1000
width = 53.8 / 1000
depth = 26 / 1000
finger_height = (99.5 - 78) / 1000
lever = None

parser = ArgumentParser()
parser.add_argument('-mcs', help='mcs source directory', type=str, required=True)


def get_inertia():
    """
    Approximates inertia by assuming mass is evenly distributed and the gripper body is basically a box
    Data taken from https://www.zimmer-group.com/fileadmin/pim/MER/GD/PG/MER_GD_PG_GEP2010IL-00-B__SDE__APD__V1.pdf
    Assumes Body coordinate system to be in the center of the "main body" of the gripper, with:
        - z-Axis pointing towards the fingers
        - x-Axis pointing to the right side (side with the plug for power and signal input)
        - y-Axis determined by x&z to build a right handed coordinate system
    """
    global lever
    mass = 0.31  # kg
    i_xx = 1 / 12 * mass * (height ** 2 + depth ** 2)
    i_yy = 1 / 12 * mass * (height ** 2 + width ** 2)
    i_zz = 1 / 12 * mass * (width ** 2 + depth ** 2)
    inertia = np.asarray(((i_xx, 0, 0), (0, i_yy, 0), (0, 0, i_zz)), dtype=float)
    return pin.Inertia(mass, lever[:3, 3], inertia)


def main():
    from Bodies import Body, Connector, Gender
    from Module import AtomicModule, ModuleHeader, ModulesDB, ModuleAssembly
    from task.Obstacle import MeshObstacle
    from utilities import file_locations, spatial
    global lever
    lever = spatial.homogeneous(translation=(0., 0., height / 2))
    # TODO: Gripper is still missing mounting adapter
    in_connector = Connector(
        connector_id='gripper_in',
        body2connector=spatial.inv_homogeneous(lever) @ spatial.rotX(np.pi),
        gender=Gender.f,
        connector_type='clamp',  # Same as modrob gen 2
        size=80
    )
    eef_connector = Connector(
        connector_id='between_fingers',
        body2connector=lever @ spatial.homogeneous(translation=(0, 0, finger_height / 2)),
        gender=Gender.m,
        connector_type='eef'
    )
    collision_object = MeshObstacle.from_crok_description(
        geometry={'file': 'meshfiles/GEP2010IO-00-B(010).stl', 'scale': 1 / 1000},
        package_dir=Path('/home/jonathan/tmp/modrob-gen2/'),
        ID='GEP2010IO', name='Zimmer GEP2010IO',
        acknowledgement='https://www.zimmer-group.com/de/technologien-komponenten/komponenten/handhabungstechnik/greifer/elektrisch/2-backen-parallelgreifer/serie-gep2000/produkte/gep2010io-00-b',
        pose=spatial.inv_homogeneous(lever) @ spatial.rotX(-np.pi / 2)
    )
    main_body = Body(
        body_id='main_body',
        connectors=(in_connector, eef_connector),
        inertia=get_inertia(),
        collision=collision_object,
        visual=None
    )


    header = ModuleHeader(ID='GEP2010IL', name=' Zimmer Gripper', author=['Jonathan Külz'])
    zimmer = AtomicModule(header, bodies=(main_body,))

    db = ModulesDB.from_name('modrob-gen2').filter(lambda m: m.id != 'GEP2010IL')
    db.add(zimmer)
    save_as = Path('modules.json')
    db.to_json(save_as)


if __name__ == '__main__':
    print("Warning! Only works if executed in the modrob-gen2 directory")
    args = parser.parse_args()
    sys.path.append(args.mcs)
    main()

