import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import EngFormatter
from scipy.fftpack import fftshift

# TODO: Try to write plotting as pyplot wrapper
# TODO: Rewrite with OOP

ENG_FORMAT = EngFormatter()

def _parse_plot_func(
        ax,
        xscale,
        yscale,
):
    if xscale == 'lin' and yscale == 'lin':
        return ax.plot
    if xscale == 'log' and yscale == 'lin':
        return ax.semilogx
    if xscale == 'lin' and yscale == 'log':
        return ax.semilogy
    if xscale == 'log' and yscale == 'log':
        return ax.loglog

def _axis_formatter(
        ax,
        scient_scale_x,
        scient_scale_y,
):
    if scient_scale_x:
        ax.xaxis.set_major_formatter(ENG_FORMAT)
    if scient_scale_y:
        ax.yaxis.set_major_formatter(ENG_FORMAT)
    return ax

def plot_time(
        t,
        data,
        scient_scale_x=False,
        scient_scale_y=False,
        fig=None,
        ax=None,
        interactive_on=False,
        **line_kwargs,
    ):
    if interactive_on:
        plt.ion()
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = plt.gca()
    ax.plot(t, data, **line_kwargs)
    ax = _axis_formatter(ax, scient_scale_x, scient_scale_y, )
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude')  
    ax.grid(True, which='both')
    if 'label' in line_kwargs:
        ax.legend()
    return fig, ax,

def plot_rfft_freq(
        f,
        data,
        xscale='lin',
        yscale='lin',
        scient_scale_x=True,
        scient_scale_y=False,
        fig=None,
        ax=None,
        interactive_on=False,
        **line_kwargs,
):

    if interactive_on:
        plt.ion()
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = plt.gca()
    plot_func = _parse_plot_func(
        ax,
        xscale,
        yscale,
    )
    plot_func(f, data, **line_kwargs)
    ax = _axis_formatter(ax, scient_scale_x, scient_scale_y, )
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude')  
    ax.grid(True, which='both')
    if 'label' in line_kwargs:
        ax.legend()
    return fig, ax,

def plot_h_full(freq_h, freq_msc, magnitude, phase_deg, msc,):
    fig = plt.figure()
    plt.subplot(311)
    ax_mod = plt.gca()
    ax_mod.plot(freq_h, magnitude)
    ax_mod.grid(which='both')
    ax_mod.set_ylabel('Magnitude [dB]')
    plt.subplot(312, sharex=ax_mod)
    ax_arg = plt.gca()
    ax_arg.plot(freq_h, phase_deg,)
    ax_arg.set_ylabel('Phase [Deg]')
    ax_arg.grid(which='both')
    plt.subplot(313, sharex=ax_mod)
    ax_msc = plt.gca()
    ax_msc.plot(freq_msc, msc,)
    ax_msc.set_ylabel('MSC')
    ax_msc.grid(which='both')
    ax_msc.set_xlabel('Frequency [Hz]')
    ax_msc.set_ylim([.5, 1.2])
    _ = plt.setp(ax_mod.get_xticklabels(), visible=False)
    _ = plt.setp(ax_arg.get_xticklabels(), visible=False)

    return fig, ax_mod, ax_arg, ax_msc,

def plot_mag_phase(
        freq_h,
        magnitude,
        phase_deg,
        xscale='lin',
        yscale_mag='lin',
        scient_scale_x=True,
        scient_scale_y=False,
        fig=None,
        ax_mag=None,
        ax_arg=None,
        interactive_on=False,
        **line_kwargs,
):
    """
    Plot Magnitude and phase in 211/212 subplots. Subplots share xaxis.

    Parameters
    ----------
    freq : array
        Frequency vector
    magnitude : array
        Magnitude vector
    phase_deg : float
        Phase in Degree
    xscale : str
        Options: 'lin', 'log', Defines wether the shared xaxis will be plotted linearly
        or logarithmically. Defaults to 'lin'
    yscale_mag : boolean
        Options: 'lin', 'log', Defines wether the yaxis of magnitude will be plotted 
        linearly or logarithmically. Phase y-axis is always linear. Defaults to 'lin'.
    scient_scale_x : boolean
        If True, x-axis is shown using engineering prefixes to represent powers of 1000,
        e.g., 10 k instead of 10e3. Defaults to True.
    scient_scale_y : boolean
        If True, y-axis is shown using engineering prefixes to represent powers of 1000,
        e.g., 10 k instead of 10e3. Defaults to False.
    interactive_on : boolean
        Sets pyplot.ion() to this value to allow pyplot interactivity. Defaults to False.
    fig : matplotlib.figure.Figure
        Figure instance of figure to be plotted in. Has to be subplot of 211/212
    ax : matplotlib.axes._axes.Axes
        Axes instance of axis to be plotted in. Has to be subplot of 211/212
    *args

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure instance of current IR fig
    ax : matplotlib.axes._axes.Axes
        Axes instance of current IR fig

    Other Parameters
    ----------------
    **line_kwargs : `~matplotlib.lines.Line2D` properties, optional
        *kwargs* are used to specify properties like a line label (for
        auto legends), linewidth, antialiasing, marker face color.
        Example::

        >>> plot([1, 2, 3], [1, 2, 3], 'go-', label='line 1', linewidth=2)
        >>> plot([1, 2, 3], [1, 4, 9], 'rs', label='line 2')

        If you specify multiple lines with one plot call, the kwargs apply
        to all those lines. In case the label object is iterable, each
        element is used as labels for each set of data.

        Here is a list of available `.Line2D` properties:

        %(Line2D:kwdoc)s
    """
    if interactive_on:
        plt.ion()
    if fig is None:
        fig = plt.figure()

    plt.subplot(211)
    if ax_mag is None:
        ax_mag = plt.gca()
    plot_func_mag = _parse_plot_func(
        ax_mag,
        xscale,
        yscale_mag,
    )
    plot_func_mag(freq_h, magnitude, **line_kwargs)
    ax_mag.grid(which='both')
    ax_mag.set_ylabel('Magnitude')

    plt.subplot(212, sharex=ax_mag)
    if ax_arg is None:
        ax_arg = plt.gca()
    plot_func_arg = _parse_plot_func(
        ax_arg,
        xscale,
        'lin',
    )
    plot_func_arg(freq_h, phase_deg, )
    ax_arg.set_ylabel('Phase [Deg]')
    ax_arg.set_xlabel('Frequency [Hz]')

    ax_mag = _axis_formatter(ax_mag, scient_scale_x, scient_scale_y, )
    if 'label' in line_kwargs:
        ax_mag.legend()
    plt.tight_layout()
    # ax_arg.grid(which='both')
    ax_mag.grid(which='both')
    return fig, ax_mag, ax_arg,

def plot_ir(
        t,
        ir,
        time_plot_width = None,
        time_plot_center = 0,
        scient_scale_x=True,
        scient_scale_y=False,
        fig=None,
        ax=None,
        interactive_on=False,
        **line_kwargs,
):
    """
    Plot zero-centered impulse response.

    Parameters
    ----------
    t : array
        Time vector
    ir : array
        Impulse response to be plotted
    time_plot_width : float
        Time-Width of the plot. Defaults to None (whole IR plotted)
    time_plot_center : float
        Can only be set if time_plot_width is set.
        Defaults to t = 0.
    scient_scale_x : boolean
        If True, x-axis is shown using engineering prefixes to represent powers of 1000,
        plus a specified unit, e.g., 10 MHz instead of 1e7. Defaults to True.
    scient_scale_y : boolean
        If True, y-axis is shown using engineering prefixes to represent powers of 1000,
        e.g., 10 MHz instead of 1e7. Defaults to False.
    interactive_on : boolean
        Sets pyplot.ion() to this value to allow interactivity. Defaults to False.
    fig : matplotlib.figure.Figure
        Figure instance of current IR fig
    ax : matplotlib.axes._axes.Axes
        Axes instance of current IR fig
    *args

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure instance of current IR fig
    ax : matplotlib.axes._axes.Axes
        Axes instance of current IR fig

    Other Parameters
    ----------------
    **line_kwargs : `~matplotlib.lines.Line2D` properties, optional
        *kwargs* are used to specify properties like a line label (for
        auto legends), linewidth, antialiasing, marker face color.
        Example::

        >>> plot([1, 2, 3], [1, 2, 3], 'go-', label='line 1', linewidth=2)
        >>> plot([1, 2, 3], [1, 4, 9], 'rs', label='line 2')

        If you specify multiple lines with one plot call, the kwargs apply
        to all those lines. In case the label object is iterable, each
        element is used as labels for each set of data.

        Here is a list of available `.Line2D` properties:

        %(Line2D:kwdoc)s
    """

    if interactive_on:
        plt.ion()
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = plt.gca()
    if time_plot_width is None:
        time_plot_width = t[-1] # Plot everything if None
    if (time_plot_center - time_plot_width) < t[0]:
        raise ValueError(
            'Chosen plot end smaller than lowest available timestamp. ' +
            'Adjust time_plot_width or time_plot_center.'
        )
    if (time_plot_center + time_plot_width) > t[-1]:
        raise ValueError(
            'Chosen plot end smaller larger than highest available timestamp. ' +
            'Adjust time_plot_width or time_plot_center.'
        )
    ax = _axis_formatter(
        ax,
        scient_scale_x,
        scient_scale_y,
    )
    xlims = [
        time_plot_center - time_plot_width,
        time_plot_center + time_plot_width,
    ]

    fig.set_size_inches([6.4, 3])
    ax = plt.gca()
    ax.set_title('Impulse Response')
    ax.plot(
        t,
        ir,
        '--o',
        **line_kwargs,
    )
    ax.set_xlim(xlims)
    ax.set_xlabel('Time [s]')
    ax.grid()
    plt.tight_layout()
    return fig, ax,

def unit_circle(radius=1, theta_res=1000, fig=None, ax=None, ):
    # TODO: Test
    if (fig is None) and (ax is None):
        fig = plt.figure()
        ax = plt.gca()    
    theta = np.arange(0, 2*np.pi, 2*np.pi/theta_res)
    unit_circle = radius*np.exp(1j*theta)
    ax.plot(np.real(unit_circle), np.imag(unit_circle))
    return fig, ax, 

