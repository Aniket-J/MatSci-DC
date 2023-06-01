import os
from pathlib import Path
from PyQt6.QtWidgets import *
import pandas as pd

home_dir = os.path.expanduser('~')

def Openfile(parent):
    file, _ = QFileDialog.getOpenFileName(parent.window(), 'Open file', home_dir, "CSV files (*.csv)")
    fname = os.path.basename(file)
    fullpath = os.path.abspath(file)
    return fname, fullpath

def load_data(filepath):
    df = pd.read_csv(filepath)
    
    # Check if the first row contains text
    first_row = df.iloc[0]
    if first_row.apply(lambda x: isinstance(x, str)).any():
        df = df.drop(labels=0, axis=0)
    
    # Convert all columns to float
    df = df.astype(float)
    
    return df
