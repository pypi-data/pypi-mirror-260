# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 21:11:01 2024

@author: MOHAMMED
"""


# DataPrepKit: A Comprehensive Toolkit for Preprocessing Datasets

DataPrepKit is a Python package designed to streamline the preprocessing of datasets, offering a wide range of functionalities to assist data scientists, analysts, and developers in their data preparation tasks. Leveraging the power of NumPy and Pandas, DataPrepKit aims to provide intuitive and efficient solutions for common preprocessing challenges encountered in data analysis and machine learning projects.

## Features

DataPrepKit offers the following key features:

-   **Data Reading**: Read data from various file formats including CSV, Excel, JSON, and more, providing flexibility in data ingestion.
-   **Dataset Summarization**: Summarize datasets with descriptive statistics and visualizations to gain insights into the data distribution and characteristics.
-   **Handling Missing Values**: Efficiently manage missing values by imputing or dropping them based on user-defined strategies.
-   **Categorical Data Encoding**: Encode categorical variables using different methods such as one-hot encoding, label encoding, or target encoding.

## Installation

You can install DataPrepKit using pip:

bashCopy code

`pip install DataPrepKit_momoV` 

## Usage

Here's a brief overview of how to use DataPrepKit:

pythonCopy code

`import dataprepkit as dpk

# Read data from a CSV file
data =dpk.read_data(name.csv)

# Summarize the dataset
data.summary()

# Handle missing values
data.fill_missing_numbers()

# Encode categorical variables
catg_ecoding_col("column_name")

## Contribution

DataPrepKit is an open-source project, and contributions from the community are welcome! If you have any ideas for new features, improvements, or bug fixes, please feel free to open an issue or submit a pull request on GitHub.
