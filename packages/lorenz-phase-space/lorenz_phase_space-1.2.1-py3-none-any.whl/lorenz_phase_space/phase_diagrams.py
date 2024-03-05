# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    phase_diagrams.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/29 16:13:35 by daniloceano       #+#    #+#              #
#    Updated: 2024/03/04 09:47:55 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pandas as pd
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import cmocean
import numpy as np

def get_max_min_values(series):
    max_val = np.amax(series)
    min_val = np.amin(series)

    if max_val < 0:
        max_val = 1

    if min_val > 0:
        min_val = -1

    return max_val, min_val

class Visualizer:
    def __init__(self, LPS_type='mixed', zoom=False, x_limits=None, y_limits=None, color_limits=None, marker_limits=None,
                 **kwargs):
        
        # Set up figure
        plt.close('all')
        self.fig, self.ax = plt.subplots(figsize=(12, 10))

        # Plotting options
        self.LPS_type = LPS_type
        self.zoom = zoom

        # Fix not zoomed plot to be always fixed limits
        if self.zoom == False:
            x_limits, y_limits = None, None
            color_limits, marker_limits = None, None

        # Set limits
        limits = self.set_limits(x_limits, y_limits)
        color_limits = np.linspace(-15, 15, 100) if color_limits is None else color_limits
        marker_size = np.linspace(2.5e5, 7e5, 100) if marker_limits is None else np.linspace(marker_limits[0], marker_limits[1], 100)

        # Get labels
        labels = self.get_labels()

        # Normalize marker colors based on whether zoom is enabled or not
        if self.zoom:
            self.plot_lines(limits, **kwargs)
            # Get original upper and lower color limits
            original_min_color, original_max_color = color_limits[0], color_limits[-1]
            
            # Adjust limits if necessary
            if original_max_color < 0:
                max_color = 1
            else:
                max_color = original_max_color
            
            if original_min_color > 0:
                min_color = -1
            else:
                min_color = original_min_color
            
            # Ensure normalization is centered around 0 by adjusting min and max proportionally
            max_abs_color = max(abs(min_color), abs(max_color))
            self.norm = colors.TwoSlopeNorm(vmin=-max_abs_color, vcenter=0, vmax=max_abs_color)
            extend = 'both'

        else:
            self.norm = colors.TwoSlopeNorm(vmin=-30, vcenter=0, vmax=30)
            extend = 'neither'

        # Compute marker sizes and intervals
        _, intervals = self.calculate_marker_size(marker_size, self.zoom)
        msizes = [200, 400, 600, 800, 1000]

        # Add legend with dynamic intervals and sizes
        self.plot_legend(self.ax, intervals, msizes, labels['size_label'])

        # Add colorbar
        sm = plt.cm.ScalarMappable(cmap=cmocean.cm.curl, norm=self.norm)
        sm.set_array([])
        cax = self.ax.inset_axes([self.ax.get_position().x1 + 0.13, self.ax.get_position().y0 + 0.35, 0.02, self.ax.get_position().height / 1.5])
        self.cbar = self.fig.colorbar(sm, extend=extend, cax=cax)
        self.cbar.ax.set_ylabel(labels['color_label'], rotation=270, labelpad=25)  # Customize this
        for t in self.cbar.ax.get_yticklabels():
            t.set_fontsize(10)

        # Add annotations
        self.annotate_plot(self.ax, self.cbar)
        self.plot_gradient_lines(**kwargs) if not self.zoom else []

        plt.subplots_adjust(right=0.8)

    def plot_data(self, x_axis, y_axis, marker_color, marker_size, **kwargs):
        if self.fig is None or self.ax is None:
            print("Plot structure not initialized. Call create_lps_plot first.")
            return
        
        # Standardize input data as pandas Series
        x_axis = pd.Series(x_axis).reset_index(drop=True)
        y_axis = pd.Series(y_axis).reset_index(drop=True)
        marker_color = pd.Series(marker_color).reset_index(drop=True)
        marker_size = pd.Series(marker_size).reset_index(drop=True)

        # arrows connecting dots
        self.ax.quiver(x_axis[:-1].values, y_axis[:-1].values,
                        (x_axis[1:].values - x_axis[:-1].values) * .9,
                        (y_axis[1:].values - y_axis[:-1].values) * .9,
                        angles='xy', scale_units='xy', scale=1, color='k')

        # Compute marker sizes and intervals
        sizes, intervals = self.calculate_marker_size(marker_size, self.zoom)
        msizes = [200, 400, 600, 800, 1000]

        # plot the moment of maximum intensity
        extreme = marker_size.idxmax()
        self.ax.scatter(x_axis.loc[extreme], y_axis.loc[extreme],
                c='None', s=sizes.loc[extreme] * 1.1, zorder=201, edgecolors='k', linewidth=3)

        # Plot the data
        alpha = kwargs.get('alpha', 1)
        cmap = kwargs.get('cmap', cmocean.cm.curl)
        scatter = self.ax.scatter(x_axis, y_axis, c=marker_color, cmap=cmap, zorder=200,
                                  norm=self.norm, s=sizes, edgecolors='k', alpha=alpha)
        
        # Marking start and end of the system
        self.ax.text(x_axis[0], y_axis[0], 'A', zorder=201, fontsize=25,
                horizontalalignment='center', verticalalignment='center')
        self.ax.text(x_axis.iloc[-1], y_axis.iloc[-1], 'Z', zorder=201, fontsize=25,
                horizontalalignment='center', verticalalignment='center')

        return self.fig, self.ax

    @staticmethod
    def calculate_marker_size(term, zoom=False):
        term = pd.Series(term)
        if zoom:
            # Calculate dynamic intervals based on quantiles if zoom is True
            intervals = list(term.quantile([0.2, 0.4, 0.6, 0.8]))

            # Determine the order of magnitude of the minimum interval value
            min_val = min(intervals)
            order_of_magnitude = 10 ** int(np.floor(np.log10(min_val))) if min_val != 0 else 1

            # Round intervals to two orders of magnitude lower than the minimum value
            round_to = order_of_magnitude / 100
            intervals = [round(v, -int(np.log10(round_to))) for v in intervals]
        else:
            # Default intervals
            intervals = [3e5, 4e5, 5e5, 6e5]

        msizes = [200, 400, 600, 800, 1000]
        sizes = pd.Series([msizes[next(i for i, v in enumerate(intervals) if val <= v)] if val <= intervals[-1] else msizes[-1] for val in term])
        return sizes, intervals
        
    def set_limits(self, x_limits=None, y_limits=None): 

        if x_limits is not None and y_limits is not None:
            self.ax.set_xlim(x_limits[0], x_limits[1])
            self.ax.set_ylim(y_limits[0], y_limits[1])

        else:   
            y_limits = {
                'mixed': (-20, 20),
                'baroclinic': (-20, 20),
                'barotropic': (-200, 200)
            }
            self.ax.set_ylim(*y_limits.get(self.LPS_type, (-20, 20)))
            self.ax.set_xlim(-70, 70)

        x_limits, y_limits = self.ax.get_xlim(), self.ax.get_ylim()
        
        return *x_limits, *y_limits

    def get_labels(self):
        labels_dict = {}

        if self.LPS_type == 'mixed':
            labels_dict['y_upper'] = 'Eddy is gaining potential energy \n from the mean flow'
            labels_dict['y_lower'] = 'Eddy is providing potential energy \n to the mean flow'
            labels_dict['x_left'] = 'Eddy is gaining kinetic energy \n from the mean flow'
            labels_dict['x_right'] = 'Eddy is providing kinetic energy \n to the mean flow'
            labels_dict['col_lower'] = 'Subsidence decreases \n eddy potential energy'
            labels_dict['col_upper'] = 'Latent heat release feeds \n eddy potential energy'
            labels_dict['lower_left'] = 'Barotropic instability'
            labels_dict['upper_left'] = 'Barotropic and baroclinic instabilities'
            labels_dict['lower_right'] = 'Eddy is feeding the local atmospheric circulation'
            labels_dict['upper_right'] = 'Baroclinic instability'

            if self.zoom:
                labels_dict['x_label'] = 'Ck - $W m^{-2})$'
                labels_dict['y_label'] = 'Ca - $W m^{-2})$'
                labels_dict['color_label'] = 'Ge - $W m^{-2})$'
                labels_dict['size_label'] = 'Ke - $J m^{-2})$'
            else:
                labels_dict['x_label'] = 'Conversion from zonal to eddy Kinetic Energy (Ck - $W m^{-2})$'
                labels_dict['y_label'] = 'Conversion from zonal to eddy Potential Energy (Ca - $W m^{-2})$'
                labels_dict['color_label'] = 'Generation of eddy Potential Energy (Ge - $W m^{-2})$'
                labels_dict['size_label'] = 'Eddy Kinect\n    Energy\n (Ke - $J m^{-2})$'

        elif self.LPS_type == 'baroclinic':
            labels_dict['y_upper'] = 'Zonal temperature gradient feeds \n eddy potential energy'
            labels_dict['y_lower'] = 'Eddy potential energy feeds \n zonal temperature gradient'
            labels_dict['x_left'] = 'Meridional temperature gradient feeds \n eddy kinetic energy'
            labels_dict['x_right'] = 'Eddy kinetic energy consumes \n meridional temperature gradient'
            labels_dict['col_lower'] = 'Subsidence decreases \n eddy potential energy'
            labels_dict['col_upper'] = 'Latent heat release feeds \n eddy potential energy'
            labels_dict['lower_left'] = 'Baroclinic stability'
            labels_dict['upper_left'] = ''
            labels_dict['lower_right'] = ''
            labels_dict['upper_right'] = 'Baroclinic instability'
            
            if self.zoom:
                labels_dict['x_label'] = 'Ce - $W m^{-2})$'
                labels_dict['y_label'] = 'Ca - $W m^{-2})$'
                labels_dict['color_label'] = 'Ge - $W m^{-2})$'
                labels_dict['size_label'] = 'Ke - $J m^{-2})$'
            else:
                labels_dict['x_label'] = 'Conversion from zonal to eddy Kinetic Energy (Ce - $W m^{-2})$'
                labels_dict['y_label'] = 'Conversion from zonal to eddy Potential Energy (Ca - $W m^{-2})$'
                labels_dict['color_label'] = 'Generation of eddy Potential Energy (Ge - $W m^{-2})$'
                labels_dict['size_label'] = 'Eddy Kinect\n    Energy\n     (Ke - $J m^{-2})$'

        elif self.LPS_type == 'barotropic':
            labels_dict['y_upper'] = 'Importation of Kinectic Energy'
            labels_dict['y_lower'] = 'Exportation of Kinectic Energy'
            labels_dict['x_left'] = 'Eddy is gaining kinetic energy \n from the mean flow'
            labels_dict['x_right'] = 'Eddy is providing kinetic energy \n to the mean flow'
            labels_dict['col_lower'] = 'Subsidence decreases \n eddy potential energy'
            labels_dict['col_upper'] = 'Latent heat release feeds \n eddy potential energy'
            labels_dict['lower_left'] = 'Barotropic instability wihtout \n downstream development'
            labels_dict['upper_left'] = 'Barotropic instability and \n downstream development'
            labels_dict['lower_right'] = 'Barotropic stability without \n downstream development'
            labels_dict['upper_right'] = 'Barotropic stability and \n downstream development'

            if self.zoom:
                labels_dict['x_label'] = 'Ck - $W m^{-2})$'
                labels_dict['y_label'] = 'Bkz - $W m^{-2})$'
                labels_dict['color_label'] = 'Ge - $W m^{-2})$'
                labels_dict['size_label'] = 'Ke - $J m^{-2})$'
            else:
                labels_dict['x_label'] = 'Conversion from zonal to eddy Kinetic Energy (Ck - $Wm^{-2})$'
                labels_dict['y_label'] = ' Kinetic Energy transport across boundaries (BKz - $Wm^{-2})$'
                labels_dict['color_label'] = 'Generation of eddy Potential Energy (Ge - $Wm^{-2})$'
                labels_dict['size_label'] = 'Eddy Kinect\n    Energy\n     (Ke - $J m^{-2})$'            

        return labels_dict
    
    def annotate_plot(self, ax, cbar, **kwargs):
        labelpad = kwargs.get('labelpad', 5) if self.zoom else kwargs.get('labelpad', 38)
        annotation_fontsize = kwargs.get('fontsize', 10)
        label_fontsize = kwargs.get('label_fontsize', 14) if self.zoom else kwargs.get('label_fontsize', 10)
        
        labels = self.get_labels()
            
        # Centering text annotations on y-axis
        yticks, xticks = ax.get_yticks(), ax.get_xticks()
        y_tick_0 = len(yticks) // 2
        y_offset = 0.5 * (yticks[y_tick_0] - yticks[-1])  # Half the distance between two consecutive y-ticks
        x_tick_pos = xticks[0] - ((xticks[1] - xticks[0])/12)

        if not self.zoom:
            ax.text(x_tick_pos, yticks[0] - y_offset, labels['y_lower'], rotation=90, fontsize=annotation_fontsize,
                    horizontalalignment='center', c='#19616C', verticalalignment='center')
            ax.text(x_tick_pos, yticks[-1] + y_offset, labels['y_upper'], rotation=90, fontsize=annotation_fontsize,
                    horizontalalignment='center', c='#CF6D66', verticalalignment='center')
            
            ax.text(0.22,-0.07, labels['x_left'], fontsize=annotation_fontsize,
                    horizontalalignment='center', c='#CF6D66', transform=ax.transAxes)
            ax.text(0.75,-0.07,labels['x_right'], fontsize=annotation_fontsize,
                    horizontalalignment='center', c='#19616C', transform=ax.transAxes)
            
            ax.text(1.13,0.49, labels['col_lower'], rotation=270, fontsize=annotation_fontsize, 
                    horizontalalignment='center', c='#19616C', transform=ax.transAxes)
            ax.text(1.13,0.75, labels['col_upper'], rotation=270,fontsize=annotation_fontsize,
                    horizontalalignment='center', c='#CF6D66', transform=ax.transAxes)
            
            ax.text(0.22,0.03, labels['lower_left'], fontsize=annotation_fontsize, horizontalalignment='center',
                    c='#660066', verticalalignment='center', transform=ax.transAxes)
            ax.text(0.22,0.97, labels['upper_left'], fontsize=annotation_fontsize,horizontalalignment='center',
                    c='#800000', verticalalignment='center', transform=ax.transAxes)
            
            ax.text(0.75,0.03, labels['lower_right'], fontsize=annotation_fontsize,horizontalalignment='center',
                    c='#000066', verticalalignment='center', transform=ax.transAxes)
            ax.text(0.75,0.97,labels['upper_right'], fontsize=annotation_fontsize,horizontalalignment='center',
                    c='#660066', verticalalignment='center', transform=ax.transAxes)
        
        # Write labels
        ax.set_xlabel(labels['x_label'], fontsize=label_fontsize,labelpad=labelpad,c='#383838')
        ax.set_ylabel(labels['y_label'], fontsize=label_fontsize,labelpad=labelpad,c='#383838')
        cbar.ax.set_ylabel(labels['color_label'], rotation=270,fontsize=label_fontsize,
                        verticalalignment='bottom', c='#383838',
                        labelpad=labelpad, y=0.59)
        
    @staticmethod
    def plot_legend(ax, intervals, msizes, title_label):
        labels = ['< ' + str(intervals[0]),
                  '< ' + str(intervals[1]),
                  '< ' + str(intervals[2]),
                  '< ' + str(intervals[3]),
                  '> ' + str(intervals[3])]

        # Create separate scatter plots for each size category
        for i in range(len(msizes)):
            ax.scatter([], [], c='#383838', s=msizes[i], label=labels[i])

        ax.legend(title=title_label, title_fontsize=12,
                  fontsize=10, loc='lower left', bbox_to_anchor=(1, 0, 0.5, 1),
                  labelcolor='#383838', frameon=False, handlelength=0.3, handleheight=4,
                  borderpad=1.5, scatteryoffsets=[0.1], framealpha=1,
                  handletextpad=1.5, scatterpoints=1)
        
    def plot_lines(self, limits, **kwargs):
        # Configure properties from kwargs        
        alpha = kwargs.get('line_alpha', 0.2)
        linewidth = kwargs.get('lw', 20)
        color = kwargs.get('c', '#383838')

        self.ax.axhline(y=0,linewidth=linewidth, c=color, alpha=alpha,zorder=1)
        self.ax.axvline(x=0,linewidth=linewidth, c=color, alpha=alpha,zorder=1)

        # Vertical lines for mixed LPS
        if self.LPS_type == 'mixed':
            # Get the end points of the plot
            end_point_x = limits[0] * 2
            end_point_y = limits[3] * 2

            # Generate points for the line
            x_points = np.linspace(0, end_point_x, 100)
            y_points = np.linspace(0, end_point_y, 100)

            self.ax.plot(x_points, y_points, linewidth=linewidth, c=color, alpha=alpha, zorder=2) 
                
    def plot_gradient_lines(self, **kwargs):
        # Configure properties from kwargs
        LPS_type = self.LPS_type
        linewidth = kwargs.get('lw', 0.5)
        color = kwargs.get('c', '#383838')
        num_lines = 20

        # Get ticks
        x_ticks = self.ax.get_xticks()
        y_ticks = self.ax.get_yticks()

        # Get offsets
        x_previous0 = x_ticks[int((len(x_ticks))/2)-1] * 0.17
        y_previous0 = y_ticks[int((len(y_ticks))/2)-1] * 0.17
        x_offsets = np.linspace(x_previous0, 0, num_lines)
        y_offsets = np.linspace(y_previous0, 0, num_lines)

        alpha_values = np.linspace(0, 0.6, num_lines)

        for i, alpha in enumerate(alpha_values):
            self.ax.axhline(y=0 + y_offsets[i], linewidth=linewidth, alpha=alpha, c=color)
            self.ax.axhline(y=0 - y_offsets[i], linewidth=linewidth, alpha=alpha, c=color)
            self.ax.axvline(x=0 + x_offsets[i], linewidth=linewidth, alpha=alpha, c=color)
            self.ax.axvline(x=0 - x_offsets[i], linewidth=linewidth, alpha=alpha, c=color)

        # Diagonal line
        if LPS_type == 'mixed':
            y_ticks = -x_ticks
            for i, alpha in enumerate(alpha_values):
                x, y = x_offsets[i], y_offsets[i]
                self.ax.plot([x, -x_ticks[-1] + x], [y, -y_ticks[-1] + y], linewidth=linewidth,
                             alpha=alpha, c=color)
                self.ax.plot([-x, -x_ticks[-1] - x], [-y, -y_ticks[-1] - y], linewidth=linewidth,
                             alpha=alpha, c=color)
        
if __name__ == '__main__':
    import random

    sample_file_1 = 'samples/sample_results_1.csv'
    sample_file_2 = 'samples/sample_results_2.csv'
    df_1 = pd.read_csv(sample_file_1, parse_dates={'Datetime': ['Date', 'Hour']},
                       date_format='%Y-%m-%d %H')
    df_2 = pd.read_csv(sample_file_2, parse_dates={'Datetime': ['Date', 'Hour']},
                       date_format='%Y-%m-%d %H')

    x_axis_1 = df_1['Ck'].values
    y_axis_1 = df_1['Ca'].values
    marker_color_1 = df_1['Ge'].values
    marker_size_1 = df_1['Ke'].values

    x_axis_2 = df_2['Ck'].values
    y_axis_2 = df_2['Ca'].values
    marker_color_2 = df_2['Ge'].values
    marker_size_2 = df_2['Ke'].values

    # Test base plot
    lps = Visualizer(LPS_type='mixed', zoom=False)
    fname = 'samples/lps_example'
    plt.savefig(f"{fname}.png", dpi=300)
    print(f"Saved {fname}.png")

    # Test base plot zoom 
    lps = Visualizer(LPS_type='mixed', zoom=True)
    fname = 'samples/lps_example_zoom'
    plt.savefig(f"{fname}.png", dpi=300)
    print(f"Saved {fname}.png")

    # Test without zoom
    lps = Visualizer(LPS_type='mixed', zoom=False)
    lps.plot_data(x_axis_1, y_axis_1, marker_color_1, marker_size_1)
    fname = 'samples/sample_1_LPS_mixed'
    plt.savefig(f"{fname}.png", dpi=300)
    print(f"Saved {fname}.png")

    # Test with zoom
    lps = Visualizer(LPS_type='mixed', zoom=True)
    lps.plot_data(x_axis_1, y_axis_1, marker_color_1, marker_size_1)
    fname = 'samples/sample_1_LPS_mixed_zoom'
    plt.savefig(f"{fname}.png", dpi=300)
    print(f"Saved {fname}.png")

    # Test with sample 2
    lps = Visualizer(LPS_type='mixed', zoom=True)
    lps.plot_data(x_axis_2, y_axis_2, marker_color_2, marker_size_2)
    fname = 'samples/sample_2'
    plt.savefig(f"{fname}.png", dpi=300)
    print(f"Saved {fname}.png")

    # Test with multiple plots - with zoom
    lps = Visualizer(LPS_type='mixed', zoom=True)
    lps.plot_data(x_axis_1, y_axis_1, marker_color_1, marker_size_1)
    lps.plot_data(x_axis_2, y_axis_2, marker_color_2, marker_size_2)
    fname = 'samples/sample_1_LPS_mixed_zoom_multiple'
    plt.savefig(f"{fname}.png", dpi=300)
    print(f"Saved {fname}.png")

    # Test with multiple plots - without zoom
    lps = Visualizer(LPS_type='mixed', zoom=False)
    lps.plot_data(x_axis_1, y_axis_1, marker_color_1, marker_size_1)
    lps.plot_data(x_axis_2, y_axis_2, marker_color_2, marker_size_2)
    fname = 'samples/sample_1_LPS_mixed_multiple'
    plt.savefig(f"{fname}.png", dpi=300)
    print(f"Saved {fname}.png")

    # Test with multiple plots and dynamically selecting limits
    x_min = np.min([*x_axis_1, *x_axis_2])
    x_max = np.max([*x_axis_1, *x_axis_2])
    y_min = np.min([*y_axis_1, *y_axis_2])
    y_max = np.max([*y_axis_1, *y_axis_2])
    color_min = np.min([*marker_color_1, *marker_color_2])
    color_max = np.max([*marker_color_1, *marker_color_2])
    size_min = np.min([*marker_size_1, *marker_size_2])
    size_max = np.max([*marker_size_1, *marker_size_2])

    lps = Visualizer(
        LPS_type='mixed',
        zoom=True,
        x_limits=[x_min, x_max],
        y_limits=[y_min, y_max],
        color_limits=[color_min, color_max],
        marker_limits=[size_min, size_max]
        )
    
    lps.plot_data(x_axis_1, y_axis_1, marker_color_1, marker_size_1)
    lps.plot_data(x_axis_2, y_axis_2, marker_color_2, marker_size_2)
    fname = 'samples/sample_1_LPS_mixed_zoom_multiple_dynamic'
    plt.savefig(f"{fname}.png", dpi=300)
    print(f"Saved {fname}.png")



