import glob
import os
import sys
import random
import time
import numpy as np
import cv2


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

SHOW_PREVIEW = False
IM_WIDTH = 640
IM_HEIGHT = 480

class carEnv:
    SHOW_CAM = SHOW_PREVIEW
    STREET_AMT = 1.0
    im_width =IM_WIDTH
    im_height = IM_HEIGHT
    front_camera = None

    def __init__(self):
        self.client =carla.Client("localhost", 2000)
        self.client.set_timeout(2.0)
        self.world = self.client.get_world()
        blueprint_library = self.world.get_blueprint_library()
        self.model_3 = blueprint_library.filter("model3")[0]




def process_img(image):
    i = np.array(image.raw_data)
    #print(dir(image))
    #print(i.shape)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3] #entier height and width, rgb value
    cv2.imshow("", i3)
    cv2.waitKey(1)
    return i3/255.0






















