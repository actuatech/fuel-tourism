import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from Classification import CATEGORIES


def euro_distribution_pie_charts(categorized_vehicles_df: pd.DataFrame, output_folder: str) -> go.Figure:
    """
    Figure containing the Euro distribution pie chart for every Category

    :param categorized_vehicles_df: Dataframe of the categorized vehicles registration list
    :param output_folder: output folder name where to store resulting chart
    :return: an html file containing the EURO distribution pie charts per each Category
    """
    # Subplots definition
    specs = [[{'type': 'domain'}, {'type': 'domain'}], [{'type': 'domain'}, {'type': 'domain'}],
             [{'type': 'domain'}, {'type': 'domain'}]]
    pie_charts = make_subplots(rows=3, cols=2, specs=specs, horizontal_spacing=0.01, vertical_spacing=0.06,
                               subplot_titles=(f"{CATEGORIES[0]}", f"{CATEGORIES[1]}", f"{CATEGORIES[2]}",
                                               f"{CATEGORIES[3]}", f"{CATEGORIES[4]}"))
    rows = [1, 1, 2, 2, 3, 3]

    # Creation of each subplot, one per category
    for i, category in enumerate(CATEGORIES):
        col = 2 if i % 2 == 1 else 1
        df = categorized_vehicles_df[categorized_vehicles_df['Category'] == category]
        data = df.groupby(['Euro Standard']).count()['Stock'].reset_index()
        legend_group = 'group2' if i == 2 or i == 3 else 'group1'
        pie_charts.add_trace(go.Pie(
            labels=data['Euro Standard'],
            values=data['Stock'],
            textinfo='percent+value',
            texttemplate='%{value:0f}\n\ %{percent:0%f}',
            legendgroup=legend_group
        ), rows[i], col)

    pie_charts.update_layout(
        title="Distribució de l'estoc de vehicles, per cada categoria segons categories EURO",
        title_x=0.5,
        height=1200,
        width=1000,
        legend={'traceorder': 'grouped'}
    )

    pie_charts.show()
    filename = output_folder + "Distribució Euro per categoria.html"
    pie_charts.write_html(filename)
