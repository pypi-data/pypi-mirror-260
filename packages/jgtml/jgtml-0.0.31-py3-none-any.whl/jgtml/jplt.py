import pandas as pd
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import seaborn as sns
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from jgtpy import JGTCDS as cds
from jgtml import jtc
from jgtpy import JGTPDSP as pds
import tlid

def _crop_dataframe(df, crop_last_dt: str = None, crop_start_dt: str = None,keep_amount=-1):
    if crop_last_dt is not None:
        df = df[df.index <= crop_last_dt]
    if crop_start_dt is not None:
        df = df[df.index >= crop_start_dt]
    
    if keep_amount > 0:
        df = df.tail(keep_amount)
    return df


def an_bivariate_plot00(data,
                        feature1='ao',
                        target_variable='target',
                        title = 'Bivariate Scatter Plot - ',
                        xlabel = '',
                        ylabel_prefix = '',
                        show=False          
                        ):
  # Scatter plot between target variable and a feature
  plt.scatter(data[feature1], data[target_variable])
  
  plt.title(title + feature1 + ' / ' + target_variable)
  
  plt.xlabel(xlabel + feature1)
  
  plt.ylabel(ylabel_prefix + target_variable)
  if show:plt.show()
  return plt.figure()
  
def an_biv_plt2ds(data1, 
                  data2, 
                  feature1='ao', 
                  feature2='ao', 
                  target_variable='target',
                  s0_title = 'Scatter Plot: ',
                  x0_prefix = "Feature1: ",
                  y0_prefix = "",
                  s1_title = 'Scatter Plot: ',
                  x1_prefix = '',
                  y1_prefix = '',
                  show=False
                  ):
  # Create a figure and two subplots with 1 row and 2 columns
  fig, axs = plt.subplots(1, 2, figsize=(10, 5))

  # Scatter plot between target variable and feature1 from data1
  axs[0].scatter(data1[feature1], data1[target_variable])
  
  axs[0].set_title(s0_title)
  
  axs[0].set_xlabel(x0_prefix + feature1)
  
  axs[0].set_ylabel(y0_prefix + target_variable)

  # Scatter plot between target variable and feature2 from data2
  axs[1].scatter(data2[feature2], data2[target_variable])
  
  axs[1].set_title(s1_title + " " + feature2 + " / " + target_variable )
  
  axs[1].set_xlabel(x1_prefix + feature2)
  
  axs[1].set_ylabel(y1_prefix + target_variable)

  # Display the plots
  plt.tight_layout()
  if show:
    plt.show()
  return fig



def an_bivariate_plot00_four_features_v2(data1, data2,data1_name,data2_name, feature1='ao', feature2='ao', feature3='ac', feature4='ac', target_variable='target', 
                                         title = 'Bivariate Analysis Scatter:',
                                         show=False):
  # Create a figure and four subplots with 2 rows and 2 columns
  fig, axs = plt.subplots(2, 2, figsize=(10, 10))

  # Scatter plot between target variable and feature1 from data1
  axs[0, 0].scatter(data1[feature1], data1[target_variable])
  axs[0, 0].set_title('Bivariate Analysis Scatter:' + data1_name + '/' + feature1)
  axs[0, 0].set_xlabel( feature1)
  axs[0, 0].set_ylabel( target_variable)

  # Scatter plot between target variable and feature2 from data2
  axs[0, 1].scatter(data2[feature2], data2[target_variable])
  
  axs[0, 1].set_title(title + data2_name + '/' + feature2)
  axs[0, 1].set_xlabel( feature2)
  axs[0, 1].set_ylabel( target_variable)

  # Scatter plot between target variable and feature3 from data1
  axs[1, 0].scatter(data1[feature3], data1[target_variable])
  axs[1, 0].set_title('Bivariate Analysis Scatter:' + data1_name + '/' + feature3)
  axs[1, 0].set_xlabel( feature3)
  axs[1, 0].set_ylabel( target_variable)

  # Scatter plot between target variable and feature4 from data2
  axs[1, 1].scatter(data2[feature4], data2[target_variable])
  axs[1, 1].set_title('Bivariate Analysis Scatter:' + data2_name + '/' + feature4)
  axs[1, 1].set_xlabel( feature4)
  axs[1, 1].set_ylabel( target_variable)

  # Display the plots
  plt.tight_layout()
  if show:
    plt.show()
  return fig


# %% PLot distribution
def an_distplot(df, feature='ao', title="Distribution of AO -",show=False):
  sns.histplot(df[feature], kde=False)
  
  plt.title(title + " " +  feature)
  
  if show:plt.show()
  return plt.figure()
  
  
def an_describe_summary_stat(data,target_var_name = 'target'):
  #print(data['target'].describe())
  # Summary statistics for the target variable  
  return data[target_var_name].describe()

def pairplot(data, title="Pairplot - ",show=False):
  sns.pairplot(data)
  plt.suptitle(title)
  if show:  plt.show()
  return plt.figure()
  
def pairgrid(data, title="Pairgrid - ",show=False):
  #sns.pairplot(iris)
  # Create a pairgrid with the data
  g = sns.PairGrid(data)
  g.map_upper(sns.scatterplot)
  g.map_lower(sns.kdeplot)
  g.map_diag(sns.histplot, kde=False)
  plt.suptitle(title)
  if show:  plt.show()
  return g