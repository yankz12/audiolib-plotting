import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import EngFormatter
from scipy.fftpack import fftshift

# TODO: Try to write plotting as pyplot wrapper
# TODO: Rewrite with OOP

_ENG_FORMAT = EngFormatter()

class BlittedCursor:
    """
    A cross-hair cursor using blitting for faster redraw.
    Copied from matplotlib Examples:
    https://matplotlib.org/stable/gallery/event_handling/cursor_demo.html

    Example:
    >>> import audiolib.plotting as al_plt
    >>> fig = plt.figure()
    >>> ax = plt.gca()
    >>> cursor = al_plt.BlittedCursor(ax)
    >>> fig.canvas.mpl_connect('motion_notify_event', cursor.on_mouse_move)
    """
    def __init__(self, ax):
        self.ax = ax
        self.background = None
        self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--', alpha=.7)
        self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--', alpha=.7)
        # text location in axes coordinates
        self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)
        self._creating_background = False
        ax.figure.canvas.mpl_connect('draw_event', self.on_draw)

    def on_draw(self, event):
        self.create_new_background()

    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw

    def create_new_background(self):
        if self._creating_background:
            # discard calls triggered from within this function
            return
        self._creating_background = True
        self.set_cross_hair_visible(False)
        self.ax.figure.canvas.draw()
        self.background = self.ax.figure.canvas.copy_from_bbox(self.ax.bbox)
        self.set_cross_hair_visible(True)
        self._creating_background = False

    def on_mouse_move(self, event):
        if self.background is None:
            self.create_new_background()
        if not event.inaxes:
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.restore_region(self.background)
                self.ax.figure.canvas.blit(self.ax.bbox)
        else:
            self.set_cross_hair_visible(True)
            # update the line positions
            x, y = event.xdata, event.ydata
            self.horizontal_line.set_ydata([y])
            self.vertical_line.set_xdata([x])
            self.text.set_text(f'x={x:1.2f}, y={y:1.2f}')

            self.ax.figure.canvas.restore_region(self.background)
            self.ax.draw_artist(self.horizontal_line)
            self.ax.draw_artist(self.vertical_line)
            self.ax.draw_artist(self.text)
            self.ax.figure.canvas.blit(self.ax.bbox)

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
        ax.xaxis.set_major_formatter(_ENG_FORMAT)
    if scient_scale_y:
        ax.yaxis.set_major_formatter(_ENG_FORMAT)
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

def plot_h_full(f, f_msc, magnitude, phase_deg, msc,):
    fig = plt.figure()
    plt.subplot(311)
    ax_mod = plt.gca()
    ax_mod.plot(f, magnitude)
    ax_mod.grid(which='both')
    ax_mod.set_ylabel('Magnitude [dB]')
    plt.subplot(312, sharex=ax_mod)
    ax_arg = plt.gca()
    ax_arg.plot(f, phase_deg,)
    ax_arg.set_ylabel('Phase [Deg]')
    ax_arg.grid(which='both')
    plt.subplot(313, sharex=ax_mod)
    ax_msc = plt.gca()
    ax_msc.plot(f_msc, msc,)
    ax_msc.set_ylabel('MSC')
    ax_msc.grid(which='both')
    ax_msc.set_xlabel('Frequency [Hz]')
    ax_msc.set_ylim([.5, 1.2])
    _ = plt.setp(ax_mod.get_xticklabels(), visible=False)
    _ = plt.setp(ax_arg.get_xticklabels(), visible=False)

    return fig, ax_mod, ax_arg, ax_msc,

def plot_mag_phase(
        f,
        magnitude,
        phase_deg,
        phase_xlim_idcs=None,
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
    f : array
        Frequency vector
    magnitude : array
        Magnitude vector
    phase_deg : float
        Phase in Degree
    phase_xlim_idcs : np.array, optional, defaults to None
        Array of frequency limits to show for phase. The form is:
        [
            [lower_lim_1st, upper_lim_1st,],
            [lower_lim_2nd, upper_lim_2nd,],
            [lower_lim_3rd, upper_lim_3rd,],
            ...
        ]
        with 1st, 2nd, ... being the 1st, 2nd, ... harmonic FRF.
        If one of the two entries for a harmonic is None, no limits will
        be applied at all to this HHFRF.
        Reason: Phase sometimes does not give valuable information outside
        frequency range under study, would only distort the visuals.
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
    ax_mag : matplotlib.axes._axes.Axes
        Axes instance of magnitude axis
    ax_arg : matplotlib.axes._axes.Axes
        Axes instance of phase axis

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
    if len(phase_xlim_idcs) != len(phase_deg.transpose()):
        raise ValueError(
            f'XLim phase indices array has to be of same len as phase_deg ' +
            f'but is of len {len(phase_xlim_idcs)} instead '
            f'of {len(phase_deg.transpose())}.'
        )

    plt.subplot(211)
    if ax_mag is None:
        ax_mag = plt.gca()
    plot_func_mag = _parse_plot_func(
        ax_mag,
        xscale,
        yscale_mag,
    )
    plot_func_mag(f, magnitude, **line_kwargs)
    ax_mag.set_ylabel('Magnitude')

    plt.subplot(212, sharex=ax_mag)
    if ax_arg is None:
        ax_arg = plt.gca()
    plot_func_arg = _parse_plot_func(
        ax_arg,
        xscale,
        'lin',
    )
    for idx, lims in enumerate(phase_xlim_idcs):
        no_lims = (lims[0] is None) or (lims[1] is None)
        plot_func_arg(
            f if no_lims else f[lims[0]:lims[1]],
            phase_deg[:, idx] if no_lims else phase_deg[lims[0]:lims[1], idx],
            **line_kwargs,
        ) # TODO: Implement that just one None will be properly interpreted
    
    ax_arg.set_ylabel('Phase [Deg]')
    ax_arg.set_xlabel('Frequency [Hz]')

    ax_mag = _axis_formatter(ax_mag, scient_scale_x, scient_scale_y, )
    if 'label' in line_kwargs:
        ax_mag.legend()
    ax_mag.grid(visible = True, which='both', axis='both', )
    ax_arg.grid(visible = True, which='both', axis='both', )

    return fig, ax_mag, ax_arg,

def plot_2d_pressure(
    x_coords,
    y_coords,
    vals,
    fig=None,
    ax=None,
    interactive_on=False,
    **pcolor_kwargs
):
    if interactive_on:
        plt.ion()
    fig = plt.figure()
    mesh_color = plt.pcolormesh(x_coords, y_coords, vals, **pcolor_kwargs)
    ax = plt.gca()
    cbar = fig.colorbar(mappable=mesh_color, ax=ax)
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    cbar.ax.set_ylabel('Pressure Level [dB SPL]')
    plt.tight_layout()
    return fig, ax, cbar

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
        plus a specified unit, e.g., 10 MHz instead of 1e7 Hz. Defaults to True.
    scient_scale_y : boolean
        If True, y-axis is shown using engineering prefixes to represent powers of 1000,
        e.g., 10 MHz instead of 1e7 Hz. Defaults to False.
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

def unit_circle(radius=1, theta_res=1000, fig=None, ax=None, **line_kwargs, ):
    # TODO: Test
    if (fig is None) and (ax is None):
        fig = plt.figure()
        ax = plt.gca()    
    theta = np.arange(0, 2*np.pi, 2*np.pi/theta_res)
    unit_circle = radius*np.exp(1j*theta)
    ax.plot(np.real(unit_circle), np.imag(unit_circle), **line_kwargs)
    return fig, ax, 

