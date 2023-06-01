# Data Cleaning App

Use this app to clean the data from your experiments. 

I designed it because I was frustrated with the noise in my data that had to be always cleaned before I could train ML models.

## Getting Started

Load the file using the "Open File" button from the "File" button in the Menu Bar.

Alternatively, click on the "Select Data File" button.

The selected file's name will be shown in the the box below it.

## Features

1) Smoothing types

A lot of smoothers have been built into this app. Majority of them make use of the tsmoothie library.

Here's the link to the tsmoothie library: https://github.com/cerlymarco/tsmoothie.

Most of the functionalities have been baked in from the library. 

Additionally, the Savitzky-Golay (SavGol) and Butterworth filters have also been incoporated in this app. You can use any of them.

Select any of the filter types after you have loaded your file (not before).

2) Data Trim Index

Sometimes the experimental data has 0 values in it due to a slack in the system. Quite common for materials science experiment.

You can trim it with the help of the "Data Trim Index" Spin Box and apply your smoothing after that (or before, however you prefer).

Your new data, which has been smoothed, will follow this data trimming.

3) Apply and Remove Smoothing

Once you are satisfied with your smoothing parameters, click the appropriate button to apply or remove the filters.

You can visualize the cleaning with the help of the Matplotlib canvas on the right.

Sometimes the plot may reset when you are changing the parameters. Just toggle the spinbox from the option below and that'll fix it.

4) Displaying Raw Data

Sometimes it's useful to see how the smoothing behaves with respect to the raw data. Uncheck or check this box as you see fit.

By default, raw data is always displayed.

5) First Derivative

I've found it helpful to see the dy/dx values of the loaded dataframe. Clicking this button pops out a new canvas and a new graph of this.

The "Data Trim Index" functionality is applied here as well, so you can tweak it as you see fit.

6) Export Data

Click the button on the bottom-right to export the smoothed CSV data. The smoothed y-column will be appended in the new CSV file.

### Contact and Contribution

If you have any questions or need support, contact me on LinkedIn. Link to my profile: https://www.linkedin.com/in/aniketjnuclear/

You can also contribute to this code via the Github repo.

Thanks for using this.
