######################################################################
# Functions for plotting various things I do alot
######################################################################
# Looks like the best approach is to make a plot class and then have
# the types of plots I like to do inherit from the first plot class
import glob
import matplotlib.pyplot as plt
import numpy as np

import matplotlib

from matplotlib import rcParams
from matplotlib.ticker import MaxNLocator


class plot(object):
    """Plot class to configure matplotlib for publication quality

    """
    def __init__(self, txt_width, frac_width=0.45, font_size=11,
                 font_family='serif', font='Computer Modern Roman',
                 max_ticks=6):
        """Configure the matplotlib settings for publication quality

        These are general parameters that I want to maintain throughout
        the plots in the publication. Specific types of plots can then
        inherit from this.

        Keyword Arguments:
        txt_width   -- from the TeX document \showthe\textwidth
        frac_width  -- fraction of width for figure to occupy
        font_size   -- (default 11) One size smaller than text font size
        font_family -- (default 'serif')
        font        -- (default 'Computer Modern Roman')
        max_ticks   -- (default 6) Max ticks to be spaced nicely
        """
        # set members of the class
        self.txt_width = txt_width
        self.frac_width = frac_width
        self.font_size = font_size
        self.font_family = font_family
        self.font = font
        self.max_ticks = max_ticks

        # dictionary containing the figures
        self.figs = {}

        # now run through the first set up
        self.set_font_size(font_size)
        self.set_font(font_family, font)
        self.set_max_ticks(max_ticks)

    def set_font_size(self, font_size):
        """Set font size
        Keyword Arguments:
        font_size -- font size in pts
        """
        self.font_size = font_size

        # update matplotlib
        rcParams['font.size'] = font_size
        rcParams['axes.labelsize'] = font_size
        rcParams['legend.fontsize'] = font_size
        rcParams['xtick.labelsize'] = font_size-2
        rcParams['ytick.labelsize'] = font_size-2

    def set_font(self, font_family, font, tex=True):
        """Set font

        http://matplotlib.org/api/font_manager_api.html

        Keyword Arguments:
        font_family -- Family
        font        -- Specific font in family
        tex         -- (default True) Use tex in plot
        """
        self.font_family = font_family
        self.font = font

        # update matplotlib
        rcParams['font.family'] = font_family
        rcParams['font.serif'] = [font]
        rcParams['text.usetex'] = tex

    def set_max_ticks(self, max_ticks):
        """Set max plot ticks

        Locator object used as axis handle property arguemnt::
          ax.yaxis.set_major_locator(locator)

        Keyword Arguments:
        max_ticks -- max ticks to use
        """
        self.max_ticks = max_ticks
        self.locator = MaxNLocator(max_ticks)

        # if figures already exist, update them
        # if len(self.figs) > 0:
        #     for j in self.figs:
        #         # get the axis and set the max ticks
        #         ax = self.figs[j].gca()

        #         # set the max ticks
        #         ax.xaxis.set_major_locator(self.locator)
        #         ax.yaxis.set_major_locator(self.locator)

    def set_fig_dims(self, txt_width, frac_width):
        """Return figure dimensions WxH in inches

        By determining the text width in pts of the latex document,
        this will determine the width and height of the figure in
        inches (dimensions for matplotlib) using the golden ratio.

        Get the textwidth from the document by putting this in here
        and checking out the output console::
          \showthe\textwidth
          \showthe\columnwidth

        Keyword Arguments:
        txt_width  -- text width of latex document (pts)
        frac_width -- fraction of the page the figure will take up
        """
        self.txt_width = txt_width
        self.frac_width = frac_width
        fig_width_pt = txt_width * frac_width
        inches_per_pt = 1.0 / 72.27
        golden_ratio = (np.sqrt(5) - 1.0) / 2.0  # DaVinci
        fig_width_in = fig_width_pt * inches_per_pt
        fig_height_in = fig_width_in * golden_ratio
        self.fig_dims = [fig_width_in, fig_height_in]

        # update matplotlib
        rcParams['figure.figsize'] = self.fig_dims

    def new_figure(self, label):
        """Add a new figure for plotting

        Keyword Arguments:
        label -- Name of figure which will also be used as default
        file name
        """
        # add figure to the dictionary
        self.figs[label] = plt.figure()

    def save_figures(self):
        """Save the figures to disk.
        """
        if len(self.figs) < 0:
            print("Please create some figures first.")
        else:
            for j in self.figs:
                # get the axis and set the max ticks
                # ax = self.figs[j].gca()

                # set the max ticks
                # ax.xaxis.set_major_locator(self.locator)
                # ax.yaxis.set_major_locator(self.locator)

                # Use all the whitespace
                self.figs[j].tight_layout(pad=0.1)

                # save as pdf
                self.figs[j].savefig(str(j)+".pdf")
