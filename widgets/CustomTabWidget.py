from PyQt5 import QtCore, QtGui, QtWidgets


class CustomButton(QtWidgets.QFrame):

	clicked = QtCore.pyqtSignal()

	def __init__(self, title, parent=None):
		super().__init__(parent)

		self.setFrameStyle(1)

		self.title = title
		self.label = QtWidgets.QLabel()
		self.label.setContentsMargins(0, 0, 0, 0)

		self.drawText(QtGui.QColor(255, 255, 255))

		layout = QtWidgets.QVBoxLayout()
		layout.setContentsMargins(10, 10, 10, 10)
		layout.addWidget(self.label)
		layout.addStretch()
		self.setLayout(layout)

	def drawText(self, colour):
		font = QtGui.QFont("Verdana", 48)
		metrics = QtGui.QFontMetrics(font)
		width = metrics.width(self.title)
		height = metrics.height()
		canvas = QtGui.QPixmap(height, width)
		canvas.fill(QtCore.Qt.transparent)

		painter = QtGui.QPainter(canvas)
		painter.setPen(colour)
		painter.setFont(font)
		painter.rotate(-90)
		painter.translate(-width, 0)
		painter.drawText(0, 0, width, height, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, self.title)
		painter.end()
		self.label.setPixmap(canvas)

	def mousePressEvent(self, event):
		self.clicked.emit()


class CustomTabWidget(QtWidgets.QFrame):

	def __init__(self, tab_title, tab_content, parent=None):
		super().__init__(parent)

		self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

		self.index = None

		self.title = CustomButton(tab_title)
		self.title.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
		self.title.clicked.connect(self.makeCurrentIndex)
		self.content = tab_content
		self.content.setFrameStyle(1)
		layout = QtWidgets.QHBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(self.title)
		layout.addWidget(self.content)
		self.setLayout(layout)

	@QtCore.pyqtSlot()
	def makeCurrentIndex(self):
		self.parentWidget().setCurrentIndex(self.index)


class CustomTabContainer(QtWidgets.QFrame):

	def __init__(self, parent=None):
		super().__init__(parent)

		self.tabs = []
		self.currentIndex = 0

		self.layout = QtWidgets.QHBoxLayout()
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.layout)

	def setCurrentIndex(self, index):
		current_widget = self.tabs[self.currentIndex]
		current_widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
		current_widget.content.hide()
		self.currentIndex = index
		new_widget = self.tabs[self.currentIndex]
		new_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		new_widget.content.show()

	def addWidget(self, widget):
		if len(self.tabs) == 0:
			widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		else:
			widget.content.hide()
		self.layout.addWidget(widget)
		self.tabs.append(widget)
		widget.index = self.tabs.index(widget)
