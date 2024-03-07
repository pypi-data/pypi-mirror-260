from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas


# code based on data_viewer.ipynb provided by supervisors in the beginning of course
def view(
    df: pandas.DataFrame,
    target_cols,
):
    fig = make_subplots(rows=(len(target_cols) + 1), cols=1, shared_xaxes=True)

    for i, _col in enumerate(target_cols):
        fig.append_trace(
            go.Scatter(x=df.index, y=df.loc[:, _col], name=_col),
            row=i + 1,
            col=1,
        )
    fig.show()
