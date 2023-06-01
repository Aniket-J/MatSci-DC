from PyQt6.QtWidgets import *
import tsmoothie as tsmt
import scipy.signal as sg
# Kept it as a function right now
# Could create a class in the future if I decide to add more in the future


def smooth_select(self, smoother_name):
# Remove all widgets from smoothing_options and interval_options
    for layout in [self.smoothing_options.layout(), self.interval_options.layout()]:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # Time to add new widgets to smoothing_options and interval_options
    if smoother_name == "Convolution":
        # create new widgets
        windowlabel = QLabel("Window Type:")
        windowcombo = QComboBox()
        windowcombo.addItems(["ones", "hanning", "hamming", "bartlett", "blackman"])
        rollingwindow = QLabel("Smoothing Window Length")
        windowlength = QSpinBox()
        intervalcomboname = QLabel("Interval Type")
        intervalcombo = QLabel("sigma_interval")
        # Add all these widgets to layout
        self.smoothing_options.layout().addWidget(windowlabel)
        self.smoothing_options.layout().addWidget(windowcombo)
        self.smoothing_options.layout().addWidget(rollingwindow)
        self.smoothing_options.layout().addWidget(windowlength)
        self.smoothing_options.layout().addWidget(intervalcomboname)
        self.smoothing_options.layout().addWidget(intervalcombo)
        # Now connect signal to appropriate slot
        windowcombo.currentTextChanged.connect(self.update_plot_with_smoothed_data)
        windowlength.valueChanged.connect(self.update_plot_with_smoothed_data)

    if smoother_name == "Exponential":
        # Create new widgets
        alphalabel = QLabel("Alpha:")
        alphaspin = QDoubleSpinBox()
        alphaspin.setMinimum(0)
        alphaspin.setMaximum(1)
        alphaspin.setSingleStep(0.05)
        rollingwindow = QLabel("Smoothing Window Length")
        windowlength = QSpinBox()
        intervalcomboname = QLabel("Interval Type")
        intervalcombo = QLabel("sigma_interval")
        # Add all these widgets to layout
        self.smoothing_options.layout().addWidget(alphalabel)
        self.smoothing_options.layout().addWidget(alphaspin)
        self.smoothing_options.layout().addWidget(rollingwindow)
        self.smoothing_options.layout().addWidget(windowlength)
        self.smoothing_options.layout().addWidget(intervalcomboname)
        self.smoothing_options.layout().addWidget(intervalcombo)
        # Connect signal to appropriate slot
        alphaspin.valueChanged.connect(self.update_plot_with_smoothed_data)
        windowlength.valueChanged.connect(self.update_plot_with_smoothed_data)

    if smoother_name == "Spectral":
        # create new widgets
        smoothfraclabel = QLabel("Smoothing Fraction:")
        smoothfracspin = QDoubleSpinBox()
        smoothfracspin.setMinimum(0)
        smoothfracspin.setMaximum(1)
        smoothfracspin.setSingleStep(0.05) # Step size to move this frac
        padelenlabel = QLabel("Padding Length")
        padlenbox = QSpinBox()
        intervalcomboname = QLabel("Interval Type")
        intervalcombo = QLabel("sigma_interval")
        # Add all these widgets to layout
        self.smoothing_options.layout().addWidget(smoothfraclabel)
        self.smoothing_options.layout().addWidget(smoothfracspin)
        self.smoothing_options.layout().addWidget(padelenlabel)
        self.smoothing_options.layout().addWidget(padlenbox)
        self.smoothing_options.layout().addWidget(intervalcomboname)
        self.smoothing_options.layout().addWidget(intervalcombo)
        # Connect signal to appropriate slot
        smoothfracspin.valueChanged.connect(self.update_plot_with_smoothed_data)
        padlenbox.valueChanged.connect(self.update_plot_with_smoothed_data)

    if smoother_name == "Polynomial":
        degreelabel = QLabel("Polynomial Degree")
        degreespinbox = QSpinBox()
        degreespinbox.setMinimum(0)
        degreespinbox.setMaximum(3)
        degreespinbox.setSingleStep(1) # tsmoothie supports only upto 3
        intervalcomboname = QLabel("Interval Type")
        intervalcombo = QComboBox()
        intervalcombo.addItems(["sigma_interval", "confidence_interval", "prediction_interval"])
        # Add all these widgets to layout
        self.smoothing_options.layout().addWidget(degreelabel)
        self.smoothing_options.layout().addWidget(degreespinbox)
        self.smoothing_options.layout().addWidget(intervalcomboname)
        self.smoothing_options.layout().addWidget(intervalcombo)
        # Connect signal to appropriate slot
        degreespinbox.valueChanged.connect(self.update_plot_with_smoothed_data)
        intervalcombo.currentTextChanged.connect(self.update_plot_with_smoothed_data)

    if smoother_name == "Spline":
        splinelab = QLabel("Spline Type")
        splinetypebox = QComboBox()
        splinetypebox.addItems(["linear_spline", "cubic_spline", "natural_cubic_spline"])
        n_knotlab = QLabel("n_knots")
        n_knot_box = QSpinBox()
        n_knot_box.setMinimum(1)
        n_knot_box.setMaximum(3)
        n_knot_box.setSingleStep(1)
        knotlab = QLabel("knots")
        knot_box = QSpinBox()
        knot_box.setMinimum(1)
        knot_box.setMaximum(3)
        knot_box.setSingleStep(1)
        intervalcomboname = QLabel("Interval Type")
        intervalcombo = QComboBox()
        intervalcombo.addItems(["sigma_interval", "confidence_interval", "prediction_interval"])
        # Add all these widgets to layout
        self.smoothing_options.layout().addWidget(splinelab)
        self.smoothing_options.layout().addWidget(splinetypebox)
        self.smoothing_options.layout().addWidget(n_knotlab)
        self.smoothing_options.layout().addWidget(n_knot_box)
        self.smoothing_options.layout().addWidget(knotlab)
        self.smoothing_options.layout().addWidget(knot_box)
        self.smoothing_options.layout().addWidget(intervalcomboname)
        self.smoothing_options.layout().addWidget(intervalcombo)
        # Connect signal to appropriate slot
        splinetypebox.currentTextChanged.connect(self.update_plot_with_smoothed_data)
        n_knot_box.valueChanged.connect(self.update_plot_with_smoothed_data)
        knot_box.valueChanged.connect(self.update_plot_with_smoothed_data)
        intervalcombo.currentTextChanged.connect(self.update_plot_with_smoothed_data)
    
    if smoother_name == "Gaussian":
        sigmalab = QLabel("Sigma")
        sigmabox = QDoubleSpinBox()
        sigmabox.setMinimum(0)
        sigmabox.setMaximum(1)
        sigmabox.setSingleStep(0.05)
        n_knotlab = QLabel("n_knots")
        n_knot_box = QSpinBox()
        n_knot_box.setMinimum(1)
        n_knot_box.setMaximum(3)
        n_knot_box.setSingleStep(1)
        knotlab = QLabel("knots")
        knot_box = QSpinBox()
        knot_box.setMinimum(1)
        knot_box.setMaximum(3)
        knot_box.setSingleStep(1)
        intervalcomboname = QLabel("Interval Type")
        intervalcombo = QComboBox()
        intervalcombo.addItems(["sigma_interval", "confidence_interval", "prediction_interval"])
        # Add all these widgets to layout
        self.smoothing_options.layout().addWidget(sigmalab)
        self.smoothing_options.layout().addWidget(sigmabox)
        self.smoothing_options.layout().addWidget(n_knotlab)
        self.smoothing_options.layout().addWidget(n_knot_box)
        self.smoothing_options.layout().addWidget(knotlab)
        self.smoothing_options.layout().addWidget(knot_box)
        self.smoothing_options.layout().addWidget(intervalcomboname)
        self.smoothing_options.layout().addWidget(intervalcombo)
        # Connect signal to appropriate slot
        sigmabox.valueChanged.connect(self.update_plot_with_smoothed_data)
        n_knot_box.valueChanged.connect(self.update_plot_with_smoothed_data)
        knot_box.valueChanged.connect(self.update_plot_with_smoothed_data)
        intervalcombo.currentTextChanged.connect(self.update_plot_with_smoothed_data)

    if smoother_name == "Lowess":
        smoothfraclab = QLabel("Smooth Fraction")
        smoothfracbox = QDoubleSpinBox()
        smoothfracbox.setMinimum(0)
        smoothfracbox.setMaximum(1)
        smoothfracbox.setSingleStep(0.05)
        iterlab = QLabel("Iterations")
        iterbox = QSpinBox()
        iterbox.setMinimum(1)
        iterbox.setMaximum(6)
        iterbox.setSingleStep(1)
        batchsizelab = QLabel("Batch Size")
        batchsize_box = QSpinBox()
        batchsize_box.setMinimum(1)
        batchsize_box.setMaximum(3)
        batchsize_box.setSingleStep(1)
        intervalcomboname = QLabel("Interval Type")
        intervalcombo = QComboBox()
        intervalcombo.addItems(["sigma_interval", "confidence_interval", "prediction_interval"])
        # Add all these widgets to layout
        self.smoothing_options.layout().addWidget(smoothfraclab)
        self.smoothing_options.layout().addWidget(smoothfracbox)
        self.smoothing_options.layout().addWidget(iterlab)
        self.smoothing_options.layout().addWidget(iterbox)
        self.smoothing_options.layout().addWidget(batchsizelab)
        self.smoothing_options.layout().addWidget(batchsize_box)
        self.smoothing_options.layout().addWidget(intervalcomboname)
        self.smoothing_options.layout().addWidget(intervalcombo)
        # Connect signal to appropriate slot
        smoothfracbox.valueChanged.connect(self.update_plot_with_smoothed_data)
        iterbox.valueChanged.connect(self.update_plot_with_smoothed_data)
        batchsize_box.valueChanged.connect(self.update_plot_with_smoothed_data)
        intervalcombo.currentTextChanged.connect(self.update_plot_with_smoothed_data)

    if smoother_name == "Butterworth Filter":
        filterlab = QLabel("Filter Order")
        filterbox = QSpinBox()
        filterbox.setMinimum(0)
        filterbox.setMaximum(50)
        filterbox.setSingleStep(1)
        critfreq_lab = QLabel("Critical Frequency")
        critfreq_box = QDoubleSpinBox()
        critfreq_box.setMinimum(0)
        critfreq_box.setMaximum(1)
        critfreq_box.setSingleStep(0.005)
        passlab = QLabel("Filter Type")
        passbox = QComboBox()
        passbox.addItems(["lowpass", "highpass"])
        # Add all these widgets to layout
        self.smoothing_options.layout().addWidget(filterlab)
        self.smoothing_options.layout().addWidget(filterbox)
        self.smoothing_options.layout().addWidget(critfreq_lab)
        self.smoothing_options.layout().addWidget(critfreq_box)
        self.smoothing_options.layout().addWidget(passlab)
        self.smoothing_options.layout().addWidget(passbox)
        # Connect signal to appropriate slot
        filterbox.valueChanged.connect(self.update_plot_with_smoothed_data)
        critfreq_box.valueChanged.connect(self.update_plot_with_smoothed_data)
        passbox.currentTextChanged.connect(self.update_plot_with_smoothed_data)

    if smoother_name == "Savitzky-Golay Filter":
        rollingwindow = QLabel("Filter Window Length")
        windowlength = QSpinBox()
        degreelabel = QLabel("Polynomial Degree")
        degreespinbox = QSpinBox()
        degreespinbox.setMinimum(1)
        degreespinbox.setMaximum(20)
        degreespinbox.setSingleStep(1)
        # Add all these widgets to layout
        self.smoothing_options.layout().addWidget(rollingwindow)
        self.smoothing_options.layout().addWidget(windowlength)
        self.smoothing_options.layout().addWidget(degreelabel)
        self.smoothing_options.layout().addWidget(degreespinbox)
        # Connect signal to appropriate slot
        windowlength.valueChanged.connect(self.update_plot_with_smoothed_data)
        degreespinbox.valueChanged.connect(self.update_plot_with_smoothed_data)

def smooth_apply(self):
    # get smoother name
    smoother_name = self.scipy_select.currentText()
    
    if smoother_name == "Convolution":
        # retrieve parameter values from GUI
        windowcombo = self.smoothing_options.layout().itemAt(1).widget().currentText()
        windowlength = self.smoothing_options.layout().itemAt(3).widget().value()
        interval_type = 'sigma_interval'

        # create and apply smoother
        smoother = tsmt.ConvolutionSmoother(window_len=windowlength, window_type=windowcombo)
        smoother.smooth(self.df_to_plot[self.y_column].values)  # smoothing applied on y values 

        # generate intervals
        low, up = smoother.get_intervals(interval_type)

        # set the smoother and intervals as instance variables to be used in update_plot
        self.smoother = smoother
        self.low = low
        self.up = up

        # create a new DataFrame to hold the smoothed data
        self.df_smoothed = self.df_to_plot.copy()

        # add smoothed column to df_smoothed
        self.df_smoothed[self.y_column + "_SMOOTHED"] = self.smoother.smooth_data[0]

        self.update_plot_with_smoothed_data()
    
    if smoother_name == "Exponential":
        # retrieve parameter values from GUI
        alphaspin = self.smoothing_options.layout().itemAt(1).widget().value()
        windowlength = self.smoothing_options.layout().itemAt(3).widget().value()
        interval_type = 'sigma_interval'

        # create and apply smoother
        smoother = tsmt.ExponentialSmoother(window_len=windowlength, alpha=alphaspin)
        smoother.smooth(self.df_to_plot[self.y_column].values)  # smoothing applied on y values 

        # generate intervals
        low, up = smoother.get_intervals(interval_type)

        # set the smoother and intervals as instance variables to be used in update_plot
        self.smoother = smoother
        self.low = low
        self.up = up
        # create a new DataFrame to hold the smoothed data
        self.df_smoothed = self.df_to_plot.copy()

        # add smoothed column to df_smoothed
        self.df_smoothed[self.y_column + "_SMOOTHED"] = self.smoother.smooth_data[0]
        self.update_plot_with_smoothed_data()
    
    if smoother_name == "Spectral":
        # retrieve parameter values from GUI
        smoothfracspin = self.smoothing_options.layout().itemAt(1).widget().value()
        padlenbox = self.smoothing_options.layout().itemAt(3).widget().value()
        interval_type = 'sigma_interval'

        # create and apply smoother
        smoother = tsmt.SpectralSmoother(smooth_fraction=smoothfracspin, pad_len=padlenbox)
        smoother.smooth(self.df_to_plot[self.y_column].values)  # smoothing applied on y values 

        # generate intervals
        low, up = smoother.get_intervals(interval_type)

        # set the smoother and intervals as instance variables to be used in update_plot
        self.smoother = smoother
        self.low = low
        self.up = up
        # create a new DataFrame to hold the smoothed data
        self.df_smoothed = self.df_to_plot.copy()

        # add smoothed column to df_smoothed
        self.df_smoothed[self.y_column + "_SMOOTHED"] = self.smoother.smooth_data[0]
        self.update_plot_with_smoothed_data()

    if smoother_name == "Polynomial":
        # retrieve parameter values from GUI
        degreespinbox = self.smoothing_options.layout().itemAt(1).widget().value()
        interval_type = self.smoothing_options.layout().itemAt(3).widget().currentText()

        # create and apply smoother
        smoother = tsmt.PolynomialSmoother(degree=degreespinbox)
        smoother.smooth(self.df_to_plot[self.y_column].values)  # smoothing applied on y values 

        # generate intervals
        low, up = smoother.get_intervals(interval_type)

        # set the smoother and intervals as instance variables to be used in update_plot
        self.smoother = smoother
        self.low = low
        self.up = up
        # create a new DataFrame to hold the smoothed data
        self.df_smoothed = self.df_to_plot.copy()

        # add smoothed column to df_smoothed
        self.df_smoothed[self.y_column + "_SMOOTHED"] = self.smoother.smooth_data[0]
        self.update_plot_with_smoothed_data()

    if smoother_name == "Spline":
        # retrieve parameter values from GUI
        splinetypebox = self.smoothing_options.layout().itemAt(1).widget().currentText()
        n_knot_box = self.smoothing_options.layout().itemAt(3).widget().value()
        knot_box = self.smoothing_options.layout().itemAt(5).widget().value()
        interval_type = self.smoothing_options.layout().itemAt(7).widget().currentText()

        # create and apply smoother
        smoother = tsmt.SplineSmoother(spline_type=splinetypebox, n_knots=n_knot_box, knots=knot_box)
        smoother.smooth(self.df_to_plot[self.y_column].values)  # smoothing applied on y values 

        # generate intervals
        low, up = smoother.get_intervals(interval_type)

        # set the smoother and intervals as instance variables to be used in update_plot
        self.smoother = smoother
        self.low = low
        self.up = up
        # create a new DataFrame to hold the smoothed data
        self.df_smoothed = self.df_to_plot.copy()

        # add smoothed column to df_smoothed
        self.df_smoothed[self.y_column + "_SMOOTHED"] = self.smoother.smooth_data[0]
        self.update_plot_with_smoothed_data()

    if smoother_name == "Gaussian":
        # retrieve parameter values from GUI
        sigmabox = self.smoothing_options.layout().itemAt(1).widget().value()
        n_knot_box = self.smoothing_options.layout().itemAt(3).widget().value()
        knot_box = self.smoothing_options.layout().itemAt(5).widget().value()
        interval_type = self.smoothing_options.layout().itemAt(7).widget().currentText()

        # create and apply smoother
        smoother = tsmt.GaussianSmoother(sigma=sigmabox, n_knots=n_knot_box, knots=knot_box)
        smoother.smooth(self.df_to_plot[self.y_column].values)  # smoothing applied on y values 

        # generate intervals
        low, up = smoother.get_intervals(interval_type)

        # set the smoother and intervals as instance variables to be used in update_plot
        self.smoother = smoother
        self.low = low
        self.up = up
        # create a new DataFrame to hold the smoothed data
        self.df_smoothed = self.df_to_plot.copy()

        # add smoothed column to df_smoothed
        self.df_smoothed[self.y_column + "_SMOOTHED"] = self.smoother.smooth_data[0]
        self.update_plot_with_smoothed_data()
    
    if smoother_name == "Lowess":
        # retrieve parameter values from GUI
        smoothfracbox = self.smoothing_options.layout().itemAt(1).widget().value()
        iterbox = self.smoothing_options.layout().itemAt(3).widget().value()
        batchsize_box = self.smoothing_options.layout().itemAt(5).widget().value()
        interval_type = self.smoothing_options.layout().itemAt(7).widget().currentText()

        # create and apply smoother
        smoother = tsmt.LowessSmoother(smooth_fraction=smoothfracbox, iterations=iterbox, batch_size=batchsize_box)
        smoother.smooth(self.df_to_plot[self.y_column].values)  # smoothing applied on y values 

        # generate intervals
        low, up = smoother.get_intervals(interval_type)

        # set the smoother and intervals as instance variables to be used in update_plot
        self.smoother = smoother
        self.low = low
        self.up = up
        # create a new DataFrame to hold the smoothed data
        self.df_smoothed = self.df_to_plot.copy()

        # add smoothed column to df_smoothed
        self.df_smoothed[self.y_column + "_SMOOTHED"] = self.smoother.smooth_data[0]
        self.update_plot_with_smoothed_data()

    if smoother_name == "Savitzky-Golay Filter":
        # retrieve parameter values from GUI
        windowlength = self.smoothing_options.layout().itemAt(1).widget().value()
        degreespinbox = self.smoothing_options.layout().itemAt(3).widget().value()
        # create a new DataFrame to hold the filtered data
        self.df_smoothed = self.df_to_plot.copy()
        # create and apply smoother
        self.df_smoothed[self.y_column] = sg.savgol_filter(self.df_to_plot[self.y_column].values, window_length=windowlength, polyorder=degreespinbox)
        self.df_smoothed[self.y_column + "_SMOOTHED"] = self.df_smoothed[self.y_column].values
        self.update_plot_with_scipyfilter_data()
    
    if smoother_name == "Butterworth Filter":
        # retrieve parameter values from GUI
        filterbox = self.smoothing_options.layout().itemAt(1).widget().value()
        critfreq_box = self.smoothing_options.layout().itemAt(3).widget().value()
        passbox = self.smoothing_options.layout().itemAt(5).widget().currentText()
        
        # create a new DataFrame to hold the filtered data
        self.df_smoothed = self.df_to_plot.copy()

        b, a = sg.butter(filterbox, critfreq_box, btype=passbox)
        self.df_smoothed[self.y_column] = sg.filtfilt(b, a, self.df_to_plot[self.y_column].values)
        self.df_smoothed[self.y_column + "_SMOOTHED"] = self.df_smoothed[self.y_column].values
        self.update_plot_with_scipyfilter_data()
