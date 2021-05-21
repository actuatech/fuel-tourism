import plotly.express as px


def histogram_plot(df, colname: str, title: str, xaxes_title: str, nbins: int = 30):
    fig = px.histogram(df, x=colname,
                       nbins=nbins,
                       marginal='box',
                       labels=dict(x=colname),
                       template='plotly_white',
                       histnorm=None)
    fig.update_layout(
        # width=1500,
        # height=1500,
        hovermode='x unified',
        title=dict(text=title, x=0.5, xanchor='center')
    )
    fig.update_xaxes(title=dict(text=xaxes_title))
    fig.update_yaxes(title=dict(text='Recompte'))
    pass
