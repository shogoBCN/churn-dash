from variables import df
import pandas as pd
import plotly.graph_objects as go

df_corr = df.corr()
df_ex_corr = pd.DataFrame(df_corr["Churned"]).reset_index()
df_ex_corr.rename(columns={"index":"Feature"}, inplace=True)
df_ex_corr.sort_values('Churned', ascending=True, inplace=True)
df_ex_corr = df_ex_corr[0:8]

mean_corr = df_ex_corr["Churned"].mean()

fig_corr = go.Figure()
fig_corr.add_trace(
    go.Bar(
        x = df_ex_corr["Churned"], 
        y = df_ex_corr["Feature"],
        text = round(df_ex_corr["Churned"], 2),
        orientation = 'h'
        )
    )

fig_corr.layout.template = "ggplot2"

fig_corr.update_layout(
    margin = {'t': 0, "b": 5},
    height = 300
    )

fig_corr.update_xaxes(
    title_text = "Correlations",
    range = [-0.2, 0.3], dtick = 0.05, tickangle = -45
    )

fig_corr.update_yaxes(
    showgrid = True,
    ticksuffix = "  "
    )

fig_corr.add_vline(
    x = mean_corr,
    line_width = 3, line_dash = 'dot', line_color = "MidnightBlue"
    )

fig_corr.add_annotation(
    x = 0.03, y = 0, xanchor = "left",
    text = "mean correlation = {}".format(round(mean_corr, 4)),
    font_color = "MidnightBlue",
    showarrow = False
    )