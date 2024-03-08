# Advanced code for the visualization module
import plotly.express as px
import plotly.graph_objects as go

# Improved interactive scatter plot function with more customization options
def create_interactive_scatter_advanced(df, x_column, y_column, color_column=None, size_column=None, marker_symbol='circle'):
    fig = px.scatter(df, x=x_column, y=y_column,
                     color=color_column, size=size_column,
                     symbol=marker_symbol)
    fig.update_traces(marker=dict(line=dict(width=2,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    fig.show()

# New function for creating interactive time series plots
def create_interactive_time_series(df, x_column, y_column, title='Time Series Plot', highlight=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[x_column], y=df[y_column], mode='lines+markers', name=y_column))
    if highlight is not None:
        for point in highlight:
            fig.add_vline(x=point, line_width=2, line_dash="dash", line_color="red")
    fig.update_layout(title=title,
                      xaxis_title=x_column,
                      yaxis_title=y_column)
    fig.show()
