from ctypes import alignment
import sys
import os
from tkinter import Button
import matplotlib
matplotlib.use('Qt5Agg')
from pathlib import Path

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPalette, QColor, QAction
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import pandas as pd

filepath = os.path.abspath(os.getcwd())

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class filer(QWidget):
    def __init__(self, parent= None):
        super(filer, self).__init__(parent)
        layout = QVBoxLayout()
        self.btn = QPushButton("QFileDialog static method demo")
        self.btn.clicked.connect(self.open)

        layout.addWidget(self.btn)

    def open(self):
            fopen = QFileDialog.getOpenFileName(self, 'Get Data File')
            self.myTextBox.setText(fopen)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Open University MatSci Data Cleaning')

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)

        # Create our pandas DataFrame with some simple
        # data and headers.
        df = pd.DataFrame([
           [0, 10], [5, 15], [2, 20], [15, 25], [4, 10],
        ], columns=['A', 'B'])

        # plot the pandas DataFrame, passing in the
        # matplotlib Canvas axes.
        df.plot(ax=sc.axes)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        btn = QPushButton('Select Data File')

        pandasops = QVBoxLayout()
        
        file_qlabel = QLabel('The File You Selected Was')
        self.file_qline = QLineEdit()
        self.file_qline.setReadOnly(True)

        notif = QLabel('Select Smoothing Type Below')
        tsmt_select = QComboBox()
        tsmt_select.addItems(["Convolution", "Exponential", "Spectrial", "Polynomial", "Gaussian"])
        tsmt_select.currentTextChanged.connect(self.smooth_select)

        interval_notif = QLabel('Select Interval Predictor Below')
        interval_tsmt_select = QComboBox()
        interval_tsmt_select.addItems(["Prediction", "Confidence", "Sigma"])

        #tsmt_select.isEditable(False)
        #rawcheck = QCheckBox('Do you want to see Raw Data Overlayed?')
        #rawcheck.setCheckState(Qt.CheckState.Checked)

        # For tristate: widget.setCheckState(Qt.PartiallyChecked)
        # Or: widget.setTriState(True)
        #rawcheck.stateChanged.connect(self.show_state)

        smoothingwindow = QSpinBox()
        smoothqspinlab = QLabel('Set Smoothing Window Rolling Interval')
        smoothlay = QHBoxLayout()
        smoothlay.addWidget(smoothqspinlab)
        smoothlay.addWidget(smoothingwindow)
        
        dtrimlay = QHBoxLayout()
        dtrimwindow = QSpinBox()
        dtrimspinlab = QLabel('Data Trim Index')
        dtrimlay.addWidget(dtrimspinlab)
        dtrimlay.addWidget(dtrimwindow)

        smoothingwindow.setMinimum(1)
        smoothingwindow.setMaximum(99)
        smoothingwindow.setSingleStep(2)  # Or e.g. 0.5 for QDoubleSpinBox
        #smoothingwindow.valueChanged.connect(self.value_changed)
        #widget.textChanged.connect(self.value_changed_str)

        dtrimwindow.setMinimum(1)
        dtrimwindow.setMaximum(100)
        dtrimwindow.setSingleStep(1)

        toperr_cont = QHBoxLayout()
        toperr_lab = QLabel('Top to smoothed line error')
        toperr_val = QLineEdit('x')
        toperr_val.setReadOnly(True)
        toperr_cont.addWidget(toperr_lab)
        toperr_cont.addWidget(toperr_val)

        boterr_cont = QHBoxLayout()
        boterr_lab = QLabel('Bottom to smoothed line error')
        boterr_val = QLineEdit('y')
        boterr_val.setReadOnly(True)
        boterr_cont.addWidget(boterr_lab)
        boterr_cont.addWidget(boterr_val)

        avgerr_cont = QHBoxLayout()
        avgerr_lab = QLabel('Average smoothing error')
        avgerr_val = QLineEdit('z')
        avgerr_val.setReadOnly(True)
        avgerr_cont.addWidget(avgerr_lab)
        avgerr_cont.addWidget(avgerr_val)

        df_smoothed_disp = QCheckBox('Display Smoothed Data')
        df_raw_disp = QCheckBox('Display Raw Data')
        df_noise_disp = QCheckBox('Highlight Noise Spread')
        deriv_disp = QPushButton('Display First Derivative of Data')
        
        pandasops.addWidget(file_qlabel)
        pandasops.addWidget(self.file_qline)
        pandasops.addWidget(notif)
        pandasops.addWidget(tsmt_select)
        pandasops.addWidget(interval_notif)
        pandasops.addWidget(interval_tsmt_select)
        pandasops.addLayout(smoothlay)
        pandasops.addLayout(dtrimlay)
        pandasops.addLayout(toperr_cont)
        pandasops.addLayout(boterr_cont)
        pandasops.addLayout(avgerr_cont)
        pandasops.addWidget(df_smoothed_disp)
        pandasops.addWidget(df_raw_disp)
        pandasops.addWidget(deriv_disp)
        pandasops.addStretch()

        pd_dispops = QVBoxLayout()
        export_disp = QPushButton('Export Smoothed CSV Data')
        pd_dispops.addWidget(export_disp)

        image_ops = QPushButton('Quit')

        layout = QGridLayout()
        layout.addWidget(toolbar, 0, 1)
        layout.addWidget(btn, 0, 0)
        layout.addLayout(pandasops, 1, 0)
        layout.addWidget(sc, 1, 1)
        layout.addLayout(pd_dispops, 2, 0)
        layout.addWidget(image_ops, 2, 1)

        btn.clicked.connect(self.openfile)

        left = QHBoxLayout()
        right = QHBoxLayout()

        right.addWidget(Color('red'))

        left.addLayout(right)

        menu = self.menuBar()

        menu_fa = QAction('Open File', self)
        menu_ha = QAction('ReadMe', self)
        file_menu = menu.addMenu("File")
        file_menu.addAction(menu_fa)
        help_menu = menu.addMenu("Help")
        help_menu.addAction(menu_ha)

        #left.addLayout(layout)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()    
        

    def openfile(self):
        home_dir = os.path.expanduser('~')
        file = QFileDialog.getOpenFileName(self, 'Open file', home_dir, "CSV files (*.csv)")
        fname = os.path.basename(file[0])
        self.file_qline.setText(fname)
        self.fname = file[0]
    
    def smooth_select(self):
        print('we changin')

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()
