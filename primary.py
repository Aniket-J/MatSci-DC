from ctypes import alignment
import sys
import os
from tkinter import Button
import matplotlib
matplotlib.use('Qt5Agg')
from pathlib import Path
import backend_old
from readme import open_readme_dialog
from smooth_selector import smooth_select, smooth_apply
import tsmoothie as tsmt
import scipy.signal as sg
import matplotlib.pyplot as plt
import numpy as np
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPalette, QColor, QAction
from PyQt6.QtCore import Qt, QFile, QTextStream

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

class ColumnSelector(QDialog):
    def __init__(self, df, parent=None):
        super(ColumnSelector, self).__init__(parent)

        self.setWindowTitle("Select columns to plot")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Table to display DataFrame
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

        layout.addWidget(self.tableWidget)

        # ComboBoxes to select columns
        self.xCombo = QComboBox()
        self.yCombo = QComboBox()
        self.xCombo.addItems(df.columns)
        self.yCombo.addItems(df.columns)

        layout.addWidget(QLabel("Select X column:"))
        layout.addWidget(self.xCombo)
        layout.addWidget(QLabel("Select Y column:"))
        layout.addWidget(self.yCombo)
        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            Qt.Orientation.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Data Cleaning')
        #self._Model = model
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)

        # Create our pandas DataFrame with some simple
        # data and headers.
        df = pd.DataFrame([
           [0, 10], [5, 15], [2, 20], [15, 25], [4, 10],
        ], columns=['A', 'B'])

        # plot the pandas DataFrame, passing in the
        # matplotlib Canvas axes.
        df.plot(ax=self.sc.axes)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        btn = QPushButton('Select Data File') #First button to select data file
        btn.clicked.connect(self.openfile) #Connecting to signal

        #############
        #Main layout starts now
        ############
        pandasops = QVBoxLayout() #Main pandas ops layout 
        
        file_qlabel = QLabel('Selected File')
        self.file_qline = QLineEdit()
        self.file_qline.setReadOnly(True)

        # Add this in __init__
        scipynotif = QLabel('Select Smoothing Type')
        self.scipy_select = QComboBox()
        self.scipy_select.addItems(["Convolution", "Exponential", "Spectral", "Polynomial", "Spline", "Gaussian", "Lowess", "Butterworth Filter", "Savitzky-Golay Filter"])
        self.scipy_select.currentTextChanged.connect(self.smooth_select)

        # create widgets for smoothing and interval options with QVBoxLayout
        self.smoothing_options = QWidget()
        self.smoothing_options.setLayout(QVBoxLayout())
        self.interval_options = QWidget()
        self.interval_options.setLayout(QVBoxLayout())

        dtrimlay = QHBoxLayout()
        dtrimwindow = QSpinBox()
        dtrimspinlab = QLabel('Data Trim Index')
        dtrimlay.addWidget(dtrimspinlab)
        dtrimlay.addWidget(dtrimwindow)

        dtrimwindow.setMinimum(1)
        dtrimwindow.setMaximum(100000)
        dtrimwindow.setSingleStep(1)
        dtrimwindow.valueChanged.connect(self.dtrim_change)

        self.applysmooth = QPushButton('Apply Smoothing')
        self.applysmooth.clicked.connect(self.apply_smoothing)
        
        self.remove_smooth_disp = QPushButton('Remove Smoothing')
        self.remove_smooth_disp.clicked.connect(self.remove_smoothing)

        df_raw_disp = QCheckBox('Display Raw Data')
        df_raw_disp.setChecked(True)
        df_raw_disp.stateChanged.connect(self.raw)
        df_raw_disp.stateChanged.connect(self.update_plot_with_smoothed_data)

        df_raw_disp.stateChanged.connect(self.update_plot_with_scipyfilter_data)
        
        self.deriv_disp = QPushButton('Display First Derivative of Data')
        self.deriv_disp.clicked.connect(self.plot_derivative)

        export_disp = QPushButton('Export Smoothed CSV Data')
        export_disp.clicked.connect(self.export_smoothed_data)
        ###############
        #Main layout functionalities created
        ###############
        #Arranging main layout below
        ###############

        pandasops.addWidget(file_qlabel) #File label
        pandasops.addWidget(self.file_qline) #Display actual file name 
        pandasops.addWidget(scipynotif) #Notify user that they need to select filter 
        pandasops.addWidget(self.scipy_select) #List of filters
        pandasops.addWidget(self.smoothing_options)
        pandasops.addWidget(self.interval_options)

        pandasops.addLayout(dtrimlay) #Manual trim point adjustment
        pandasops.addWidget(self.applysmooth)
        pandasops.addWidget(self.remove_smooth_disp)
        pandasops.addWidget(df_raw_disp) #Display raw data overlayed or nah?
        pandasops.addWidget(self.deriv_disp ) #Popup window for first-derivative of force
        pandasops.addStretch() #For aesthetics

        #############
        #Main layout arranged
        #############
        #Arranging the toolbars and boxes stuff now
        #############

        pd_dispops = QVBoxLayout() #To shift stuff in the bottom left half
        pd_dispops.addWidget(export_disp) #Adds the export button

        image_ops = QPushButton('Quit') #Adds the Quit command
        image_ops.clicked.connect(QtWidgets.QApplication.quit)
        
        layout = QGridLayout() #Arranging the jigsaw puzzle pieces now
        layout.addWidget(toolbar, 0, 1) #Toolbar at the top
        layout.addWidget(btn, 0, 0) #Navigation Toolbar top-right
        layout.addLayout(pandasops, 1, 0) #Pandas ops on centre-left
        layout.addWidget(self.sc, 1, 1) #Pandas plot on centre-right
        layout.addLayout(pd_dispops, 2, 1) #Export button bottom-right
        layout.addWidget(image_ops, 2, 0) #Quit button bottom-left

        menu = self.menuBar() #Menubar for ReadMe and File

        menu_fa = QAction('Open File', self)
        menu_fa.triggered.connect(self.openfile)
        file_menu = menu.addMenu("File")
        file_menu.addAction(menu_fa)
        # Connect the action to the open_readme_dialog() method
        menu_ha = QAction('ReadMe', self)
        menu_ha.triggered.connect(open_readme_dialog)

        # Add the action to the Help menu
        help_menu = menu.addMenu("Help")
        help_menu.addAction(menu_ha)

        # Create the shortcut for Ctrl+O
        #open_file_shortcut = QtWidgets.QKeySequenceEdit(keySequence=open)
        # Connect the shortcut to the openfile method
        #open_file_shortcut.activated.connect(self.openfile)

        #left.addLayout(layout)
        self.filename = ""
        self.display_raw_data = True
        self.smoother = ""
        self.low = ""
        self.up = ""
        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()   

    def openfile(self):
        filename, fullpath = backend_old.Openfile(self)
        self.filename = filename
        if filename:
            try:
                self.file_qline.setText(filename)
                self.fname = fullpath
                # Load the dataframe
                self.df = backend_old.load_data(fullpath)
                self.df_to_plot = self.df.copy()
                # Open column selector dialog
                dialog = ColumnSelector(self.df)
                result = dialog.exec()
                if result == QDialog.DialogCode.Accepted:
                    self.x_column = dialog.xCombo.currentText()
                    self.y_column = dialog.yCombo.currentText()
                    self.update_plot()  # update the plot after a file is selected
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading file:\n{str(e)}")
        else:
            QMessageBox.information(self, "Info", "No file selected")
    
    def update_plot(self):
        self.sc.axes.clear()  # clear the previous plot
        self.df_to_plot.plot(x=self.x_column, y=self.y_column, ax=self.sc.axes)  # plot new data
        self.sc.axes.set_ylabel(self.y_column) # set y-axis label
        self.sc.axes.set_xlabel(self.x_column) # set x-axis label
        self.sc.axes.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)  # add gridlines
        self.sc.draw()
   
    def smooth_select(self, smoother_name):
        smooth_select(self, smoother_name)
        
    def update_plot_with_smoothed_data(self, selected_option):
        # get smoother name
        smoother_name = self.scipy_select.currentText()
        #smoother_name = self.sender().parent().children()[1].currentText()
        # update plot based on smoother_name and selected_option

    def update_table(self):
        # Clear the old table
        self.tableWidget.setRowCount(0)

        # Limit to first 10 rows
        df_preview = self.df.head(10)

        # Update the QTableWidget with the dataframe values
        for i in range(df_preview.shape[0]):
            for j in range(df_preview.shape[1]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(df_preview.iat[i, j])))

    def adjust_df(self, df, row_index):
        adjusted_df = df.copy()
        for column in adjusted_df.columns:
            adjusted_df[column] = adjusted_df[column] - adjusted_df[column].iloc[row_index]
        adjusted_df = adjusted_df.iloc[row_index+1:]  # trim the DataFrame
        return adjusted_df.reset_index(drop=True)
    
    def apply_smoothing(self):
        smooth_apply(self)

    def update_plot_with_smoothed_data(self):
        self.sc.axes.clear()  # clear the previous plot
        if self.smoother:  # check if smoother has been initialized
            self.sc.axes.plot(self.df_to_plot[self.x_column].values, self.smoother.smooth_data[0], linewidth=3, color='blue')  # plot smoothed data
            if self.display_raw_data:
                self.sc.axes.plot(self.df_to_plot[self.x_column].values, self.df_to_plot[self.y_column].values, '.k', markersize = 1)  # plot original data
                self.sc.axes.fill_between(self.df_to_plot[self.x_column].values, self.low[0], self.up[0], alpha=0.3)  # plot intervals
        self.sc.axes.set_ylabel(self.y_column)  # set y-axis label
        self.sc.axes.set_xlabel(self.x_column) # set x-axis label
        self.sc.axes.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)  # add gridlines
        self.sc.draw()

    def update_plot_with_scipyfilter_data(self):
        self.sc.axes.clear()  # clear the previous plot
        self.sc.axes.plot(self.df_to_plot[self.x_column].values, self.df_to_plot[self.y_column].values, linewidth=3, color='blue')  # plot filtered data
        if self.display_raw_data:
            self.sc.axes.plot(self.df_to_plot[self.x_column].values, self.df_to_plot[self.y_column].values, '.k', markersize = 1)  # plot original data
        self.sc.axes.set_ylabel(self.y_column) # set y-axis label
        self.sc.axes.set_xlabel(self.x_column) # set x-axis label
        self.sc.axes.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)  # add gridlines
        self.sc.draw()
        
    def export_smoothed_data(self):
        # Get the original file name
        original_filename = os.path.splitext(os.path.basename(self.filename))[0]

        # Set the default file name with the placeholder
        default_filename = f"{original_filename}_SMOOTHED.csv"

        # Open a file dialog to get the save file name and directory
        save_file, _ = QFileDialog.getSaveFileName(
            self, "Save Smoothed Data", default_filename, "CSV Files (*.csv)")

        # Check if a file name was selected
        if save_file and hasattr(self, 'df_smoothed') and not self.df_smoothed.empty:
            # Save the smoothed data to the selected file
            self.df_smoothed.to_csv(save_file, index=False)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No smoothed data available to export!")
            msg.setWindowTitle("Warning")
            msg.exec_()

    def dtrim_change(self, dtrimcount):
        if hasattr(self, 'df') and not self.df.empty:  # if a file is loaded
            self.df_to_plot = self.adjust_df(self.df, dtrimcount)
            self.update_plot()  # update the plot with the trimmed and adjusted data
    
    def plot_derivative(self):
        # Perform derivative calculations and create derivative plot
        y_values = self.df_to_plot[self.y_column].values
        x_values = self.df_to_plot[self.x_column].values
        
        # Calculate the derivative dy/dx using finite
        #  differences
        dy_dx = self.df_to_plot[self.y_column].diff() / self.df_to_plot[self.x_column].diff()
        
        # Create a new MplCanvas instance for the derivative plot
        derivative_canvas = MplCanvas()
        
        # Plot the derivative data on the new canvas
        derivative_canvas.axes.clear()
        derivative_canvas.axes.plot(x_values, dy_dx)
        derivative_canvas.axes.set_xlabel(self.x_column)
        derivative_canvas.axes.set_ylabel('dy/dx')
        derivative_canvas.axes.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        derivative_canvas.draw()        
        # Create a new window to display the derivative plot
        derivative_window = QDialog(self)
        layout = QVBoxLayout()
        # Add the navigation toolbar to the derivative window
        toolbar = NavigationToolbar(derivative_canvas, derivative_window)
        layout.addWidget(toolbar)
        layout.addWidget(derivative_canvas)
        derivative_window.setLayout(layout)
        derivative_window.setWindowTitle('Derivative Plot')
        derivative_window.show()

    def raw(self, state):
        self.display_raw_data = bool(state)

    def remove_smoothing(self):
        # Reset df_to_plot to the original loaded dataframe
        self.df_to_plot = self.df.copy()

        # Re-draw the original plot
        self.update_plot()

class Model(QtCore.QObject):
    def __init__(self,model):
        super().__init__()

        self._model = model

    

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()
