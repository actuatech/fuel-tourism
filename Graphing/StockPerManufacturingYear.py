import pandas as pd
import plotly.express as px
from typing import Dict, List

from Classification import HYBRID_PHEV_TYPES


def figures_to_html(figs, filename="dashboard.html"):
    dashboard = open(filename, 'w')
    dashboard.write("<html><head></head><body>" + "\n")
    for fig in figs:
        inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
        dashboard.write(inner_html)
    dashboard.write("</body></html>" + "\n")


def categories_grouping(row):
    """Group hybrid and PHEV type without segment associated to avoid too large segmentations when plotting"""
    if row['Fuel'] == 'Battery Electric':
        return 'Battery Electric'
    if row['Fuel'] in HYBRID_PHEV_TYPES:
        if 'Hybrid' in row['Fuel']:
            return 'Hybrid'
        else:
            return 'PHEV'
    else:
        result = row['Fuel'] + ' ' + row['Segment']
        return result


def update_chart_layout(figure, title: str = None):
    figure.update_layout(
        title=title,
        title_x=0.4,
        legend_title='',
        height=600,
        width=800,
        template='plotly_white',
        xaxis_title='Any de fabricació',
        yaxis_title='Estoc'
    )


def add_annotation_to_chart(figure, data: pd.DataFrame, category: str):
    figure.add_annotation(
        x=data['ANY_FABRICACIO'].min() + (data['ANY_FABRICACIO'].max() - data['ANY_FABRICACIO'].min()) / 2,
        y=data.groupby(['ANY_FABRICACIO']).sum()['Stock'].max() * 1.15,
        xanchor='center', yanchor='top',
        font={'size': 16}, text=category, showarrow=False)


def create_chart_with_segmentation_and_colors_configuration(data: pd.DataFrame, category_orders: Dict, colors: List):
    fig = px.bar(data,
                 x='ANY_FABRICACIO', y='Stock', color="segmentation",
                 category_orders=category_orders,
                 color_discrete_sequence=colors
                 )
    return fig


def stock_per_manufacturing_year_and_category_bar_charts(categorized_vehicles_df: pd.DataFrame, output_folder: str):
    """
    Save to and html file a bar chart representing the stock distribution per year of manufacturing, per segment and
    per fuel type. One chart for each vehicle category
    :param categorized_vehicles_df: Dataframe of the categorized vehicles registration list
    :param output_folder: output folder name where to store resulting chart
    :return: an html file containing the 5 bar charts, one for each vehicle Category
    """
    # Passenger Cars chart:
    data = categorized_vehicles_df[categorized_vehicles_df.Category == 'Passenger Cars'].groupby(
        ['Fuel', 'Segment', 'ANY_FABRICACIO'], dropna=False).sum().reset_index()
    data['segmentation'] = data.apply(lambda row: categories_grouping(row), axis=1)

    colors = ['rgb(0,68,27)', 'rgb(35,139,69)', 'rgb(199,233,192)',
              'rgb(8,48,107)', 'rgb(33,113,181)', 'rgb(107,174,214)', # 'rgb(198,219,239)', # Color for Diesel Mini
              'rgb(127,39,4)', 'rgb(217,72,1)', 'rgb(253,141,60)', 'rgb(253,208,162)'
              ]
    category_orders = {"segmentation": ['Battery Electric', 'PHEV', 'Hybrid',
                                        'Diesel Large-SUV-Executive', 'Diesel Medium', 'Diesel Small',
                                        'Diesel Mini',
                                        'Petrol Large-SUV-Executive', 'Petrol Medium', 'Petrol Small',
                                        'Petrol Mini']
                       }

    fig = create_chart_with_segmentation_and_colors_configuration(data, category_orders, colors)
    update_chart_layout(fig, 'Parc de vehicles actius per any de fabricació i tipologia')
    add_annotation_to_chart(fig, data, "Passenger Cars")
    fig.show()

    # Light Commercial Vehicles Chart
    data = categorized_vehicles_df[categorized_vehicles_df.Category == 'Light Commercial Vehicles'].groupby(
        ['Fuel', 'Segment', 'ANY_FABRICACIO'], dropna=False).sum().reset_index()
    data['segmentation'] = data.apply(lambda row: categories_grouping(row), axis=1)

    colors = ['rgb(0,68,27)',
              'rgb(8,48,107)', 'rgb(33,113,181)', 'rgb(107,174,214)',
              'rgb(127,39,4)', 'rgb(217,72,1)', 'rgb(253,141,60)', 'rgb(199,233,192)', 'rgb(247,252,245)'
              ]
    category_orders = {"segmentation": ['Battery Electric', 'Diesel N1-I', 'Diesel N1-II',
                                        'Diesel N1-III', 'Petrol N1-I', 'Petrol N1-II', 'Petrol N1-III',
                                        'Hybrid']
                       }
    fig2 = create_chart_with_segmentation_and_colors_configuration(data, category_orders, colors)
    update_chart_layout(fig2)
    add_annotation_to_chart(fig2, data, "Light Commercial Vehicles")
    fig2.show()

    # Heavy Duty Trucks
    data = categorized_vehicles_df[categorized_vehicles_df.Category == 'Heavy Duty Trucks'].groupby(
        ['Fuel', 'Segment', 'ANY_FABRICACIO'], dropna=False).sum().reset_index()
    data['segmentation'] = data.apply(lambda row: categories_grouping(row), axis=1)

    colors = [
        'rgb(8,48,107)', 'rgb(8,81,156)', 'rgb(33,113,181)', 'rgb(66,146,198)', 'rgb(107,174,214)', 'rgb(158,202,225)',
        'rgb(198,219,239)', 'rgb(199,233,192)',
        'rgb(222,235,247)', 'rgb(247,251,255)'
    ]
    category_orders = {"segmentation": ['Diesel Rigid <=7,5 t',
                                        'Diesel Rigid 7,5 - 12 t',
                                        'Diesel Rigid 12 - 14 t',
                                        'Diesel Rigid 14 - 20 t',
                                        'Diesel Rigid 20 - 26 t',
                                        'Diesel Rigid 26 - 28 t',
                                        'Diesel Rigid 28 - 32 t',
                                        'Hybrid']
                       }
    fig3 = create_chart_with_segmentation_and_colors_configuration(data, category_orders, colors)
    update_chart_layout(fig3)
    add_annotation_to_chart(fig3, data, "Heavy Duty Trucks")
    fig3.show()

    # Buses
    data = categorized_vehicles_df[categorized_vehicles_df.Category == 'Buses'].groupby(
        ['Fuel', 'Segment', 'ANY_FABRICACIO'], dropna=False).sum().reset_index()
    data['segmentation'] = data.apply(lambda row: categories_grouping(row), axis=1)

    colors = [
        'rgb(8,48,107)', 'rgb(33,113,181)', 'rgb(107,174,214)', 'rgb(199,233,192)',
        'rgb(247,251,255)', 'rgb(222,235,247)', 'rgb(198,219,239)', 'rgb(158,202,225)'
    ]
    category_orders = {"segmentation": ['Diesel Urban Buses Midi <=15 t',
                                        'Diesel Urban Buses Standard 15 - 18 t',
                                        'Diesel Urban Buses Articulated >18 t',
                                        'Hybrid']
                       }
    fig4 = create_chart_with_segmentation_and_colors_configuration(data, category_orders, colors)
    update_chart_layout(fig4)
    add_annotation_to_chart(fig4, data, "Buses")
    fig4.show()

    # L-Category
    data = categorized_vehicles_df[categorized_vehicles_df.Category == 'L-Category'].groupby(
        ['Fuel', 'Segment', 'ANY_FABRICACIO'], dropna=False).sum().reset_index()
    data['segmentation'] = data.apply(lambda row: categories_grouping(row), axis=1)

    colors = ['rgb(0,68,27)',  # electric
              # Petrol
              'rgb(127,39,4)',
              'rgb(217,72,1)',
              'rgb(253,141,60)',
              'rgb(253,208,162)',
              # Diesel
              'rgb(107,174,214)', 'rgb(203,24,29)', 'rgb(165,15,21)', 'rgb(103,0,13)'
              ]
    category_orders = {"segmentation": ['Battery Electric',
                                        'Petrol Mopeds 2-stroke <50 cm³',
                                        'Petrol Motorcycles 4-stroke <250 cm³',
                                        'Petrol Motorcycles 4-stroke 250 - 750 cm³',
                                        'Petrol Motorcycles 4-stroke >750 cm³',
                                        'Diesel Motorcycles 4-stroke >750 cm³']
                       }
    fig5 = create_chart_with_segmentation_and_colors_configuration(data, category_orders, colors)
    update_chart_layout(fig5)
    add_annotation_to_chart(fig5, data, "L-Category")
    fig5.show()

    # Save figures to html file
    figs = [fig, fig2, fig3, fig4, fig5]
    filename = output_folder + "Parc de vehicles actius per any de fabricació i tipologia.html"
    figures_to_html(figs, filename)

