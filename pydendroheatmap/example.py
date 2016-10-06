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


import numpy as np
import pydendroheatmap as pdh
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd


def run():

    print ('Here is the source for this example: ')
    print ("""
    import numpy as np
    import pyDendroHeatMap as pdh
    import scipy.cluster.hierarchy as sch
    import scipy.spatial.distance as ssd

    #make up some data
    data = np.random.normal(scale = 50,size=(50,50))
    data[0:25,0:25] += 75
    data[25:,25:] = np.random.poisson(lam=50,size=data[25:,25:].shape)
    #cluster the rows
    row_dist = ssd.squareform(ssd.pdist(data))
    row_Z = sch.linkage(row_dist)
    row_idxing = sch.leaves_list(row_Z)

    row_labels = 50 * ['blah']

    #cluster the columns
    col_dist = ssd.squareform(ssd.pdist(data.T))
    col_Z = sch.linkage(col_dist)
    col_idxing = sch.leaves_list(col_Z)
    #make the dendrogram

    col_labels = 50 * ['blah']

    data = data[:,col_idxing][row_idxing,:]

    heatmap = pdh.DendroHeatMap(heat_map_data=data, left_dendrogram=row_Z, top_dendrogram=col_Z)
    heatmap.row_labels = row_labels
    heatmap.col_labels = col_labels
    heatmap.title = 'An example heatmap'
    heatmap.show()
    """)

    #make up some data
    data = np.random.normal(scale = 50,size=(50,50))
    data[0:25,0:25] += 75
    data[25:,25:] = np.random.poisson(lam=50,size=data[25:,25:].shape)
    #cluster the rows
    row_dist = ssd.squareform(ssd.pdist(data))
    row_Z = sch.linkage(row_dist)
    row_idxing = sch.leaves_list(row_Z)

    row_labels = 50 * ['blah']

    #cluster the columns
    col_dist = ssd.squareform(ssd.pdist(data.T))
    col_Z = sch.linkage(col_dist)
    col_idxing = sch.leaves_list(col_Z)
    #make the dendrogram

    col_labels = 50 * ['blah']

    data = data[:,col_idxing][row_idxing,:]

    heatmap = pdh.DendroHeatMap(heat_map_data=data,left_dendrogram=row_Z, top_dendrogram=col_Z)
    heatmap.row_labels = row_labels
    heatmap.col_labels = col_labels
    heatmap.title = 'An example heatmap'
    heatmap.show()




if __name__ == '__main__':
    run()