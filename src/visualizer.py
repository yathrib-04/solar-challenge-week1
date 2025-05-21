"""
Data visualization module for solar data analysis.
"""
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VisualizationError(Exception):
    """Custom exception for visualization errors."""
    pass

class SolarDataVisualizer:
    """
    A class for creating visualizations of solar data.
    
    Attributes:
        combined_df (pd.DataFrame): Combined data from all countries
        country_dfs (Dict[str, pd.DataFrame]): Dictionary of country-specific data
    """
    
    def __init__(self, combined_df: pd.DataFrame, country_dfs: Dict[str, pd.DataFrame]):
        """
        Initialize the SolarDataVisualizer.
        
        Args:
            combined_df: Combined DataFrame with all countries' data
            country_dfs: Dictionary of individual country DataFrames
            
        Raises:
            VisualizationError: If data validation fails
        """
        self.combined_df = combined_df
        self.country_dfs = country_dfs
        self._validate_data()
    
    def _validate_data(self) -> None:
        """
        Validate the input data.
        
        Raises:
            VisualizationError: If data validation fails
        """
        required_columns = ['Country', 'GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'RH']
        missing_cols = set(required_columns) - set(self.combined_df.columns)
        
        if missing_cols:
            raise VisualizationError(f"Missing required columns: {missing_cols}")
        
        if not all(country in self.country_dfs for country in self.combined_df['Country'].unique()):
            raise VisualizationError("Missing country data in country_dfs")
    
    def create_comparative_boxplots(self) -> go.Figure:
        """
        Create box plots comparing key variables across countries.
        
        Returns:
            Plotly figure object
            
        Raises:
            VisualizationError: If visualization fails
        """
        try:
            fig = make_subplots(rows=2, cols=2,
                              subplot_titles=('GHI by Country', 'Temperature by Country',
                                            'Wind Speed by Country', 'Humidity by Country'))
            
            fig.add_trace(go.Box(x=self.combined_df['Country'], y=self.combined_df['GHI'],
                                name='GHI'), row=1, col=1)
            fig.add_trace(go.Box(x=self.combined_df['Country'], y=self.combined_df['Tamb'],
                                name='Temperature'), row=1, col=2)
            fig.add_trace(go.Box(x=self.combined_df['Country'], y=self.combined_df['WS'],
                                name='Wind Speed'), row=2, col=1)
            fig.add_trace(go.Box(x=self.combined_df['Country'], y=self.combined_df['RH'],
                                name='Humidity'), row=2, col=2)
            
            fig.update_layout(height=800, title_text="Comparative Analysis of Key Variables")
            logger.info("Successfully created comparative boxplots")
            return fig
            
        except Exception as e:
            raise VisualizationError(f"Error creating comparative boxplots: {str(e)}")
    
    def create_distribution_plots(self) -> go.Figure:
        """
        Create distribution plots for key variables.
        
        Returns:
            Plotly figure object
            
        Raises:
            VisualizationError: If visualization fails
        """
        try:
            fig = make_subplots(rows=2, cols=2,
                              subplot_titles=('GHI Distribution', 'Temperature Distribution',
                                            'Wind Speed Distribution', 'Humidity Distribution'))
            
            for country, df in self.country_dfs.items():
                fig.add_trace(go.Violin(x=[country]*len(df), y=df['GHI'],
                                      name=f'{country} GHI'), row=1, col=1)
                fig.add_trace(go.Violin(x=[country]*len(df), y=df['Tamb'],
                                      name=f'{country} Temp'), row=1, col=2)
                fig.add_trace(go.Violin(x=[country]*len(df), y=df['WS'],
                                      name=f'{country} WS'), row=2, col=1)
                fig.add_trace(go.Violin(x=[country]*len(df), y=df['RH'],
                                      name=f'{country} RH'), row=2, col=2)
            
            fig.update_layout(height=800, title_text="Distribution Analysis Across Countries")
            logger.info("Successfully created distribution plots")
            return fig
            
        except Exception as e:
            raise VisualizationError(f"Error creating distribution plots: {str(e)}")
    
    def create_correlation_heatmaps(self) -> Dict[str, go.Figure]:
        """
        Create correlation heatmaps for each country.
        
        Returns:
            Dictionary of Plotly figure objects
            
        Raises:
            VisualizationError: If visualization fails
        """
        try:
            variables = ['GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'RH']
            heatmaps = {}
            
            for country, df in self.country_dfs.items():
                corr_matrix = df[variables].corr()
                fig = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='RdBu',
                    zmin=-1, zmax=1
                ))
                fig.update_layout(title=f'{country} Correlation Heatmap')
                heatmaps[country] = fig
            
            logger.info("Successfully created correlation heatmaps")
            return heatmaps
            
        except Exception as e:
            raise VisualizationError(f"Error creating correlation heatmaps: {str(e)}")
    
    def create_seasonal_plots(self) -> go.Figure:
        """
        Create seasonal pattern plots.
        
        Returns:
            Plotly figure object
            
        Raises:
            VisualizationError: If visualization fails
        """
        try:
            if 'Month' not in self.combined_df.columns:
                raise VisualizationError("Month column not found in data")
            
            fig = make_subplots(rows=2, cols=2,
                              subplot_titles=('GHI by Month', 'Temperature by Month',
                                            'Wind Speed by Month', 'Humidity by Month'))
            
            for country, df in self.country_dfs.items():
                monthly_avg = df.groupby('Month').agg({
                    'GHI': 'mean',
                    'Tamb': 'mean',
                    'WS': 'mean',
                    'RH': 'mean'
                }).reset_index()
                
                fig.add_trace(go.Scatter(x=monthly_avg['Month'], y=monthly_avg['GHI'],
                                       name=f'{country} GHI'), row=1, col=1)
                fig.add_trace(go.Scatter(x=monthly_avg['Month'], y=monthly_avg['Tamb'],
                                       name=f'{country} Temp'), row=1, col=2)
                fig.add_trace(go.Scatter(x=monthly_avg['Month'], y=monthly_avg['WS'],
                                       name=f'{country} WS'), row=2, col=1)
                fig.add_trace(go.Scatter(x=monthly_avg['Month'], y=monthly_avg['RH'],
                                       name=f'{country} RH'), row=2, col=2)
            
            fig.update_layout(height=800, title_text="Seasonal Patterns Across Countries")
            logger.info("Successfully created seasonal plots")
            return fig
            
        except Exception as e:
            raise VisualizationError(f"Error creating seasonal plots: {str(e)}")
    
    def create_diurnal_plots(self) -> go.Figure:
        """
        Create diurnal pattern plots.
        
        Returns:
            Plotly figure object
            
        Raises:
            VisualizationError: If visualization fails
        """
        try:
            if 'Hour' not in self.combined_df.columns:
                raise VisualizationError("Hour column not found in data")
            
            fig = make_subplots(rows=2, cols=2,
                              subplot_titles=('GHI by Hour', 'Temperature by Hour',
                                            'Wind Speed by Hour', 'Humidity by Hour'))
            
            for country, df in self.country_dfs.items():
                hourly_avg = df.groupby('Hour').agg({
                    'GHI': 'mean',
                    'Tamb': 'mean',
                    'WS': 'mean',
                    'RH': 'mean'
                }).reset_index()
                
                fig.add_trace(go.Scatter(x=hourly_avg['Hour'], y=hourly_avg['GHI'],
                                       name=f'{country} GHI'), row=1, col=1)
                fig.add_trace(go.Scatter(x=hourly_avg['Hour'], y=hourly_avg['Tamb'],
                                       name=f'{country} Temp'), row=1, col=2)
                fig.add_trace(go.Scatter(x=hourly_avg['Hour'], y=hourly_avg['WS'],
                                       name=f'{country} WS'), row=2, col=1)
                fig.add_trace(go.Scatter(x=hourly_avg['Hour'], y=hourly_avg['RH'],
                                       name=f'{country} RH'), row=2, col=2)
            
            fig.update_layout(height=800, title_text="Diurnal Patterns Across Countries")
            logger.info("Successfully created diurnal plots")
            return fig
            
        except Exception as e:
            raise VisualizationError(f"Error creating diurnal plots: {str(e)}")
    
    def save_figures(self, figures: Dict[str, go.Figure], output_dir: Union[str, Path]) -> None:
        """
        Save figures to files.
        
        Args:
            figures: Dictionary of figure names and Plotly figure objects
            output_dir: Directory to save figures to
            
        Raises:
            VisualizationError: If saving fails
        """
        try:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for name, fig in figures.items():
                output_path = output_dir / f"{name}.html"
                fig.write_html(str(output_path))
            
            logger.info(f"Successfully saved figures to {output_dir}")
            
        except Exception as e:
            raise VisualizationError(f"Error saving figures: {str(e)}") 