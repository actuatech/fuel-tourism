import pandas as pd
import plotly.express as px


def stock_per_category_pie_chart(categorized_vehicles_df: pd.DataFrame, output_folder: str) -> px.Figure:
    """
    Pie Chart of the stock by Category

    :param categorized_vehicles_df: Dataframe of the categorized vehicles registration list
    :param output_folder: output folder name where to store resulting chart
    :return: a plotly.Figure containing the whole Stock distribution pie chart
    """
    data = categorized_vehicles_df.groupby(['Category']).count()['Stock'].reset_index()
    pie_chart = px.pie(data, values='Stock', names='Category',
                       title='Estoc segons tipologia de vehicle')
    pie_chart.update_traces(
        textinfo='percent+value',
        texttemplate= '%{value:0f} \n\  %{percent:0%f}'
    )

    pie_chart.update_layout(
        title_x=0.5
    )
    pie_chart.show()
    filename = output_folder + "Estoc segons tipologia de vehicle.html"
    pie_chart.write_html(filename)
