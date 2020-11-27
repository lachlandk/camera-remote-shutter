from PyQt5 import QtCore, QtGui, QtWidgets
from threads.CameraIntervalometer import Intervalometer


class LivePreviewTab(QtWidgets.QFrame):

	def __init__(self, parent=None):
		super().__init__(parent)

		font = QtGui.QFont("Verdana", 72)
		self.setFont(font)

		# TODO: implement
		title_label = QtWidgets.QLabel("Live Preview\nNot Implemented")
		title_label.setAlignment(QtCore.Qt.AlignCenter)

		main_layout = QtWidgets.QHBoxLayout()
		main_layout.addWidget(title_label)
		self.setLayout(main_layout)


class PropertiesTab(QtWidgets.QFrame):

	def __init__(self, parent=None):
		super().__init__(parent)

		font = QtGui.QFont("Verdana", 72)
		self.setFont(font)

		# TODO: implement
		title_label = QtWidgets.QLabel("Camera Properties\nNot Implemented")
		title_label.setAlignment(QtCore.Qt.AlignCenter)

		main_layout = QtWidgets.QHBoxLayout()
		main_layout.addWidget(title_label)
		self.setLayout(main_layout)


class IntervalometerTab(QtWidgets.QFrame):

	class SpinBoxLabel(QtWidgets.QLabel):

		def __init__(self, title, font_size, parent=None):
			super().__init__(parent)
			self.setText(title)
			self.setFont(QtGui.QFont("Verdana", font_size))
			self.setAlignment(QtCore.Qt.AlignCenter)

	class CustomSpinBox(QtWidgets.QDoubleSpinBox):

		def __init__(self, up, down, lineedit, parent=None):
			super().__init__(parent)
			# self.setAlignment(QtCore.Qt.AlignCenter)
			self.setLineEdit(lineedit)
			up.clicked.connect(self.stepUp)
			down.clicked.connect(self.stepDown)
			lineedit.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
			lineedit.setMinimumWidth(0)
			lineedit.setAlignment(QtCore.Qt.AlignCenter)
			self.hide()
			# TODO: https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qspinbox

	def __init__(self, parent=None):
		super().__init__(parent)

		font = QtGui.QFont("Verdana", 48)
		self.setFont(font)

		# TODO: rewrite this by styling QSpinBox with stylesheets
		self.delay_up_button = QtWidgets.QPushButton("/\\")
		self.delay_down_button = QtWidgets.QPushButton("\\/")
		self.delay_entry = self.CustomSpinBox(self.delay_up_button, self.delay_down_button, QtWidgets.QLineEdit(), parent=self)
		self.delay_entry.setRange(1, 99)
		self.delay_entry.setSuffix("s")
		self.delay_entry.valueChanged.connect(self.update_capture_time)
		self.exposure_up_button = QtWidgets.QPushButton("/\\")
		self.exposure_down_button = QtWidgets.QPushButton("\\/")
		self.exposure_entry = self.CustomSpinBox(self.exposure_up_button, self.exposure_down_button, QtWidgets.QLineEdit(), parent=self)
		self.exposure_entry.setRange(1, 99)
		self.exposure_entry.setSuffix("s")
		self.exposure_entry.valueChanged.connect(self.update_capture_time)
		self.interval_up_button = QtWidgets.QPushButton("/\\")
		self.interval_down_button = QtWidgets.QPushButton("\\/")
		self.interval_entry = self.CustomSpinBox(self.interval_up_button, self.interval_down_button, QtWidgets.QLineEdit(), parent=self)
		self.interval_entry.setRange(0, 99)
		self.interval_entry.setSuffix("s")
		self.interval_entry.valueChanged.connect(self.update_capture_time)
		self.count_up_button = QtWidgets.QPushButton("/\\")
		self.count_down_button = QtWidgets.QPushButton("\\/")
		self.count_entry = self.CustomSpinBox(self.count_up_button, self.count_down_button, QtWidgets.QLineEdit(), parent=self)
		self.count_entry.setRange(1, 99)
		self.count_entry.valueChanged.connect(self.update_capture_time)

		delay_box = QtWidgets.QVBoxLayout()
		delay_box.addStretch()
		delay_box.addWidget(self.SpinBoxLabel("Del.", 72))
		delay_box.addWidget(self.delay_up_button)
		delay_box.addWidget(self.delay_entry.lineEdit())
		delay_box.addWidget(self.delay_down_button)
		delay_box.addStretch()
		exposure_box = QtWidgets.QVBoxLayout()
		exposure_box.addStretch()
		exposure_box.addWidget(self.SpinBoxLabel("Exp.", 72))
		exposure_box.addWidget(self.exposure_up_button)
		exposure_box.addWidget(self.exposure_entry.lineEdit())
		exposure_box.addWidget(self.exposure_down_button)
		exposure_box.addStretch()
		interval_box = QtWidgets.QVBoxLayout()
		interval_box.addStretch()
		interval_box.addWidget(self.SpinBoxLabel("Int.", 72))
		interval_box.addWidget(self.interval_up_button)
		interval_box.addWidget(self.interval_entry.lineEdit())
		interval_box.addWidget(self.interval_down_button)
		interval_box.addStretch()
		count_box = QtWidgets.QVBoxLayout()
		count_box.addStretch()
		count_box.addWidget(self.SpinBoxLabel("Cnt.", 72))
		count_box.addWidget(self.count_up_button)
		count_box.addWidget(self.count_entry.lineEdit())
		count_box.addWidget(self.count_down_button)
		count_box.addStretch()

		intervalometer_settings_layout = QtWidgets.QHBoxLayout()
		intervalometer_settings_layout.addLayout(delay_box)
		intervalometer_settings_layout.addWidget(self.SpinBoxLabel(":", 72))
		intervalometer_settings_layout.addLayout(exposure_box)
		intervalometer_settings_layout.addWidget(self.SpinBoxLabel(":", 72))
		intervalometer_settings_layout.addLayout(interval_box)
		intervalometer_settings_layout.addWidget(self.SpinBoxLabel(":", 72))
		intervalometer_settings_layout.addLayout(count_box)

		self.total_exposure_time_label = QtWidgets.QLabel()
		self.time_to_capture_label = QtWidgets.QLabel()
		self.start_button = QtWidgets.QPushButton("Start Capture")
		self.start_button.clicked.connect(self.start_intervalometer)

		total_time_layout = QtWidgets.QVBoxLayout()
		total_time_layout.addWidget(self.total_exposure_time_label)
		total_time_layout.addWidget(self.time_to_capture_label)
		total_time_start_button_layout = QtWidgets.QHBoxLayout()
		total_time_start_button_layout.addLayout(total_time_layout)
		total_time_start_button_layout.addWidget(self.start_button)

		main_layout = QtWidgets.QVBoxLayout()
		main_layout.addLayout(intervalometer_settings_layout)
		main_layout.addLayout(total_time_start_button_layout)
		self.setLayout(main_layout)

		self.entry_list = []
		self.entry_list.append(self.delay_up_button)
		self.entry_list.append(self.delay_down_button)
		self.entry_list.append(self.delay_entry.lineEdit())
		self.entry_list.append(self.exposure_up_button)
		self.entry_list.append(self.exposure_down_button)
		self.entry_list.append(self.exposure_entry.lineEdit())
		self.entry_list.append(self.interval_up_button)
		self.entry_list.append(self.interval_down_button)
		self.entry_list.append(self.interval_entry.lineEdit())
		self.entry_list.append(self.count_up_button)
		self.entry_list.append(self.count_down_button)
		self.entry_list.append(self.count_entry.lineEdit())
		self.entry_list.append(self.start_button)

		self.delay = 1
		self.exposure = 1
		self.interval = 0
		self.count = 1
		self.update_capture_time()
		self.intervalometer_thread = None

	@QtCore.pyqtSlot()
	def update_capture_time(self):
		self.delay = float(self.delay_entry.cleanText())
		self.exposure = float(self.exposure_entry.cleanText())
		self.interval = float(self.interval_entry.cleanText())
		self.count = float(self.count_entry.cleanText())
		self.total_exposure_time_label.setText(f"Exposure Time: {self.exposure * self.count}s")
		self.time_to_capture_label.setText(f"Time to Capture: {self.delay + self.exposure * self.count + self.interval * (self.count - 1)}s")

	@QtCore.pyqtSlot()
	def start_intervalometer(self):
		self.intervalometer_thread = Intervalometer(int(self.delay), int(self.exposure), int(self.interval), int(self.count), self)
		# disable form widgets
		# .setDisabled(True)


class ReviewTab(QtWidgets.QFrame):

	def __init__(self, parent=None):
		super().__init__(parent)

		font = QtGui.QFont("Verdana", 72)
		self.setFont(font)

		# TODO: implement
		title_label = QtWidgets.QLabel("Image Review\nNot Implemented")
		title_label.setAlignment(QtCore.Qt.AlignCenter)

		main_layout = QtWidgets.QHBoxLayout()
		main_layout.addWidget(title_label)
		self.setLayout(main_layout)
