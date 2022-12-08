import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc, dash_table, html
from dash.dependencies import Output, Input

from variables import df, table_dict_list, option_dict, option_dict_num, option_dict_all,churn_rate_list, dist_list, scatter_list
from showoff import fig_corr


app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(
    [   
        html.Div(
            className = "main_Frame",
            children = [
                html.H1("Churn Data Visualizations", className = "page_Title"),    
                dcc.Tabs(
                    id = "tab_frame", value = "graphs",
                    children = [
                        dcc.Tab(label = 'Graphs', value = 'graphs'),
                        dcc.Tab(label = 'Tables', value = 'tables')
                    ]
                ),   
                html.Div(id = "tabs_content")
            ]
        ),
    ],
)

@app.callback(
    Output('tabs_content', 'children'),
    Input('tab_frame', 'value')
    )
def render_content(tab):
    if tab == 'tables':
        return html.Div(
            [   
                html.Div(className = "Spacer"),
                html.Span("Select a Feature and it\'s respective value:"),
                dcc.Dropdown(
                    id = "feat_dropdown", 
                    options = list(option_dict.keys()), 
                    value = list(option_dict.keys())[0]
                ),
                dcc.RadioItems(id = "cats_radio"),
                dash_table.DataTable(
                    id = "table",
                    columns = table_dict_list,
                    data = df.to_dict("records"),
                    style_table = {"height": "300px", "overflowY": "auto"},
                )   
            ]
        )
    elif tab == 'graphs':
        return html.Div(
            className = "graph_tab",
            children = [   
                html.Div(className = "Spacer"),

                html.Div(
                    className = "graphs_row_1",
                    children = [
                        html.Div(
                            className = "churn_container",
                            children = [
                                html.H3(
                                    "Average Churn Rates",
                                    id = "text_span"
                                    ),
                                html.Div(
                                    className = "drop_container",
                                    children = [
                                        dcc.Dropdown(
                                            id = "churn_drop",
                                            options = churn_rate_list,
                                            value = churn_rate_list[0]
                                        )
                                    ]
                                ),
                                dcc.Graph(id = "graphs_churn")
                            ]
                        ),
                        html.Div(
                            className = "dist_container",
                            children = [
                                html.H3(
                                    "Data Distribution",
                                    id = "text_span"
                                    ),
                                html.Div(
                                    className = "drop_container",
                                    children = [
                                        dcc.Dropdown(
                                            id = "dist_drop",
                                            options = dist_list,
                                            value = dist_list[0]
                                        )
                                    ]
                                ),
                                dcc.Graph(id = "graphs_dist")
                            ]
                        ),
                        html.Div(
                            className = "scatter_container",
                            children = [
                                html.H3(
                                    "Correlation Scatter against Churn",
                                    id = "text_span"
                                    ),
                                html.Div(
                                    className = "scatter_drop_container",
                                    children = [
                                        html.Div(
                                            dcc.Dropdown(
                                                id = "scatter_drop_1",
                                                options = scatter_list,
                                                value = scatter_list[1]
                                            )
                                        ),
                                        html.Div(
                                            dcc.Dropdown(
                                                id = "scatter_drop_2",
                                                options = scatter_list,
                                                value = scatter_list[0]
                                            )
                                        )
                                    ]
                                ),
                                dcc.Graph(id = "graphs_scatter")
                            ]
                        )
                    ]                   
                ),

                html.Div(className = "Spacer_2"),

                html.Div(
                    className = "graphs_row_2",
                    children = [
                        html.Div(
                            className = "corrs_container",
                            children = [
                                html.H3(
                                    "Correlation Show-Off",
                                    id = "text_span"
                                    ),
                                dcc.Graph(
                                    id = "graphs_corrs",
                                    figure = fig_corr
                                )
                            ]
                        )
                    ]
                )
            ]
        )


## table dropdown
@app.callback(
    Output("cats_radio", "options"),
    Input("feat_dropdown", "value"),
    )
def get_option_drop(selected_feature):
    return [ {"label": i, "value": i} for i in option_dict[selected_feature] ]

## table radio
@app.callback(
    Output("cats_radio", "value"),
    Input("cats_radio", "options"))
def set_cat_value(available):
    return available[0]["value"]

## table
@app.callback(
    Output("table", "data"),
    Input("feat_dropdown", "value"),
    Input("cats_radio","value")
    )
def get_option_rad(feature, available):
    if available == "All":
        return df.to_dict("records")
    else:
        return df[df[feature] == available].to_dict("records")

## churn dropdown
@app.callback(
    Output("churn_drop", "value"),
    Input("churn_drop", "value"))
def set_cat_value(compare_value):
    return compare_value

## churn fig
@app.callback(
    Output("graphs_churn", "figure"),
    Input("churn_drop", "value"))
def make_fig(compare_value):

    df_temp = df.groupby(compare_value)["Churned"].mean().reset_index()

    fig_1 = go.Figure()
    fig_1.layout.template = "ggplot2"
    fig_1.add_trace(
        go.Bar(
            x = df_temp[compare_value],
            y = df_temp["Churned"] * 100,
            name = compare_value
        )
    )

    fig_1.update_layout(
    xaxis_title_text = compare_value,
    yaxis_title_text = "Churn Rate in %",
    barmode = 'group', bargap = 0.10, bargroupgap = 0.1,
    margin = {'t': 30, "b": 5},
    height = 300
    )

    return fig_1

## dist dropdown
@app.callback(
    Output("dist_drop", "value"),
    Input("dist_drop", "value"))
def set_cat_value(dist_value):
    return dist_value

## dist fig
@app.callback(
    Output("graphs_dist", "figure"),
    Input("dist_drop", "value"))
def make_fig(dist_value):

    fig_2 = go.Figure()
    fig_2.layout.template = "seaborn"
    fig_2.add_trace(
        go.Histogram(
            x = df[dist_value],
            name = dist_value
        )
    )

    fig_2.update_layout(
    xaxis_title_text = dist_value,
    yaxis_title_text = "Counts",
    barmode = 'group', bargap = 0.10, bargroupgap = 0.1,
    margin = {'t': 30, "b": 5},
    height = 300
    )

    return fig_2


## scatter dropdown_1
@app.callback(
    Output("scatter_drop_1", "value"),
    Input("scatter_drop_1", "value"))
def set_cat_value(scatter_value_1):
    return scatter_value_1

## scatter dropdown_2
@app.callback(
    Output("scatter_drop_2", "value"),
    Input("scatter_drop_2", "value"))
def set_cat_value(scatter_value_2):
    return scatter_value_2

## scatter fig
@app.callback(
    Output("graphs_scatter", "figure"),
    Input("scatter_drop_1", "value"),
    Input("scatter_drop_2", "value"))
def make_fig(scatter_value_1, scatter_value_2):

    fig_3 = go.Figure()
    fig_3.layout.template = "ggplot2"
    fig_3.add_trace(
        go.Scatter(
            y = df[scatter_value_1],
            x = df[scatter_value_2],
            marker_color = df["Churned"],
            mode = "markers"
        )
    )

    fig_3.update_layout(
    yaxis_title_text = scatter_value_1,
    xaxis_title_text = scatter_value_2,
    barmode = 'group', bargap = 0.10, bargroupgap = 0.1,
    margin = {'t': 30, "b": 5},
    height = 300
    )

    return fig_3







if __name__ == "__main__":
    app.run_server(debug=True, port=8085)