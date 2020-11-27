import threading
from PyQt5 import QtCore
# import gphoto2 as gp


class Intervalometer(threading.Thread, QtCore.QObject):

	def __init__(self, delay, exposure, interval, _count, parent):
		threading.Thread.__init__(self)
		QtCore.QObject.__init__(self, parent)

		self.delay = delay
		self.exposure = exposure
		self.interval = interval
		self.count = _count

		self.start()

	def run(self):
		camera = self.parent().window().camera
		config = self.parent().window().camera_config

		shutter = config.get_child_by_name("shutterspeed")
		old_shutter_speed = shutter.get_value()
		print(f"{old_shutter_speed=}")
		shutter.set_value("bulb")
		camera.set_config(config)

		remote = config.get_child_by_name("eosremoterelease")

		# TODO: add logging
		for i in range(self.count):
			remote.set_value("Immediate")
			camera.set_config(config)

			print(f"Starting Exposure {i+1}")
			while True:
				event, data = camera.wait_for_event(10000)
				if data == f"BulbExposureTime {exposure}":
					break

			remote.set_value("Release Full")
			camera.set_config(config)

			while True:
				event, data = camera.wait_for_event(10000)
				if event == gp.GP_EVENT_FILE_ADDED:
					# print(f"Exposure {str(i + 1)} saved as {data.folder}/{data.name}")
					break

			if i != self.count - 1:
				sleep(self.interval)
			else:
				shutter.set_value(old_shutter_speed)
				remote.set_value("None")
				camera.set_config(config)

		print("Finished")
