import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

plt.style.use('BJA_matplotlib_stylesheet.mplstyle')


ANNOT_CIRCLE_SIZE = 90
ANNOT_COLOR = '0.5'
ANNOT_FONTSIZE = 6
ANNOT_LW = 1
POINT_SIZES = {True:46,  False:22}
POINT_LW = 0.4
POINT_EC = '0.1'
POINT_ALPHA = 1.0
SPINE_LW = 1
SPINE_GRID_COLOR = '0.1'
TICK_FONTSIZE = 6
TICK_PAD = 1
LABEL_FONTSIZE = 7
FIG_LETTER_FONTSIZE = 9
FIG_LETTER_FONTWEIGHT = 'bold'
LEGEND_TEXT_FONTSIZE = 6
LEGEND_TITLE_FONTSIZE = 7
GRID_LW = 0.6
GRID_LIGHT_COLOR = '0.8'
HIGHLIGHT_BBOX_PAD = 1.5
HIGHLIGHT_FONTSIZE = 6
HIGHLIGHT_FONTWEIGHT = 'bold'
HIGHLIGHT_FACECOLOR = '0.9'
HIGHLIGHT_ANNOT_LW = 1.5


def set_stylesheet():
    plt.style.use('BJA_matplotlib_stylesheet.mplstyle')


def plot_parameter_heatmap(ax, df, fontsize=6, light_gray=0.1, dark_gray=0.25, fontcolor='black'):
    """
    Plots a grayscale-colored grid of values from a pandas dataframe.
    Useful for showing values of different parameters in that row. 
    
    """
    for x, col in enumerate(df.columns):
        unique_params = df[col].unique()
        num_unique = len(unique_params)
        grays = np.linspace(light_gray, dark_gray, num_unique)  
        colormap = {val: plt.cm.Greys(gray_val) for val, gray_val in zip(unique_params, grays)}

        for y, val in enumerate(df[col]):
            ax.fill_between([x, x+1], y-0.5, y+0.5, color=colormap[val])
            ax.text(x + 0.5, y, val, va='center', ha='center', 
                    fontsize=fontsize, color=fontcolor)

    ax.set_xticks(np.arange(len(df.columns)) + 0.5)
    ax.set_xticklabels(df.columns)
    ax.set_yticks(np.arange(len(df.index)) + 0.5)
    ax.set_yticklabels(df.index)
    ax.invert_yaxis()  # To align it like typical heatmaps
    ax.set_xlabel('Parameters')



def annotate_point(xy,  
                   text, 
                   xytext, 
                   ax,
                   relpos=(0.5, 0.5),
                   lw=ANNOT_LW,
                   color=ANNOT_COLOR,
                   fontsize=ANNOT_FONTSIZE,
                   fontweight='regular',
                   fontcolor='0.1',
                   ha='center',
                   zorder=6,
                   circle_size=ANNOT_CIRCLE_SIZE, 
                   bbox_pad=0,
                   bbox_facecolor='white',
                   highlight=False,
                   **kwargs
                  ):
    """
    Convenience function for streamlining annotation on slope vs. slope and volcano plots. 
    
    xy is the location of the point in Data units
    
    xytext values are a percentage of axes distance away from the xy point.
        They should be a percentage (e.g. 8) rather than a decimal (0.08) 
        Position of text is given in the difference in 'axes fraction' away from the point for easier eyeballing. 
    
    relpos is the relative position of the text bbox where the arrow points to
        relpos=(0.5, 0.5) points to the exact middle of the textbox
        relpos=(1, 1) points to the upper right of the textbox
    """
    frac_to_data = ax.transLimits.inverted().transform  # converts axes fraction to data coords
    # To calculate the xytext as a delta, find the difference in data coords from (0, 0)
    xtextdelta, ytextdelta = (frac_to_data(xytext) - frac_to_data([0, 0])) / 100
    xytext = (xy[0] + xtextdelta, xy[1] + ytextdelta)
    if highlight:
        bbox_pad = HIGHLIGHT_BBOX_PAD
        fontsize = HIGHLIGHT_FONTSIZE
        fontweight = HIGHLIGHT_FONTWEIGHT
        bbox_facecolor = HIGHLIGHT_FACECOLOR
        lw = HIGHLIGHT_ANNOT_LW
        zorder = zorder + 1
    ax.annotate(
        text=text, 
        xy=xy, 
        xytext=xytext, #(counter+5, row['coef']+0.05),
        textcoords='data',
        arrowprops=dict(arrowstyle='-', 
                        relpos=relpos, 
                        lw=lw, 
                        color=color),
        bbox=dict(pad=bbox_pad, 
                  facecolor=bbox_facecolor, 
                  edgecolor='none'),
        fontsize=fontsize, 
        fontweight=fontweight,
        color=fontcolor,
        annotation_clip=True, 
        ha=ha, va='center',
        zorder=zorder,
        **kwargs
    )
    # Draw circle around point
    alpha_corrected_color = (str(float(color) - 0.15))
    ax.scatter(xy[0], xy[1], 
               edgecolor=alpha_corrected_color, facecolor='white', linewidth=lw, alpha=0.7,
               s=circle_size, zorder=zorder)


def transform_mixed_coordinates(ax, swap=False):
    """
    Get a mixed transform for (transData and transAxes)
    
    if swap is True: transform is (transAxes, transData)
    """
    if not swap:
        return plt.matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes)
    else: 
        return plt.matplotlib.transforms.blended_transform_factory(ax.transAxes, ax.transData)



def custom_colorbar(ax, 
                    continuous_or_discrete='continuous',
                    vmin=None, vmax=None, vcenter=None,
                    bbox=[0.1, 0.6, 0.1, 0.3], 
                    orientation='vertical',
                    boundaries=[0, 69, 420],
                    cmap=None,
                    palette='viridis', n_colors=None, desat=None,
                    transform=None, 
                    edgewidth=0.5, 
                    label=None,
                    cbar_zorder=10,
                    extend='neither',
                    show_frame=False,
                    frame_edgewidth=None, frame_facecolor='white',
                    **cbar_kwargs,
                   ):
    """
    Reference: https://matplotlib.org/stable/tutorials/colors/colorbar_only.html
    Some other tricks:
    cbar.outline has set_linewidth() and other such things
    cbar takes .tick_params(), .set_xticks(), etc. 
    
    
    ax: parent axes
    continuous_or_discrete: 'continuous' or 'discrete' defines whether Normalize 
        or BoundaryNorm is used 
    
    vmin, vmax, vcenter: min, max and center values of colorbar, 
        USES TwoSlopeNorm() WHICH MAKES ASYMMETRIC COLOR SCALE OF COLORBAR.
    vcenter: optional 
    bbox: 4-tuple of [left, bottom, width, height]
    orientation: 'vertical' or 'horizontal'
    
    boundaries: the dividing points used for discrete colorbar
    
    cmap: Directly provide a cmap without going through sns.color_palette() 
    palette, n_colors, desat: sns.color_palette() arguments
    
    extend: Whether to draw arrows on colorbar indicating a cut-off for the values
        One of {'neither', 'both', 'min', 'max'}
    
    debug_rect: plot a gray background on the colorbar to show cax tight_bbox
    
    Returns (cbar, cax)
    
    """    
    if transform is None:
        transform = ax.transAxes
    
    cax = ax.inset_axes(bbox, transform=transform, zorder=cbar_zorder)
    cax.set(xticks=[], yticks=[])

    # First step is a ScalarMappable
    sm = plt.matplotlib.cm.ScalarMappable()

    # seaborn.color_palette() is used because it's convenient and easy
    if cmap is None: 
        cmap = sns.color_palette(palette=palette, n_colors=n_colors, desat=desat, 
                             as_cmap=True)
    else:
        if not isinstance(cmap, plt.matplotlib.colors.Colormap):
            try:
                cmap = plt.matplotlib.colors.ListedColormap(cmap)
            except:
                raise ValueError('cmap is weird, provide MPL cmap or a list of colors')
    
    # The  main Normalizations are Normalize, CenteredNorm, TwoSlopeNorm, BoundaryNorm
    #     It seems that TwoSlopeNorm can do what the other two can do with clever logic
    if continuous_or_discrete == 'discrete':
        norm = plt.matplotlib.colors.BoundaryNorm(boundaries=boundaries, ncolors=cmap.N)
    
    elif continuous_or_discrete == 'continuous':
        if vmin is None or vmax is None:
            raise ValueError('Specify vmin and vmax, or choose "discrete"')
        if vcenter is None:
            norm = plt.matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)  # vmin, vmax, clip

        elif vcenter is not None:
#             print('Using TwoSlopeNorm. Check for symmetry between vmin, vcenter and vmax.')
            norm = plt.matplotlib.colors.TwoSlopeNorm(vcenter=vcenter, vmin=vmin, vmax=vmax)
        else:
            raise ValueError('Could not discern colorbar normalization scheme')
    
    else:
        raise ValueError('Choose "continuous" or "discrete"')
    
    sm.set_array([])  # You need to set_array to an empty list for some reason
    sm.set_norm(norm)
    sm.set_cmap(cmap)
    
    cbar = ax.figure.colorbar(mappable=sm, cax=cax, ax=ax, orientation=orientation, 
                              label=label, extend=extend,
                              **cbar_kwargs)
    cbar.outline.set_linewidth(edgewidth)
    # Set tick width same as edgewidth for visual consistency
    cax.tick_params(width=edgewidth)  
    
    if show_frame:
        raise NotImplementedError('Getting cax tight bounding box is complicated by whether ticks, title and labels are drawn yet')
    
    # if show_frame:
        # cax_bbox = ax.transAxes.inverted().transform(cax.get_tightbbox(ax.get_figure().canvas.get_renderer()))
    # Convert raw 2x2 array into BBox object:
    # cax_bbox = plt.matplotlib.transforms.Bbox(cax_bbox)
    # if frame_edgewidth is None:
        # frame_edgewidth = edgewidth
    # patch = plt.Rectangle(xy=(cax_bbox.x0, cax_bbox.y0), width=cax_bbox.x1-cax_bbox.x0, height=cax_bbox.y1-cax_bbox.y0, 
    #                         transform=ax.transAxes, fc=frame_facecolor, ec='0.2', lw=frame_edgewidth)
    # ax.add_artist(patch)
    
    
    return cbar, cax


def custom_legend(entries, 
                  ax,
                  palette,
                  handles=None,
                  labels=None,
                  loc=(1.02, 0), show_frame=False, sort=False, 
                  handlelength=1.1, handletextpad=0.3,
                  title_fontsize=LEGEND_TITLE_FONTSIZE, title_fontweight='bold',
                  frame_color='1', frame_edgecolor='0.25', frame_edgewidth=0.8,
                  mew=POINT_LW, mec=POINT_EC, ms=8, marker='o', 
                  ncol=1, columnspacing=0.8,
                  **kwargs):
    """
    Wrapper for making a legend based on list of entries, using colors defined in provided color palette.
    
    marker can be a string with one marker, or a list of marker strings
    
    sort: sorts entries ascending
    
    borderpad : fractional whitespace inside the legend border, in font-size units.

    labelspacing : vertical space between the legend entries, in font-size units.

    handlelength : length of the legend handles, in font-size units.

    handleheight : height of the legend handles, in font-size units.

    handletextpad : pad between the legend handle and text, in font-size units.

    borderaxespad : pad between the axes and legend border, in font-size units.

    columnspacing : spacing between columns, in font-size units.
    
    **kwargs go into ax.legend()
    
    """
    if labels is not None:
        entries = {entry: label for entry, label in zip(entries, labels)}
        
    if sort and labels is not None: 
        entries = dict(sorted(entries.items()))
    elif sort and labels is None:
        entries = sorted(entries)
    
    if isinstance(entries, dict):
        labels = entries.values()
    
    if isinstance(marker, str):
        marker = [marker] * len(entries)
     
    if handles is None:
        handles = []
        for entry, m in zip(entries, marker):
            color = palette[entry]
            handles.append(
                plt.matplotlib.lines.Line2D(
                    [0], [0], label=entry,
                    linewidth=0, mfc=color, mew=mew, mec=mec, ms=ms, marker=m,
                )
            )
        
    if show_frame:
        frame_params = dict(
            frameon=True, framealpha=1, facecolor=frame_color, 
            fancybox=False, edgecolor=frame_edgecolor)
    else:
        frame_params = dict()
        
    legend = ax.legend(
        handles=handles, 
        labels=labels,
        loc=loc, 
        handlelength=handlelength, handletextpad=handletextpad,
        title_fontproperties=dict(size=title_fontsize, weight=title_fontweight), 
        ncol=ncol, columnspacing=columnspacing,
        **frame_params,
        **kwargs
        )
    legend._legend_box.align = 'left'  # shift legend title to left alignment
    if show_frame: 
        frame = legend.get_frame()
        frame.set_linewidth(frame_edgewidth)
    return legend
    

def adjust_violin_quartiles(ax, lw=1, linestyle='-', diff_median=True, median_lw=2, median_linestyle='-', 
                            solid_capstyle='butt', dash_capstyle='round', **kwargs):
    """
    In call to sns.violinplot(), set inner='quartile' for this to work!
    Seaborn offers no control over the 'inner' parameter that draws quartiles, so fix that. 
    Indiscriminantly looks for Line2D instances, so use early in plotting for that axes.
    
    Also nice to set linewidth=0 in sns.violinplot, which cleans up outlines nicely
    
    linestyle can also be a tuple of even length, 
    e.g. (0, (5, 1, 2, 1))
    This means: Start at 0, then do  (5 points on, 1 point off, 2 points on, 1 point off), repeat
    
    capstyles are one of {'butt', 'projecting', 'round'}
    """
    
    lines = [child for child in ax.get_children() if isinstance(child, plt.matplotlib.lines.Line2D)]
    
    if diff_median:
        for start in range(0, len(lines), 3):
            q1, median, q3 = lines[start:start+3]
            q1.set(linestyle=linestyle, lw=lw, solid_capstyle=solid_capstyle, dash_capstyle=dash_capstyle, **kwargs)
            median.set(linestyle=median_linestyle, lw=median_lw, solid_capstyle=solid_capstyle, dash_capstyle=dash_capstyle, **kwargs)
            q3.set(linestyle=linestyle, lw=lw, solid_capstyle=solid_capstyle, dash_capstyle=dash_capstyle, **kwargs)  
    else:
        for line in lines:
            line.set(linestyle=linestyle, lw=lw, solid_capstyle=solid_capstyle, dash_capstyle=dash_capstyle, **kwargs)


def adjust_color(color, amount=0.5):
    """
    From : https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


def shrink_cbar(ax, shrink=0.9):
    """
    Shrink the height of a colorbar that is set within its own pre-made colorbar axes (cax) 
    From https://stackoverflow.com/questions/53429258/matplotlib-change-colorbar-height-within-own-axes    
    """
    b = ax.get_position()
    new_h = b.height*shrink
    pad = (b.height-new_h)/2.
    new_y0 = b.y0 + pad
    new_y1 = b.y1 - pad
    b.y0 = new_y0
    b.y1 = new_y1
    ax.set_position(b)



def create_panel_letter_label(ax, letter, fontsize=None, fontweight='bold', transform=None, **kwargs):
    """
    Places a letter on the axes at the top left corner of the axes.

    Used for adding the figure panel label to the axes, like A, B, C, etc.
    """
    if fontsize is None:
        fontsize = LABEL_FONTSIZE
    
        
    fig = ax.get_figure()
    
    if transform is None:
        transform = fig.transFigure
    
    bbox = tight_bbox(ax)
    ax.text(
        x=(bbox.x0), 
        y=(bbox.y1), 
        s=letter, 
        fontsize=fontsize,
        fontweight=fontweight,
        transform=transform, 
        **kwargs)


def tight_bbox(ax):
    """
    Example for placing figure panel letters at very top left of the axis bounding box: 
    for ax, letter in zip([ax1, ax2], ['A', 'B']):
        bb = tight_bbox(ax)
        ax.text(x=bb.x0, y=bb.y1, s=letter, 
        fontsize=src.plots.LABEL_FONTSIZE, fontweight='bold', transform=fig.transFigure, )
    """
    fig = ax.get_figure()
    tight_bbox_raw = ax.get_tightbbox(fig.canvas.get_renderer())
    from matplotlib.transforms import TransformedBbox
    tight_bbox_fig = TransformedBbox(tight_bbox_raw, fig.transFigure.inverted())
    return tight_bbox_fig


def make_ci(x, y, std=2, **kwargs):
    """
    Draw confidence intervals around data
    From https://stackoverflow.com/a/25022642
    """
    cov = np.cov(x, y)
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals = vals[order]
    vecs = vecs[:, order]
    theta = np.degrees((np.arctan2)(*vecs[:, 0][::-1]))
    w, h = 2 * std * np.sqrt(vals)
    ellipse = (plt.matplotlib.patches.Ellipse)(xy=(
 np.mean(x), np.mean(y)),
     width=w,
     height=h,
     angle=theta, **kwargs)
    return ellipse


def change_width(ax, new_value):
    """
    Offsetting boxplot and swarmplot side-by-side is super annoying.
    code from:
    # https://stackoverflow.com/questions/61647192/boxplot-and-data-points-side-by-side-in-one-plot

    """
    for patch in ax.patches:
        current_width = patch.get_width()
        diff = current_width - new_value
        patch.set_width(new_value)
        patch.set_x(patch.get_x() + diff * 0.5)
        
        
        
def get_3way_subsets(df, cols):
    """
    Calculate the subset sizes for a Venn diagram.
    Used for the matplotlib_venn package venn3 method.
    Args:
    df: pandas DataFrame with boolean columns
    cols: list of boolean column names to use
    Returns:
    A list with seven subset sizes.
    Ordering is: [Abc, aBc, ABc, abC, AbC, aBC, ABC]
    """
    
    assert len(cols) == 3, "Number of columns must be 3."
    
    Abc = df[ df[cols[0]] & ~df[cols[1]] & ~df[cols[2]]].shape[0]
    aBc = df[~df[cols[0]] &  df[cols[1]] & ~df[cols[2]]].shape[0]
    ABc = df[ df[cols[0]] &  df[cols[1]] & ~df[cols[2]]].shape[0]
    abC = df[~df[cols[0]] & ~df[cols[1]] &  df[cols[2]]].shape[0]
    AbC = df[ df[cols[0]] & ~df[cols[1]] &  df[cols[2]]].shape[0]
    aBC = df[~df[cols[0]] &  df[cols[1]] &  df[cols[2]]].shape[0]
    ABC = df[ df[cols[0]] &  df[cols[1]] &  df[cols[2]]].shape[0]
    
    return [Abc, aBc, ABc, abC, AbC, aBC, ABC]