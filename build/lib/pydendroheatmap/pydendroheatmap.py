#
# The MIT License (MIT)
#
# Copyright (c) 2015 Matthew Antalek Jr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import matplotlib.pyplot as pylab
import matplotlib
import matplotlib as mpl
import scipy.cluster.hierarchy as sch
import numpy as np



class DendroHeatMap(object):
    """
    Class for quickly and easily plotting heatmaps with dendrograms on the side, as seen in
    http://code.activestate.com/recipes/578175-hierarchical-clustering-heatmap-python/
    """

    def __init__(self,
                 heat_map_data=None,
                 left_dendrogram=None,
                 top_dendrogram=None,
                 window_height=10,
                 window_width = 14,
                 color_bar_width = 0.015,
                 left_dendro_x=0.05,
                 left_dendro_y=0.22,
                 left_dendro_width=0.2,
                 left_dendro_height=0.6,
                 left_dendro_x_distance_to_row_cb=0.004,
                 left_dendro_y_distance_to_col_cb=0.004,
                 top_dendro_x=0.273,
                 top_dendro_y=0.843,
                 top_dendro_width=0.5,
                 top_dendro_height=0.117,
                 row_cb_x=0.254,
                 row_cb_y=0.22,
                 row_cb_width=0.015,
                 row_cb_height=0.6,
                 row_cb_on=True,
                 col_cb_x = 0.273,
                 col_cb_y=0.824,
                 col_cb_width=0.5,
                 col_cb_height=0.015,
                 col_cb_on=True,
                 heat_x=0.273,
                 heat_y=0.22,heat_width=0.5,
                 heat_height=0.6,
                 color_legend_x=0.07,
                 color_legend_y=0.88,
                 color_legend_width=0.2,
                 color_legend_height=0.09,
                 color_legend_ticks=7,
                 row_labels=None,
                 max_row_labels=100,
                 row_labels_size=8,
                 col_labels=None,
                 max_col_labels=100,
                 col_labels_size=8,
                 left_colorbar_labels = None,
                 left_colorbar_legend_names = None,
                 font_size = 20,
                 verbose=False):

        self.figure = None
        self.verbose= verbose

        # print 'should be moving into setter land....'
        self.heat_map_data = heat_map_data
        self.top_dendrogram = top_dendrogram
        self.left_dendrogram = left_dendrogram

        #set the default behaviors
        self.window_height=window_height
        self.window_width=window_width
        self.color_bar_width=color_bar_width

        self.left_dendro_x=left_dendro_x
        self.left_dendro_y=left_dendro_y
        self.left_dendro_width=left_dendro_width
        self.left_dendro_height=left_dendro_height
        self.left_dendro_x_distance_to_row_cb=left_dendro_x_distance_to_row_cb
        self.left_dendro_y_distance_to_col_cb=left_dendro_y_distance_to_col_cb


        self.top_dendro_x=top_dendro_x
        self.top_dendro_y=top_dendro_y
        self.top_dendro_width = top_dendro_width
        self.top_dendro_height=top_dendro_height

        # self.cluster_cb_colors = mpl.colors.ListedColormap(['r', 'g', 'b', 'y', 'w', 'k', 'm'])
        self.cluster_cb_colors = mpl.colors.LinearSegmentedColormap.from_list(name="custom",
                                                                              colors=['r', 'g', 'b', 'y', 'w', 'k', 'm'],
                                                                              N=10)

        self.row_cb_x=row_cb_x
        self.row_cb_y = row_cb_y
        self.row_cb_width=row_cb_width
        self.row_cb_height=row_cb_height
        self.row_cb_on=row_cb_on

        self.col_cb_x=col_cb_x
        self.col_cb_y=col_cb_y
        self.col_cb_width=col_cb_width
        self.col_cb_height=col_cb_height
        self.col_cb_on=col_cb_on

        self.heat_x=heat_x
        self.heat_y=heat_y
        self.heat_width=heat_width
        self.heat_height=heat_height

        self.color_legend_x=color_legend_x
        self.color_legend_y=color_legend_y
        self.color_legend_width=color_legend_width
        self.color_legend_height=color_legend_height
        self.color_legend_ticks = color_legend_ticks

        self.row_labels=row_labels
        self.row_labels_size=row_labels_size
        self.max_row_labels=max_row_labels

        self.col_labels=col_labels
        self.col_labels_size=col_labels_size
        self.max_col_labels=max_col_labels

        self.redBlackBlue=self.__RedBlackBlue()
        self.redBlackSkyBlue=self.__RedBlackSkyBlue()
        self.redBlackGreen=self.__RedBlackGreen()
        self.yellowBlackBlue=self.__YellowBlackBlue()
        self.colormap=self.redBlackGreen



        self.left_dendro_title = ''
        self.top_dendro_title = ''
        self.title = ''
        self.color_legend_title = ''
        self.plotRendered = False
        self.font_size = font_size
        self.exportDPI = 600

        self.left_colorbar_labels = left_colorbar_labels
        self.left_colorbar_legend_names = left_colorbar_legend_names





    def render_plot(self,showFrames=False):
        self.resetPlot()
        matplotlib.rcParams.update({"font.size":self.font_size})

        if(self.verbose):
            print('Rendering plot...')

        self.figure = pylab.figure(figsize=[self.window_width, self.window_height])

        #plot the top dendrogram
        if(not self.top_dendrogram is None):
            self.top_dendro_axes = self.figure.add_axes([self.top_dendro_x, self.top_dendro_y, self.top_dendro_width, self.top_dendro_height], frame_on=showFrames)
            self.top_dendro_plot = sch.dendrogram(self.top_dendrogram)
            self.top_dendro_axes.set_xticks([])
            self.top_dendro_axes.set_yticks([])
            self.top_dendro_axes.set_title(self.top_dendro_title)

        #plot the left dendrogram
        if(not self.left_dendrogram is None):
            self.left_dendro_axes = self.figure.add_axes([self.left_dendro_x, self.left_dendro_y, self.left_dendro_width, self.left_dendro_height], frame_on=showFrames)
            self.left_dendro_plot = sch.dendrogram(self.left_dendrogram,orientation='left')
            self.left_dendro_axes.set_xticks([])
            self.left_dendro_axes.set_yticks([])
            self.left_dendro_axes.set_title(self.left_dendro_title,rotation='vertical')

        #plot the heat map
        if(not self.heat_map_data is None):
            self.heat_map_axes = self.figure.add_axes([self.heat_x, self.heat_y, self.heat_width, self.heat_height], frame_on=showFrames)
            self.heat_map_plot = self.heat_map_axes.matshow(self.heat_map_data, aspect='auto', origin='lower', cmap=self.colormap, norm=self.cmap_norm)
            self.heat_map_axes.set_xticks([])
            self.heat_map_axes.set_yticks([])
            self.heat_map_rows = self.heat_map_data.shape[0]
            self.heat_map_cols = self.heat_map_data.shape[1]

            #add the from the labels to the figure
            # print len(self.row_labels)
            row_scale_factor = float(self.window_height) / self.heat_map_data.shape[0]
            for i in range(0, self.heat_map_rows):
                if(self.row_labels):
                    if(len(self.row_labels) < self.max_row_labels):
                        self.heat_map_axes.text(self.heat_map_cols-0.5, i-0.5, ' '+self.row_labels[i], size=self.row_labels_size)

            for i in range(0, self.heat_map_cols):
                if(self.col_labels):
                    if(len(self.col_labels) < self.max_col_labels):
                        self.heat_map_axes.text(i-0.2, self.heat_map_rows-self.heat_map_rows-0.5, ' '+self.col_labels[i], size=self.col_labels_size, rotation=270,verticalalignment='top')


        #plot the column colorbar
        if(not self.top_dendrogram is None):
            self.col_cb_axes = self.figure.add_axes([self.col_cb_x, self.col_cb_y, self.col_cb_width, self.col_cb_height], frame_on=True)
            # print self.top_colorbar_labels.shape
            # print 'Col cb'
            # print [self.col_cb_x, self.col_cb_y, self.col_cb_width, self.col_cb_height]
            self.col_cb_plot = self.col_cb_axes.matshow(self.top_colorbar_labels,aspect='auto',origin='lower',cmap=self.cluster_cb_colors)
            self.col_cb_axes.set_xticks([])
            self.col_cb_axes.set_yticks([])

        #plot the row colorbar
        if(not self.left_dendrogram is None):
            self.row_cb_axes = self.figure.add_axes([self.row_cb_x, self.row_cb_y, self.row_cb_width, self.row_cb_height], frame_on=True)
            # print self.left_colorbar_labels.shape
            # print 'Row cb'
            # print [self.row_cb_x, self.row_cb_y, self.row_cb_width, self.row_cb_height]
            self.row_cb_plot = self.row_cb_axes.matshow(self.left_colorbar_labels, aspect='auto',origin='lower',cmap=self.cluster_cb_colors)
            self.row_cb_axes.set_xticks([])
            self.row_cb_axes.set_yticks([])

        #plot the color legend
        if(not self.heat_map_data is None):
            self.color_legend_axes = self.figure.add_axes([self.color_legend_x, self.color_legend_y, self.color_legend_width, self.color_legend_height], frame_on=showFrames)
            self.color_legend_plot = mpl.colorbar.ColorbarBase(self.color_legend_axes, cmap=self.colormap, norm=self.cmap_norm,orientation='horizontal')
            tl=mpl.ticker.MaxNLocator(nbins=self.color_legend_ticks)
            self.color_legend_plot.locator = tl
            self.color_legend_plot.update_ticks()
            self.color_legend_axes.set_title(self.color_legend_title)
            self.heat_map_axes.format_coord = self.__formatCoords

        #plot the row colorbar if its been set
        if(not self.left_colorbar_labels is None and self.left_dendrogram is None):
            #reset the colorbar
            n_cb_classes = len(set(self.left_colorbar_labels[:, 0].tolist()))
            self.cluster_cb_colors = mpl.colors.LinearSegmentedColormap.from_list(name="custom",
                                                                                  colors=['r', 'g', 'b', 'y', 'w', 'k', 'm'],
                                                                                  N=n_cb_classes)

            self.row_cb_axes = self.figure.add_axes([self.row_cb_x, self.row_cb_y, self.row_cb_width, self.row_cb_height], frame_on=True)
            self.row_cb_plot = self.row_cb_axes.matshow(self.left_colorbar_labels, aspect='auto',origin='lower',cmap=self.cluster_cb_colors)
            self.row_cb_axes.set_xticks([])
            self.row_cb_axes.set_yticks([])
            self.row_cb_axes.legend(label=self.left_colorbar_legend_names)

            # if(not self.left_colorbar_legend_names is None):
            #     cbaxes = self.figure.add_axes([0.1, 0.1, 0.03, 0.8])
            #     self.left_colorbar_legend = pylab.colorbar(self.row_cb_plot, cax=cbaxes)
            #     self.left_colorbar_legend.set_label(self.left_colorbar_legend_names)

        self.figure.suptitle(self.title)


        self.plotRendered = True

        if(self.verbose):
            print( 'Plot rendered...')


    def show(self):
        self.resetPlot()
        self.render_plot()
        pylab.show()

    def export(self,filename):
        self.resetPlot()
        if('.' not in filename):
            filename += '.png'
        else:
            if(self.verbose):
                print ('Saving plot to: ', filename)
            self.render_plot()
            pylab.savefig(filename,dpi=self.exportDPI)



    @property
    def heat_map_data(self):
        return self.__heat_map_data

    @heat_map_data.setter
    def heat_map_data(self, heat_map_data):
        # print 'In the setter...'
        self.__heat_map_data=heat_map_data
        self.resetPlot()
        # print type(heat_map_data)
        if((isinstance(heat_map_data,np.ndarray)) | (isinstance(heat_map_data,np.matrix))):
            hm_min = heat_map_data.min()
            hm_max = heat_map_data.max()
            self.cmap_norm = mpl.colors.Normalize(hm_min,hm_max)
        else:
            raise TypeError('Data for the heatmap must be a numpy.ndarray or numpy.matrix object!')


    def resetPlot(self):
        self.plotRendered = False
        if(self.figure):
            pylab.close(self.figure)
            self.figure = None
        else:
            self.figure = None

    @property
    def figure(self):
        return self.__figure

    @figure.setter
    def figure(self,figure):
        self.__figure = figure
        if((not isinstance(figure, pylab.Figure)) & (isinstance(figure,object))):
            #this force's the figure to either be "None" type or a pylab.Figure object
            self.__figure = None


    @property
    def row_labels(self):
        return self.__row_labels

    @row_labels.setter
    def row_labels(self, row_labels):
        if(not isinstance(self.heat_map_data,np.ndarray) or not isinstance(self.heat_map_data, np.matrix)):
            if(self.verbose):
                print ("""Warning: data for heat map not yet specified, be sure that the number of elements in row_labels
                is equal to the number of rows in heat_map_data.
                """)
            self.__row_labels = row_labels
        else:
            if(len(row_labels) != self.heat_map_data.shape[0]):
                print ("""Invalid entry for row_labels. Please be sure that the number of elements in row_labels is equal
                to the number of rows in heat_map_data.""")
                self.__row_labels = None
            else:
                self.__row_labels = row_labels


    @property
    def col_labels(self):
        return self.__col_labels

    @col_labels.setter
    def col_labels(self, col_labels):
        if(not isinstance(self.heat_map_data,np.ndarray) or not isinstance(self.heat_map_data, np.matrix)):
            if(self.verbose):
                print ("""Warning: data for heat map not yet specified, be sure that the number of elements in col_labels
                is equal to the number of columns in heat_map_data.
                """)
            self.__col_labels = col_labels
        else:
            if(len(col_labels) != self.heat_map_data.shape[0]):
                print ("""Invalid entry for col_labels. Please be sure that the number of elements in col_labels is equal
                to the number of columns in heat_map_data.""")
                self.__col_labels = None
            else:
                self.__col_labels = col_labels


    @property
    def colormap(self):
        return self.__colormap

    @colormap.setter
    def colormap(self, colormap):
        self.__colormap = colormap
        self.resetPlot()


    @property
    def top_dendrogram(self):
        return self.__top_dendrogram

    @top_dendrogram.setter
    def top_dendrogram(self,top_dendrogram):
        if(isinstance(top_dendrogram,np.ndarray)):
            self.__top_dendrogram = top_dendrogram
            self.resetPlot()
            self.top_colorbar_labels = np.array(sch.fcluster(top_dendrogram,0.7*max(top_dendrogram[:,2]),'distance'),dtype=int)
            self.top_colorbar_labels.shape = (1,len(self.top_colorbar_labels))
            temp_dendro = sch.dendrogram(top_dendrogram,no_plot=True)
            self.top_colorbar_labels = self.top_colorbar_labels[:,temp_dendro['leaves']]
        elif top_dendrogram is None:
            self.__top_dendrogram = top_dendrogram
            self.resetPlot()
        else:
            raise TypeError('Dendrograms must be a n-1 x 4 numpy.ndarray as per the scipy.cluster.hierarchy implementation!')

    @property
    def left_dendrogram(self):
        return self.__left_dendrogram

    @left_dendrogram.setter
    def left_dendrogram(self,left_dendrogram):

        if isinstance(left_dendrogram,np.ndarray):
            self.__left_dendrogram = left_dendrogram
            self.resetPlot()
            self.left_colorbar_labels = np.array(sch.fcluster(left_dendrogram,0.7 * max(left_dendrogram[:,2]),'distance'), dtype=int)
            self.left_colorbar_labels.shape = (len(self.left_colorbar_labels),1)
            temp_dendro = sch.dendrogram(left_dendrogram,no_plot=True)
            self.left_colorbar_labels = self.left_colorbar_labels[temp_dendro['leaves'],:]
        elif left_dendrogram is None:
            self.__left_dendrogram = left_dendrogram
            self.resetPlot()

        else:
            raise TypeError('Dendrograms must be a n-1 x 4 numpy.ndarray as per the scipy.cluster.hierarchy implementation!')


    @property
    def left_colorbar_labels(self):
        return self._left_colorbar_labels

    @left_colorbar_labels.setter
    def left_colorbar_labels(self, left_colorbar_labels):
        if isinstance(left_colorbar_labels, list):
            self._left_colorbar_labels = np.array(left_colorbar_labels)
            self._left_colorbar_labels.shape = (len(self._left_colorbar_labels), 1)
        elif isinstance(left_colorbar_labels, np.ndarray):
            self._left_colorbar_labels = left_colorbar_labels
            self._left_colorbar_labels.shape = (len(self._left_colorbar_labels), 1)

        elif left_colorbar_labels is None:
            self._left_colorbar_labels = left_colorbar_labels
        else:
            raise TypeError("'left_colorbar_labels' must be a list or numpy.ndarray")







    def __RedBlackSkyBlue(self):
        cdict = {'red':   ((0.0, 0.0, 0.0),
                           (0.5, 0.0, 0.1),
                           (1.0, 1.0, 1.0)),

                 'green': ((0.0, 0.0, 0.9),
                           (0.5, 0.1, 0.0),
                           (1.0, 0.0, 0.0)),

                 'blue':  ((0.0, 0.0, 1.0),
                           (0.5, 0.1, 0.0),
                           (1.0, 0.0, 0.0))
                }

        my_cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        return my_cmap

    def __RedBlackBlue(self):
        cdict = {'red':   ((0.0, 0.0, 0.0),
                           (0.5, 0.0, 0.1),
                           (1.0, 1.0, 1.0)),

                 'green': ((0.0, 0.0, 0.0),
                           (1.0, 0.0, 0.0)),

                 'blue':  ((0.0, 0.0, 1.0),
                           (0.5, 0.1, 0.0),
                           (1.0, 0.0, 0.0))
                }

        my_cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        return my_cmap


    def __RedBlackGreen(self):
        cdict = {'red':   ((0.0, 0.0, 0.0),
                           (0.5, 0.0, 0.1),
                           (1.0, 1.0, 1.0)),

                 'blue': ((0.0, 0.0, 0.0),
                           (1.0, 0.0, 0.0)),

                 'green':  ((0.0, 0.0, 1.0),
                           (0.5, 0.1, 0.0),
                           (1.0, 0.0, 0.0))
                }

        my_cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        return my_cmap

    def __YellowBlackBlue(self):
        cdict = {'red':   ((0.0, 0.0, 0.0),
                           (0.5, 0.0, 0.1),
                           (1.0, 1.0, 1.0)),

                 'green': ((0.0, 0.0, 0.8),
                           (0.5, 0.1, 0.0),
                           (1.0, 1.0, 1.0)),

                 'blue':  ((0.0, 0.0, 1.0),
                           (0.5, 0.1, 0.0),
                           (1.0, 0.0, 0.0))
                }
        ### yellow is created by adding y = 1 to RedBlackSkyBlue green last tuple
        ### modulate between blue and cyan using the last y var in the first green tuple
        my_cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        return my_cmap

    def __formatCoords(self, x,y):
        col = int(x+0.5)
        row = int(y+0.5)
        if col>=0 and col<self.heat_map_cols and row>=0 and row<self.heat_map_rows:
            z = self.heat_map_data[row,col]
            return 'x=%1.4f, y=%1.4f, z=%1.4f'%(x, y, z)
        else:
            return 'x=%1.4f, y=%1.4f'%(x, y)
