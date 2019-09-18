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
        #self.blueprint_library = self.world.get_blueprint_library()
        blueprint_library = self.world.get_blueprint_library()
        self.model_3 = blueprint_library.filter("model3")[0]


        def reset(self):
            self.collision_list =[]
            self.actor_list = []

            self.transform = random.choice(self.world.get_map().get_spawn_points())
            self.vehicle = self.world.spawn_actor(self.model_3, self.transform)
            self.actor_list.append(self.vehicle)

            self.rgb_cam = self.blueprint_library.find('sensor_camera.rgb')
            self.rgb.set_attribute("image_size_x", f"{self.im_width}")
            self.rgb.set_attribute("image_size_y", f"{self.im_height}")
            self.rgb.set_attribute("fov", f"110")

            transform = carla.Transorm(carla.Location(x=2.5, z=0.7))
            self.sensor = self.world.spawn_actor(self.rgb_cam, transform, attach_to = self.vehicle)
            self.actor_list.append(self.sensor)
            self.sensor.listen(lambda data:self.process_img(data))

            self.vehicle.apply_control(carla.VehicleControl(throttle= 0.0, breke= 0.0))
            time.sleep(4)

            colsensor = self.blueprint_library.find("sensor.other.collision")
            self.colsensor = self.world.spawn_actor(colsensor, transform, attach_to=self.vehicle)
            self.actor_list.append(self.colsensor)
            self.colsensor.listen(lambda event: self.colsensor_data(event))

            while self.front_camera is None:
                time.sleep(0.01)

            self.episode_strat = time.time()

            self.vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=0.0))

            return  self.front_camera

        def colsensor_data(self, event):
            self.collision_list.append(event)

        def process_img(self,image):
            i = np.array(image.raw_data)
            # print(dir(image))
            # print(i.shape)
            i2 = i.reshape((IM_HEIGHT , IM_WIDTH , 4))
            i3 = i2[: , : , :3]  # entier height and width, rgb value
            
            cv2.imshow("" , i3)
            cv2.waitKey(1)
            return i3 / 255.0






























