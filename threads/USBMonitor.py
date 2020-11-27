import pyudev
import threading
from PyQt5 import QtCore


class USBMonitor(threading.Thread, QtCore.QObject):

	usb_connected = QtCore.pyqtSignal()
	usb_disconnected = QtCore.pyqtSignal()

	def __init__(self):
		threading.Thread.__init__(self, target=self._work)
		QtCore.QObject.__init__(self)
		self.daemon = True

		self.start()

	def _work(self):
		self.context = pyudev.Context()
		self.monitor = pyudev.Monitor.from_netlink(self.context)
		self.monitor.filter_by(subsystem="usb")

		for device in iter(self.monitor.poll, None):
			if device.action == "add":
				self.usb_connected.emit()
			elif device.action == "remove":
				self.usb_disconnected.emit()
