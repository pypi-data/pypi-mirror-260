import logging

import matplotlib.patches as mpatches
import matplotlib.transforms as trn
import numpy as np
from matplotlib.path import Path as mPath

_logger = logging.getLogger(__name__)

RATIO_OPTIONS = {"golden_ratio", "equal", "from_rows"}


def add_values_to_bars(
    axis,
    type="bar",
    position="c",
    format="{:.0f}",
    x_offset=0,
    y_offset=0,
    color="k",
    horizontalalignment="center",
    verticalalignment="center",
):
    """
    Add the values of the bars as number in the center

    Parameters
    ----------
    axis : `mpl.pyplot.axes.Axes` object
        Axis containing the bar plot
    position: {"c", "t", "l", "r", "b"}, optional
        Location of the numbers, where "c" is center, "t" is top, "l" is left, "r" is right and "b"
        is bottom. Default = "c"
    type: {"bar", "barh"}
        Direction of the bars. Default = "bar", meaning vertical bars. Alternatively you need to
        specify "barh" for horizontal bars.
    format: str, optional
        Formatter to use for the numbers. Default = "{:.0f}" (remove digits from float)
    x_offset: float, optional
        x offset in pt. Default = 0
    y_offset: float, optional
        y offset in pt. Default = 0
    color: "str", optional
        Color of the characters, Default is black
    horizontalalignment: str, optional
        Horizontal alignment of the numbers. Default = "center"
    verticalalignment: str, optional
        Vertical alignment of the numbers Default = "center"
    ):
    """

    # voeg percentage to aan bars
    for patch in axis.patches:
        b = patch.get_bbox()
        cx = (b.x1 + b.x0) / 2
        cy = (b.y1 + b.y0) / 2
        hh = b.y1 - b.y0
        ww = b.x1 - b.x0
        if position == "c":
            (px, py) = (cx, cy)
        elif position == "t":
            (px, py) = (cx, cy + hh / 2)
        elif position == "b":
            (px, py) = (cx, cy - hh / 2)
        elif position == "l":
            (px, py) = (cx - ww / 2, cy)
        elif position == "r":
            (px, py) = (cx + ww / 2, cy)
        else:
            raise ValueError(f"position = {position} not recognised. Please check")

        # add offsets
        (px, py) = (px + x_offset, py + y_offset)

        if type == "bar":
            value = hh
        elif type == "barh":
            value = ww
        else:
            raise ValueError(f"type = {type} not recognised. Please check")

        # make the value string using the format specifier
        value_string = format.format(value)

        axis.annotate(
            value_string,
            (px, py),
            color=color,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
        )


def add_cbs_logo_to_plot(
    fig,
    axes=None,
    margin_x_in_mm=6.0,
    margin_y_in_mm=6.0,
    x0=0,
    y0=0,
    width=None,
    height=None,
    zorder_start=1,
    fillcolor="cbs:highchartslichtgrijs",
    edgecolor="cbs:logogrijs",
):
    # maak een box met de coordinaten van de linker onderhoek van het grijze vierkant in axis
    # fractie coordinaten
    if width is None:
        ww = 1
    else:
        ww = width
    if height is None:
        hh = 1
    else:
        hh = height

    if axes is not None:
        tb = trn.Bbox.from_bounds(x0, y0, ww, hh).transformed(axes.transAxes)

        # bereken de linker onderhoek van het figure in Figure coordinaten (pt van linker onderhoek)
        x0 = tb.x0 + (margin_x_in_mm / 25.4) * fig.dpi
        y0 = tb.y0 + (margin_y_in_mm / 25.4) * fig.dpi
    else:
        x0 = (margin_x_in_mm / 25.4) * fig.dpi
        y0 = (margin_y_in_mm / 25.4) * fig.dpi

    all_points = get_cbs_logo_points()

    if axes is not None:
        trans = axes.transAxes
    else:
        trans = fig.transFigure

    zorder = zorder_start
    for points_in_out in all_points:

        for ii, points in enumerate(points_in_out):
            points[:, :2] *= fig.dpi / 25.4
            points[:, 0] += x0
            points[:, 1] += y0
            pl = points[:, :2]
            dr = points[:, 2]
            tr_path = mPath(pl, dr).transformed(trans.inverted())
            if ii == 0:
                color = edgecolor
            else:
                color = fillcolor
            poly = mpatches.PathPatch(
                tr_path, fc=color, linewidth=0, zorder=zorder, transform=trans
            )
            poly.set_clip_on(False)
            if axes is not None:
                axes.add_patch(poly)
            else:
                fig.patches.append(poly)
            zorder += 1


def get_cbs_logo_points(logo_width_in_mm=3.234, logo_height_in_mm=4.995, rrcor=0.171):
    """
    Maak een array met de letters van het CBS logog

    Parameters
    ----------
    logo_width_in_mm: float
        Breeedte van het logo
    logo_height_in_mm: float
        Hoogte van het logo
    rrcor: float
        Radius of corners

    Returns
    -------
    list
        List met 3 Nx2 arrays

    """

    ww = logo_width_in_mm

    # punten C, beginnen links onder, tegen klok in, binnen en buiten kant
    points_c = [
        np.array(
            list(
                [
                    [0.000, 2.663, mPath.MOVETO],
                    [1.430, 2.663, mPath.LINETO],
                    [1.430, 3.308, mPath.LINETO],
                    [0.644, 3.308, mPath.LINETO],
                    [0.644, 3.577, mPath.LINETO],
                    [1.430, 3.577, mPath.LINETO],
                    [1.430, 4.221, mPath.LINETO],
                    [rrcor, 4.221, mPath.LINETO],
                    [0.000, 4.221, mPath.CURVE3],
                    [0.000, 4.221 - rrcor, mPath.CURVE3],
                    [0.000, 2.663, mPath.CLOSEPOLY],
                ]
            )
        ),
        np.array(
            list(
                [
                    [0.188, 2.851, mPath.MOVETO],
                    [1.242, 2.851, mPath.LINETO],
                    [1.242, 3.120, mPath.LINETO],
                    [1.242, 3.120, mPath.LINETO],
                    [0.457, 3.120, mPath.LINETO],
                    [0.457, 3.765, mPath.LINETO],
                    [1.242, 3.765, mPath.LINETO],
                    [1.242, 4.033, mPath.LINETO],
                    [0.188, 4.033, mPath.LINETO],
                    [0.188, 2.851, mPath.CLOSEPOLY],
                ]
            )
        ),
    ]

    points_b1 = [
        np.array(
            list(
                [
                    [1.674, 2.663, mPath.MOVETO],
                    [3.234, 2.663, mPath.LINETO],
                    [3.234, 4.221 - rrcor, mPath.LINETO],
                    [3.234, 4.221, mPath.CURVE3],
                    [3.063, 4.221, mPath.CURVE3],
                    [2.318, 4.221, mPath.LINETO],
                    [2.318, 4.996 - rrcor, mPath.LINETO],
                    [2.318, 4.996, mPath.CURVE3],
                    [2.147, 4.996, mPath.CURVE3],
                    [1.674, 4.996, mPath.LINETO],
                    [1.674, 2.663, mPath.CLOSEPOLY],
                ]
            )
        ),
        np.array(
            list(
                [
                    [1.862, 2.851, mPath.MOVETO],
                    [3.046, 2.851, mPath.LINETO],
                    [3.046, 4.034, mPath.LINETO],
                    [2.130, 4.034, mPath.LINETO],
                    [2.130, 4.808, mPath.LINETO],
                    [1.862, 4.808, mPath.LINETO],
                    [1.862, 2.851, mPath.CLOSEPOLY],
                ]
            )
        ),
    ]

    # in binnen stuk van de b
    points_b2 = [
        np.array(
            list(
                [
                    [2.129, 3.121, mPath.MOVETO],
                    [2.775, 3.121, mPath.LINETO],
                    [2.775, 3.766, mPath.LINETO],
                    [2.129, 3.766, mPath.LINETO],
                    [2.129, 3.121, mPath.CLOSEPOLY],
                ]
            )
        ),
        np.array(
            list(
                [
                    [2.317, 3.309, mPath.MOVETO],
                    [2.588, 3.309, mPath.LINETO],
                    [2.588, 3.578, mPath.LINETO],
                    [2.317, 3.578, mPath.LINETO],
                    [2.317, 3.309, mPath.CLOSEPOLY],
                ]
            )
        ),
    ]

    # de punten van de S, beginnende linksboven, tegen de klok in. Eerst array is de
    # buitenkant, tweede array is de binnenkant
    points_s = [
        np.array(
            list(
                [
                    [0.000, 2.420, mPath.MOVETO],
                    [0.000, 0.888, mPath.LINETO],
                    [2.589, 0.888, mPath.LINETO],
                    [2.589, 0.645, mPath.LINETO],
                    [0.000, 0.645, mPath.LINETO],
                    [0.000, rrcor, mPath.LINETO],
                    [0.000, 0.000, mPath.CURVE3],
                    [rrcor, 0, mPath.CURVE3],
                    [ww - rrcor, 0, mPath.LINETO],
                    [ww, 0, mPath.CURVE3],
                    [ww, rrcor, mPath.CURVE3],
                    [ww, 1.533, mPath.LINETO],
                    [0.646, 1.533, mPath.LINETO],
                    [0.646, 1.772, mPath.LINETO],
                    [3.234, 1.772, mPath.LINETO],
                    [3.234, 2.420, mPath.LINETO],
                    [0.000, 2.420, mPath.CLOSEPOLY],
                ]
            )
        ),
        np.array(
            list(
                [
                    [0.188, 2.232, mPath.MOVETO],
                    [0.188, 1.076, mPath.LINETO],
                    [2.777, 1.076, mPath.LINETO],
                    [2.777, 0.457, mPath.LINETO],
                    [0.188, 0.457, mPath.LINETO],
                    [0.188, 0.188, mPath.LINETO],
                    [3.045, 0.188, mPath.LINETO],
                    [3.045, 1.345, mPath.LINETO],
                    [0.458, 1.345, mPath.LINETO],
                    [0.458, 1.960, mPath.LINETO],
                    [3.045, 1.960, mPath.LINETO],
                    [3.045, 2.232, mPath.LINETO],
                    [0.188, 2.232, mPath.CLOSEPOLY],
                ]
            )
        ),
    ]

    return [points_c, points_b1, points_b2, points_s]


def add_axis_label_background(
    fig,
    axes,
    alpha=1,
    margin=0.05,
    x0=None,
    y0=None,
    loc="east",
    radius_corner_in_mm=1,
    logo_margin_x_in_mm=1,
    logo_margin_y_in_mm=1,
    add_logo=True,
    aspect=None,
    backgroundcolor="cbs:highchartslichtgrijs",
    logo_fillcolor="cbs:highchartslichtgrijs",
    logo_edgecolor="cbs:logogrijs",
):
    """
    Add a background to the axis label

    Parameters
    ----------
    fig : `mpl.figure.Figure` object
        The total canvas of the Figure
    axes : `mpl.axes.Axes` object
        The axes of the plot to add a box
    alpha: float, optional
        Transparency of the box. Default = 1 (not transparent)
    margin: float, optional
        The margin between the labels and the side of the gray box
    loc: {"east", "south"}
        Location of the background. Default = "east" (left to y-axis. Only "east" and "south" are
        implemented
    add_logo: bool, optional
        If true, add the cbs logo. Default = True
    radius_corner_in_mm: float, optional
        Radius of the corner in mm. Default = 2
    logo_margin_x_in_mm: float
        Distance from bottom of logo in mm. Default = 2
    logo_margin_y_in_mm=2,
        Distance from left of logo in mm. Default = 2
    backgroundcolor: str, optional
        Color of the grey square. Default is "cbs:lichtgrijs"
    logo_edgecolor: str, optional
        Color of the logo edge. Default "cbs:logogrijs"
    """

    # the bounding box with respect to the axis in Figure coordinates
    # (0 is bottom left canvas, 1 is top right)
    bbox_axis_fig = axes.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

    # the bounding box with respect to the axis coordinates
    # (0 is bottom left axis, 1 is top right axis)
    bbox_axi = axes.get_tightbbox(fig.canvas.get_renderer()).transformed(
        axes.transAxes.inverted()
    )

    if loc == "east":
        if x0 is None:
            x0 = bbox_axi.x0 - margin * bbox_axi.width
        x1 = 0

        y0 = 0
        y1 = 1

    elif loc == "south":
        x0 = 0
        x1 = 1

        if y0 is None:
            y0 = bbox_axi.y0 - margin * bbox_axi.height
        y1 = 0
    else:
        raise ValueError(
            f"Location loc = {loc} is not recognised. Only east and south implemented"
        )

    # width and height of the grey box area
    width = x1 - x0
    height = y1 - y0

    _logger.debug(f"Adding rectangle with width {width} and height {height}")

    # eerste vierkant zorgt voor rechte hoeken aan de rechter kant
    if loc == "east":
        rec_p = (x0 + width / 2, y0)
        rec_w = width / 2
        rec_h = height
    elif loc == "south":
        rec_p = (x0, y0 + height / 2)
        rec_w = width
        rec_h = height / 2
    else:
        raise AssertionError(f"This should not happen")

    p1 = mpatches.Rectangle(
        rec_p,
        width=rec_w,
        height=rec_h,
        alpha=alpha,
        facecolor=backgroundcolor,
        edgecolor=backgroundcolor,
        zorder=0,
    )
    p1.set_transform(axes.transAxes)
    p1.set_clip_on(False)

    # tweede vierkant zorgt voor ronde hoeken aan de linker kant
    radius_in_inch = radius_corner_in_mm / 25.4
    xshift = radius_in_inch / bbox_axis_fig.width
    yshift = radius_in_inch / bbox_axis_fig.height
    pad = radius_in_inch / bbox_axis_fig.width
    # we moeten corrigeren voor de ronding van de hoeken als we een aspect ratio hebben
    if aspect is None:
        aspect = bbox_axis_fig.height / bbox_axis_fig.width
    _logger.debug(f"Using aspect ratio {aspect}")
    p2 = mpatches.FancyBboxPatch(
        (x0 + xshift, y0 + yshift),
        width=width - 2 * xshift,
        height=height - 2 * yshift,
        mutation_aspect=1 / aspect,
        alpha=alpha,
        facecolor=backgroundcolor,
        edgecolor=backgroundcolor,
        transform=fig.transFigure,
        zorder=0,
    )
    p2.set_boxstyle("round", pad=pad)
    p2.set_transform(axes.transAxes)
    p2.set_clip_on(False)

    # add_artist wordt niet door mpld3 herkend. add_patch wel. Wel chechekn of het ong wel goed gaat
    # axes.add_artist(p1)
    # axes.add_artist(p2)
    axes.add_patch(p1)
    axes.add_patch(p2)

    if add_logo:
        add_cbs_logo_to_plot(
            fig=fig,
            axes=axes,
            x0=x0,
            y0=y0,
            width=width,
            height=height,
            margin_x_in_mm=logo_margin_x_in_mm,
            margin_y_in_mm=logo_margin_y_in_mm,
            edgecolor=logo_edgecolor,
            fillcolor=logo_fillcolor,
        )


def clean_up_artists(axis, artist_list):
    """
    try to remove the artists stored in the artist list belonging to the 'axis'.
    :param axis: clean artists belonging to these axis
    :param artist_list: list of artist to remove
    :return: nothing
    """
    for artist in artist_list:
        try:
            # fist attempt: try to remove collection of contours for instance
            while artist.collections:
                for col in artist.collections:
                    artist.collections.remove(col)
                    try:
                        axis.collections.remove(col)
                    except ValueError:
                        pass

                artist.collections = []
                axis.collections = []
        except AttributeError:
            pass

        # second attempt, try to remove the text
        try:
            artist.remove()
        except (AttributeError, ValueError):
            pass
