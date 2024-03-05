import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from .utils import jitter
from matplotlib.patches import Rectangle
from matplotlib.patches import Patch
import pandas as pd


def plot(data, parameter, trellis, UL=None, LL=None, filters=None, color=None, plot='violin', cmap="viridis", norm=None, yscale="linear", ylim=None, ylabel=None, width=9, height=5, fontsize=6, markersize=1, linewidth=1):
    """Plots trellis of a given parameter on split conditions.
    
    Parameters
    ----------
    data : pd.DataFrame
        Summarized dataframe from which to plot parameters from.
    parameter : str
        Variable (y-axis) name. Datatype should be numeric.
    trellis : list of str
        Names of column names to trellis by. Ordered from top to bottom.
    UL : float, optional
        Upper limit line.
    LL : float, optional
        Lower limit line.
    filters : dict, optional
        Dictionary of column name keys and list of values to narrow down the data by.
    color : str, optional
        Name of column to color by. Datatype can be both numeric and categorical. If numeric, will be colored according to cmap.
    plot : str, default = 'violin'
        Type of plot for each trellis element. Can be 'violin' or 'box'. If 'violin', both 'box' and 'violin' are plotted.
    cmap : str, default = 'viridis'
        Colormap to use for data points. Refer to matplotlib colormaps for accepted values.
    norm : plt.Normalize, optional
        Color normalization. If not specified, defaults to minimum and maximum value of data.
    yscale : str, default = 'linear'
        y-scale of plot. Either 'linear' or 'log'.
    ylim : list of float, optional
        y-limits. If not specified, defaults to automatic.
    ylabel : str, optional
        y-label. If not specififed, defaults to column name specififed by `parameter`.
    width : float, optional
        width of the plot in inches
    height : float, optional
        height of the plot in inches
    fontsize : float, optional
    markersize : float, optional
    linewidth : float, optional

    Returns
    -------
    fig, ax of plot

    """
    
    
    #  Initialize figure to plot in
    fig, ax = plt.subplots(figsize=(width,height))
    fs = fontsize
    ms = markersize
    lw = linewidth

    if filters is None:
        filters = {}
    #  First filter dataframe to only contain the items in the filter.
    for key, val in filters.items():
        if type(val) == list:
            data = data.loc[data[key].isin(val)]
        else:
            data = data.loc[data[key]==val]

    #  Initialize empty lists to go through all the trellis options.
    count = 0
    #  These are used for single parameter plotting
    x = np.array([])
    y = np.array([])
    z = np.array([])
    mean = []
    median = []
    std = []
    n_sample = []
    #  These are used for both single parameter and plot plotting
    label = []

    #  If the color by column is discrete, i.e. different words, colormaps are dictionaries corresponding to unique value in color column to color pair
    if color is not None:
        if data[color].dtype =="O":
            flag = "discrete"
            cmap = dict(zip(data[color].unique(),sns.color_palette("Set2",10)))
            if type(parameter) != str:  # if plotting parameter curves, change to a function like a cmap object
                colormap = lambda key: cmap[key]
        else:
            flag = "numeric"
            if norm is None:
                norm = plt.Normalize(data[color].min(), data[color].max())
            colormap = plt.cm.get_cmap(cmap)
    
    #  Generate list of all existing trellis combinations
    all_combinations = data.groupby(trellis).count().index.to_list()

    if type(trellis)==str or len(trellis)==1:  # to handle clases where only trellising by a single column, so a simple list is created instead a list of tuples
        all_combinations = [tuple([combo]) for combo in all_combinations]
    
    #  For plot plotting, need to create inset subfigures. These parameters help with spacing the insets out
    numplots = len(all_combinations)
    padding = 0.1
    plotwidth = 1/(padding*(numplots+1)+numplots)
    paddingwidth = padding*plotwidth

    ############################### plotting single parameter ##############################################
    for combination in all_combinations:
        data_slice = data
        for j in range(len(trellis)):
            data_slice = data_slice.loc[data_slice[trellis[j]]==combination[j]]
        label.append(combination)
        x = np.append(x, np.repeat([count], data_slice[parameter].shape[0]))
        y = np.append(y, data_slice[parameter])
        # get rid of nan values before applying jitter
        nan_idx = np.isnan(y)
        x = x[~nan_idx] # get rid of nans
        y = y[~nan_idx] # get rid of nans
        if color is not None:
            z = np.append(z, data_slice[color])
            z = z[~nan_idx]
        mean.append(data_slice[parameter].mean())
        median.append(data_slice[parameter].median())
        std.append(data_slice[parameter].std())
        n_sample.append(data_slice[parameter].count())
        count += 1
        
    if plot =='violin':      
        sns.boxplot(x=x, y=y, ax=ax, color='0.99', linewidth=0.5, zorder=200, notch=True)
        sns.violinplot(x=x, y=y, ax=ax, color='0.95', inner=None, zorder=198)
    elif plot =='box':
        sns.boxplot(x=x, y=y, ax=ax, color='0.95', zorder=200, notch=True)
    
    if color is None:
        # sns.stripplot(x=x, y=y, size=10,ax=ax)
        ax.scatter(x=jitter(x,y), y=y, s=6*ms, zorder=202)
    else:
        # sns.stripplot(x=x, y=y, hue=z, palette='viridis', size=6, ax=ax)
        if data[color].dtype == "O":  # if color by column is categorical
            cmap=dict(zip(data[color].unique(),sns.color_palette("Set2",10)))
            z = pd.DataFrame({color:z})
            ax.scatter(x=jitter(x,y), y=y, c=z[color].map(cmap), s=6*ms, zorder=202)

            # add a legend. First, configure the handles and labels
            patches = []
            for key, val in cmap.items():
                patches.append(Patch(color=val, label=key))
            ax.legend(bbox_to_anchor=(1.0, 0.5), loc="center left", handles=patches, fontsize=fs+4)

        else:  # if color by column is numerical, add colorbar
            if norm is None:
                norm = plt.Normalize(min(z), max(z))
            ax.scatter(x=jitter(x,y), y=y, c=z, s=6*ms, cmap=cmap, norm=norm, zorder=202)
            #  If color is numeric, generate a color bar
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            # add a colorbar
            cbar = fig.colorbar(sm, label=color, ax=ax)
            cbar.ax.tick_params(labelsize=fs+4)
            #ax.figure.colorbar(sm, label=color)
            ax.figure.axes[-1].yaxis.label.set_size(fs+4)
    # set yscale
    ax.set_yscale(yscale)
        
    ############################################### Setting up labeling system ##########################################################    
            

    #  Prep for setting up labelling system. First store current y limits (will change to create margin for labeling and statistics) and set x limits
    if ylim is not None:  # if ylim is explicitly set, set it.
        ax.set_ylim(ylim)

    # make sure x limits only contain the data
    xlims=[-0.5, count-0.5]
    ax.set_xlim(xlims)             

    #  Set up y coordinates for texts and color rectangle positions
    box_height = 0.003*fs # height of the box
    ypositions = np.linspace(1, 1+ box_height*(2*len(trellis)), 2*len(trellis)+1)
    top_max = ypositions[-1] # used to adjust margin at the end
    rec_ypos_bottom = ypositions[-3::-2]  # 0th, 2nd, 4th, ... item is the location of the box. Negative to flip
    ypositions = ypositions[-2::-2]
    # rec_ypos = np.linspace(ylims[1]+(len(trellis)-1)*labelmargin/len(trellis), ylims[1], len(trellis))  # position for rectangles

    color_list = ['#F4CDF3', '#CDE2F4', '#CDF4E2','#F4CDCD','#F5C185', '#A0EBF9', '#DFDFDF']  # list of colors for the label rectangles

    #  Now, go through each trellis and add text and labels
    for i in range(len(trellis)):
        j = 0
        
        while j < len(label):
            count = 1
            for k in range(j,len(label)-1):
                if label[k+1][i] == label[k][i]:  # check if next neighbor is part of the same label
                    count += 1
                else:
                    break
            xpos = (j+0.5*count)/len(label)  # center of the text position. should be in axes coordinates (0 to 1 essentially)
            rec_xpos_left = j/len(label)
            ax.text(xpos, ypositions[i], label[j][i], fontsize=fs, horizontalalignment='center', verticalalignment='center', fontweight='heavy', zorder=100, transform=ax.transAxes)
            # shaded box
            ax.add_patch(Rectangle(xy=(rec_xpos_left, rec_ypos_bottom[i]), width=count/len(label), height=2*box_height, facecolor=color_list[i % len(color_list)], alpha=1, linewidth=12, zorder=99, transform=ax.transAxes, clip_on=False))
            # border box
            ax.add_patch(Rectangle(xy=(rec_xpos_left, rec_ypos_bottom[i]), width=count/len(label), height=2*box_height, fill=False, edgecolor='white', linewidth=lw, zorder=101, transform=ax.transAxes, clip_on=False))
            j += count # to skip over future entries
        ax.text(0, ypositions[i], trellis[i]+' ', fontsize=fs+2, horizontalalignment='right', verticalalignment='center', fontweight='heavy', transform=ax.transAxes)

            
    if type(parameter) == str:
        #  Regenerate y positions for statistics reporting region
        ypositions = np.linspace(0, -box_height*8, 8+1)
        bot_max = ypositions[-1] # used to adjust margin at the end
        rec_ypos_bottom = ypositions[2::2]  # 0th, 2nd, 4th, ... item is the location of the box. Negative to flip
        ypositions = ypositions[1::2]


        #  Generate statistics table.
        for i in range(len(mean)):
            rec_xpos = i/len(mean)
            if abs(mean[i]) > 0.1:
                formatted_mean = f'{mean[i]:0.3f}'
                formatted_std = f'{std[i]:0.3f}'
                formatted_median = f'{median[i]:0.3f}'
                formatted_count = f'{n_sample[i]}'
            else:
                formatted_mean = f'{mean[i]:0.3e}'
                formatted_std = f'{std[i]:0.3e}'
                formatted_median = f'{median[i]:0.3e}'
                formatted_count = f'{n_sample[i]}'
            ax.text((i+0.5)/len(mean), ypositions[0], formatted_mean, fontsize=fs, horizontalalignment='center', verticalalignment='center', fontweight='heavy', transform=ax.transAxes)
            ax.add_patch(Rectangle(xy=(rec_xpos, rec_ypos_bottom[0]), width=1/len(mean), height=2*box_height, fill=False, edgecolor='black', linewidth=1, transform=ax.transAxes, clip_on=False))
            ax.text((i+0.5)/len(mean), ypositions[1], formatted_std, fontsize=fs, horizontalalignment='center', verticalalignment='center', fontweight='heavy', transform=ax.transAxes)
            ax.add_patch(Rectangle(xy=(rec_xpos, rec_ypos_bottom[1]), width=1/len(mean), height=2*box_height, fill=False, edgecolor='black', linewidth=1, transform=ax.transAxes, clip_on=False))
            ax.text((i+0.5)/len(mean), ypositions[2], formatted_median, fontsize=fs, horizontalalignment='center', verticalalignment='center', fontweight='heavy', transform=ax.transAxes)
            ax.add_patch(Rectangle(xy=(rec_xpos, rec_ypos_bottom[2]), width=1/len(mean), height=2*box_height, fill=False, edgecolor='black', linewidth=1, transform=ax.transAxes, clip_on=False))
            ax.text((i+0.5)/len(mean), ypositions[3], formatted_count, fontsize=fs, horizontalalignment='center', verticalalignment='center', fontweight='heavy', transform=ax.transAxes)
            ax.add_patch(Rectangle(xy=(rec_xpos, rec_ypos_bottom[3]), width=1/len(mean), height=2*box_height, fill=False, edgecolor='black', linewidth=1, transform=ax.transAxes, clip_on=False))
        ax.text(0, ypositions[0], 'Mean ', fontsize=fs+2, horizontalalignment='right', verticalalignment='center', fontweight='heavy', transform=ax.transAxes)
        ax.text(0, ypositions[1], 'Std ', fontsize=fs+2, horizontalalignment='right', verticalalignment='center', fontweight='heavy', transform=ax.transAxes)
        ax.text(0, ypositions[2], 'Median ', fontsize=fs+2, horizontalalignment='right', verticalalignment='center', fontweight='heavy', transform=ax.transAxes)
        ax.text(0, ypositions[3], 'Count ', fontsize=fs+2, horizontalalignment='right', verticalalignment='center', fontweight='heavy', transform=ax.transAxes)
        ax.grid("y","both",color="0.95", zorder=0.1)
        
    #if upper and lower limits specified, draw it.
    if UL is not None:
        ax.plot([xlims[0], xlims[1]], [UL, UL], ':', c="0.7")
    if LL is not None:
        ax.plot([xlims[0], xlims[1]], [LL, LL], ':', c="0.7")
    
    
    ax.set_ylabel(ylabel=parameter, fontweight='heavy', fontsize=fs+4)
    # if ylabel specified, change it
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontweight='heavy', fontsize=fs+4)

    ax.set_xticks([])
    fig.subplots_adjust(top=(1-bot_max)/(top_max-bot_max), bottom=(-bot_max)/(top_max-bot_max))

    return fig, ax