"""
Plotting functions for AnnData.
"""

import numpy as np
from pandas import DataFrame
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from anndata import AnnData
from typing import Union
import warnings
import math

from ..get import check_indices


def plot_3d_score(
        adata: AnnData,
        obs_key,
        width: float = 7,
        height: float = 7,
        xlabel: str = 'x',
        ylabel: str = 'y',
        zlabel: str = '',
        title: str = '',
):
    check_indices(adata, obs_key)
    hypo_df = adata.obs[['array_row', 'array_col', obs_key]]
    # 10X visium spot 78row * 64col = 4992 total
    value_lt = []
    for row_idx in range(78):
        row_df = hypo_df[hypo_df['array_row'] == row_idx]
        row_item = [0] * 64
        for idx, row in row_df.iterrows():
            col_idx = row['array_col']
            col_idx2 = (col_idx + 1) / 2 - 1 if col_idx % 2 else col_idx / 2
            val = row[obs_key]
            row_item[int(col_idx2)] = round(val, 4)
        value_lt.append(row_item)
    z_value = np.array(value_lt).T
    sh0, sh1 = z_value.shape
    x = np.linspace(0, 1, sh1)
    y = np.linspace(0, 1, sh0)
    z = z_value
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Viridis')])
    # colorscale can pick in [Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,
    # Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd]
    fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                      highlightcolor="limegreen", project_z=True))
    if not title:
        title = obs_key
    if not zlabel:
        zlabel = obs_key
    fig.update_layout(title=title,
                      scene={
                          'xaxis_title': xlabel,
                          'yaxis_title': ylabel,
                          'zaxis_title': zlabel,
                      },
                      autosize=False,
                      # scene_camera_eye=dict(x=1.87, y=0.88, z=-0.64),  # set preview perspective
                      width=width * 100,
                      height=height * 100,
                      margin=dict(l=65, r=50, b=65, t=90))
    fig.show()


def violin(
        adata: AnnData,
        obs_key
):
    check_indices(adata, obs_key)
    sns.violinplot(adata.obs[obs_key], inner='box')


def plot_lever_core(
        cluster_df: DataFrame,
        core_type: Union['independent', 'adjacent'],
        core_num: int = 4,
        col_wrap: int = 4,
        width: float = 11.5,
        height: float = 3.5,
        xlabel: str = 'row',
        ylabel: str = 'col',
        title: str = '',
):
    df = cluster_df[cluster_df['class'] == core_type]
    idx_lt = [i for i, j in df['cluster_idx'].value_counts().items() if j > 3]  # keep cluster contain at least 3 spots
    if not idx_lt or df.shape[0] == 0:
        raise IOError(f'{core_type} core type is None or all core spot number <= 3, please check.')
    elif len(idx_lt) < core_num:
        warnings.warn(f'{core_type} number is less than {core_num}, total {len(idx_lt)} number is to plot!')
    df = df[df.cluster_idx.isin(idx_lt[: core_num])]
    fig = px.scatter(
        df,
        x='row',
        y='col',
        color="type",
        color_discrete_map={'lever1': 'red', 'lever2': 'orange'},
        facet_col="cluster_idx",
        facet_col_wrap=col_wrap,
        facet_row_spacing=0.03,  # default is 0.07 when facet_col_wrap is used
        category_orders={
            'cluster_idx': idx_lt[: core_num],
        }
    )
    n_block = math.ceil(core_num / 4)
    if not title:
        title = f'{core_type} type scatter，total {len(idx_lt)} cluster'
    fig.update_layout(title=title,
                      xaxis={'title': xlabel},
                      yaxis={'title': ylabel},
                      width=width * 100,
                      height=height * 100 * n_block,
                      showlegend=True, )
    fig.show()


def plot_cycle_bar(
        cluster_df: DataFrame,
        core_type=None,
        width: float = 6,
        height: float = 4,
        xlabel: str = 'cycle',
        ylabel: str = 'count',
        title: str = '',
):
    if core_type is None:
        pick_type = ['independent', 'adjacent']
    else:
        pick_type = [core_type]
    df = cluster_df[cluster_df['class'].isin(pick_type)]['cycle'].value_counts().reset_index()
    df = df[df['count'] > 10]  # keep cycle contain at least 10 spots
    x_order = sorted(df['cycle'].tolist())
    fig = px.bar(df, x='cycle', y='count', category_orders={'index': x_order})
    if not title:
        title = f'Spot number in every cycle of {",".join(pick_type)} type，total {len(x_order)} cycles'
    fig.update_layout(title=title,
                      xaxis={'title': xlabel},
                      yaxis={'title': ylabel},
                      width=width * 100,
                      height=height * 100, showlegend=True)
    fig.show()


def plot_cycle_abundance(
        cluster_df: DataFrame,
        cell_type_lt,
        width: float = 10,
        height: float = 4,
        xlabel: str = 'cycle',
        ylabel: str = 'cell abundance',
        title: str = 'Cell Abundance In Each Cycle',
):
    df = cluster_df[(cluster_df['class'].isin(['independent', 'adjacent'])) & ~(cluster_df['class'] == np.nan)]
    category_counts = cluster_df['cycle'].value_counts()
    df = df[df['cycle'].isin(category_counts[category_counts >= 10].index)]
    fig = px.histogram(df, x='cycle', y=cell_type_lt, histfunc='avg')
    fig.update_layout(
        title=title, barmode='group',
        xaxis={'title': xlabel},
        yaxis={'title': ylabel},
        width=width * 100,
        height=height * 100,
        showlegend=True
    )
    fig.show()


def plot_line_abundance(
        cluster_scale_df: DataFrame,
        cell_type_lt,
        width: float = 8,
        height: float = 5,
        xlabel: str = 'cycle',
        ylabel: str = 'cell abundance',
        title: str = 'Cell Abundance In Each Cycle',
):
    idx_lt = [i for i, j in cluster_scale_df['cycle'].value_counts().items() if
              j > 10]  # keep cycle contain at least 10 spots
    plt.figure(figsize=(width, height), dpi=80)
    for cell_type in cell_type_lt:
        sns.lineplot(data=cluster_scale_df[cluster_scale_df['cycle'].isin(idx_lt)], x='cycle', y=cell_type,
                     label=cell_type, estimator='mean', errorbar=None)
    sns.lineplot(data=cluster_scale_df[cluster_scale_df['cycle'].isin(idx_lt)], x='cycle', y='mean_abundance',
                 label='mean_abundance', estimator='mean', errorbar=None, color='black')
    plt.title(title, fontsize=22)
    # 设置 x 轴和 y 轴标题
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.6))
    # plt.legend()
    # plt.savefig('my_plot.png')
    plt.show()


def plot_cell_abundance(
        cluster_scale_df: DataFrame,
        cell_type,
        width: float = 8,
        height: float = 5,
        xlabel: str = 'cycle',
        ylabel: str = '',
        title: str = ''
):
    if not ylabel:
        ylabel = cell_type
    if not title:
        title = cell_type
    if cell_type not in cluster_scale_df.columns:
        raise KeyError(f'{cell_type} is not in cluster_scale_df')
    plt.figure(figsize=(width, height), dpi=80)
    category_counts = cluster_scale_df['cycle'].value_counts()
    df = cluster_scale_df[cluster_scale_df['cycle'].isin(category_counts[category_counts >= 10].index)]
    sns.boxplot(data=df, x='cycle', y=cell_type)
    plt.title(title, fontsize=22)
    # 设置 x 轴和 y 轴标题
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
