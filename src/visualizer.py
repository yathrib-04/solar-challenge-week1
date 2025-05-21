import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from windrose import WindroseAxes
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np

class Visualizer:
    """Class for creating various visualizations of solar data."""
    
    def __init__(self):
        """Initialize the Visualizer with default style settings."""
        plt.style.use('seaborn')
        sns.set_palette('husl')
        
    def plot_time_series(self, time_series: Dict[str, pd.Series], 
                        figsize: Tuple[int, int] = (15, 10)) -> None:
        """
        Plot multiple time series in a grid.
        
        Args:
            time_series (Dict[str, pd.Series]): Dictionary of time series data
            figsize (Tuple[int, int]): Figure size
        """
        n_plots = len(time_series)
        n_cols = min(2, n_plots)
        n_rows = (n_plots + 1) // 2
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.ravel()
        
        for idx, (name, series) in enumerate(time_series.items()):
            series.plot(ax=axes[idx], title=f'{name} over Time')
            
        plt.tight_layout()
        plt.show()
        
    def plot_correlation_heatmap(self, correlation_matrix: pd.DataFrame, 
                               figsize: Tuple[int, int] = (10, 8)) -> None:
        """
        Plot correlation heatmap.
        
        Args:
            correlation_matrix (pd.DataFrame): Correlation matrix
            figsize (Tuple[int, int]): Figure size
        """
        plt.figure(figsize=figsize)
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Heatmap')
        plt.show()
        
    def plot_wind_rose(self, wind_direction: np.ndarray, wind_speed: np.ndarray) -> None:
        """
        Plot wind rose.
        
        Args:
            wind_direction (np.ndarray): Wind direction data
            wind_speed (np.ndarray): Wind speed data
        """
        ax = WindroseAxes.from_ax()
        ax.bar(wind_direction, wind_speed, normed=True, opening=0.8, edgecolor='white')
        ax.set_legend()
        plt.title('Wind Rose Plot')
        plt.show()
        
    def plot_temperature_humidity(self, data: pd.DataFrame) -> None:
        """
        Create bubble chart for temperature, GHI, and humidity relationship.
        
        Args:
            data (pd.DataFrame): DataFrame containing Tamb, GHI, and RH columns
        """
        fig = px.scatter(data, x='Tamb', y='GHI', size='RH',
                        title='Temperature vs GHI with Relative Humidity',
                        labels={'Tamb': 'Ambient Temperature',
                               'GHI': 'Global Horizontal Irradiance',
                               'RH': 'Relative Humidity'})
        fig.show()
        
    def plot_cleaning_impact(self, cleaning_stats: pd.DataFrame) -> None:
        """
        Plot cleaning impact on module performance.
        
        Args:
            cleaning_stats (pd.DataFrame): Statistics by cleaning status
        """
        cleaning_stats.plot(kind='bar', title='Module Performance by Cleaning Status')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show() 