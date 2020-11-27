from PyQt5 import QtCore, QtGui, QtWidgets


class BatteryIndicatorWidget(QtWidgets.QWidget):
	# TODO: implement
	pass


class TitleBarWidget(QtWidgets.QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)

		self.camera_model_label = QtWidgets.QLabel()
		self.camera_battery_widget = QtWidgets.QLabel()  # change in future to custom
		self.red_line_button = QtWidgets.QPushButton("Red Light")
		self.close_button = QtWidgets.QPushButton("Quit")

		layout = QtWidgets.QHBoxLayout()
		layout.addWidget(self.camera_model_label)
		layout.addWidget(self.camera_battery_widget)
		layout.addStretch()
		layout.addWidget(self.red_line_button)
		layout.addWidget(self.close_button)

		self.setLayout(layout)
