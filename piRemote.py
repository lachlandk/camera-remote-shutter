from PyQt5 import QtCore, QtGui, QtWidgets
# from threads.USBMonitor import USBMonitor
from widgets.TitleWidgets import TitleBarWidget
from widgets.CustomTabWidget import CustomTabWidget, CustomTabContainer
import widgets.CameraTabs as CameraTabs
# import gphoto2 as gp
import logging


class CameraConnectedView(QtWidgets.QFrame):

	def __init__(self, parent=None):
		super().__init__(parent)

		main_layout = QtWidgets.QHBoxLayout()
		main_layout.setContentsMargins(0, 0, 0, 0)
		main_layout.addWidget(container := CustomTabContainer())
		self.setLayout(main_layout)

		# TODO: simplify this?
		self.preview_tab = CameraTabs.LivePreviewTab(parent=container)
		self.properties_tab = CameraTabs.PropertiesTab(parent=container)
		self.intervalometer_tab = CameraTabs.IntervalometerTab(parent=container)
		self.review_tab = CameraTabs.ReviewTab(parent=container)

		container.addWidget(preview := CustomTabWidget("Live Preview", self.preview_tab))
		container.addWidget(properties := CustomTabWidget("Camera Properties", self.properties_tab))
		container.addWidget(intervalometer := CustomTabWidget("Intervalometer", self.intervalometer_tab))
		container.addWidget(review := CustomTabWidget("Image Review", self.review_tab))

		self.tabs = []
		self.tabs.append(preview)
		self.tabs.append(properties)
		self.tabs.append(intervalometer)
		self.tabs.append(review)

	def refresh(self):
		# TODO: thread which checks for changed properties
		pass


class CameraDisconnectedView(QtWidgets.QFrame):

	def __init__(self, parent=None):
		super().__init__(parent)

		font = QtGui.QFont("Verdana", 72)
		self.setFont(font)

		title_label = QtWidgets.QLabel("No Camera Connected:\nPLease Connect a Camera.")
		title_label.setAlignment(QtCore.Qt.AlignCenter)

		main_layout = QtWidgets.QHBoxLayout()
		main_layout.addWidget(title_label)
		self.setLayout(main_layout)


class CameraWindow(QtWidgets.QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)

		# TODO: themes and styles
		self.setAutoFillBackground(True)
		font = QtGui.QFont("Verdana", 36)
		self.setFont(font)

		connected_view = CameraConnectedView(parent=self)
		disconnected_view = CameraDisconnectedView(parent=self)
		self.camera_view = QtWidgets.QStackedWidget()
		self.camera_view.addWidget(connected_view)
		self.camera_view.addWidget(disconnected_view)

		self.title_bar = TitleBarWidget()
		self.title_bar.red_line_button.clicked.connect(self.toggle_red_light)
		self.title_bar.close_button.clicked.connect(self.clean_exit)

		main_layout = QtWidgets.QVBoxLayout()
		main_layout.addWidget(self.title_bar)
		main_layout.addWidget(self.camera_view)

		self.setLayout(main_layout)

		self.camera = None
		self.camera_config = None
		self.camera_id = None

		# monitor = USBMonitor()
		# monitor.usb_connected.connect(self.camera_connect)
		# monitor.usb_disconnected.connect(self.camera_disconnect)

		# Testing delete these later
		self.title_bar.camera_model_label.setText(f"Camera Connected: EOS4000D")
		self.title_bar.camera_battery_widget.setText(f"Battery Level: 100%")

		# self.camera_view.setCurrentIndex(1)  # off
		self.camera_view.setCurrentIndex(0)  # on
		# self.camera_connect()

		self.red_light = False
		self.toggle_red_light()

	@QtCore.pyqtSlot()
	def camera_connect(self):
		if not self.camera_config:
			try:
				self.camera = gp.Camera()
				self.camera.init()
				self.camera_config = self.camera.get_config()
				camera_model = self.camera_config.get_child_by_name("cameramodel").get_value()
				camera_battery = self.camera_config.get_child_by_name("batterylevel").get_value()
				camera_serial_number = self.camera_config.get_child_by_name("eosserialnumber").get_value()
				self.camera_id = f"{camera_model}/{camera_serial_number}"

				self.title_bar.camera_model_label.setText(f"Camera Connected: {camera_model}")
				self.title_bar.camera_battery_widget.setText(f"Battery Level: {camera_battery}")

				self.camera_view.setCurrentIndex(0)
			except gp.GPhoto2Error as error:
				if error.code == gp.GP_ERROR_MODEL_NOT_FOUND:
					pass
				else:
					pass

	@QtCore.pyqtSlot()
	def camera_disconnect(self):
		if self.camera_config:
			try:
				self.camera.get_summary()
			except gp.GPhoto2Error as error:
				if error.code == gp.GP_ERROR_IO_USB_FIND:
					self.camera = None
					self.camera_config = None
					self.camera_id = None

					self.title_bar.camera_model_label.setText("")
					self.title_bar.camera_battery_widget.setText("")

					self.camera_view.setCurrentIndex(1)
				else:
					raise

	@QtCore.pyqtSlot()
	def toggle_red_light(self):
		# TODO: replace everything with stylesheets
		if self.red_light:
			palette = QtGui.QPalette()
			palette.setColor(QtGui.QPalette.Window, QtGui.QColor(50, 0, 0))
			palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(150, 0, 0))
			self.setPalette(palette)

			for entry in self.camera_view.currentWidget().intervalometer_tab.entry_list:
				entry.setStyleSheet("color: rgb(150, 0, 0); background-color: rgb(75, 0, 0); font-size: 72px; selection-color: rgb(150, 0, 0); selection-background-color: rgb(75, 0, 0);")
			self.title_bar.red_line_button.setStyleSheet("color: rgb(150, 0, 0); background-color: rgb(75, 0, 0); font-size: 48px")
			self.title_bar.close_button.setStyleSheet("color: rgb(150, 0, 0); background-color: rgb(75, 0, 0); font-size: 48px")

			for tab in self.camera_view.currentWidget().tabs:
				tab.title.drawText(QtGui.QColor(150, 0, 0))

			self.red_light = False
		else:
			palette = QtGui.QPalette()
			palette.setColor(QtGui.QPalette.Window, QtGui.QColor(50, 50, 50))
			palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(200, 200, 200))
			self.setPalette(palette)

			for entry in self.camera_view.currentWidget().intervalometer_tab.entry_list:
				entry.setStyleSheet("color: rgb(50, 50, 50); background-color: rgb(255, 255, 255); font-size: 72px; selection-color: rgb(50, 50, 50); selection-background-color: rgb(255, 255, 255);")
			self.title_bar.red_line_button.setStyleSheet("color: rgb(50, 50, 50); background-color: rgb(255, 255, 255); font-size: 48px")
			self.title_bar.close_button.setStyleSheet("color: rgb(50, 50, 50); background-color: rgb(255, 255, 255); font-size: 48px")

			for tab in self.camera_view.currentWidget().tabs:
				tab.title.drawText(QtGui.QColor(200, 200, 200))

			self.red_light = True

	@QtCore.pyqtSlot()
	def clean_exit(self):
		if self.camera:
			camera.exit()
		self.close()


if __name__ == "__main__":
	import sys
	logging.basicConfig(level=logging.WARNING)
	# callback_obj = gp.check_result(gp.use_python_logging())
	app = QtWidgets.QApplication(sys.argv)
	window = CameraWindow()
	window.setWindowTitle("piRemote")
	window.showFullScreen()
	sys.exit(app.exec())
