# pydendroheatmap - a plotting tool for making heatmaps with hierarchically clustered data in python.

pydendroheatmap is registered as a package on PyPI, so to install, simply type

```bash
pip install pydendroheatmap
```

To install the package from source, download the repository, unpack and open a command line prompt in the unpackaged directory. Then simply type:

```bash
python setup.py install
```


To make a plot, simply import the package, and create a DendroHeatMap object. Data for the heatmap and
dendrogram do not need to be specified at the time of creation, however, if no data is supplied then
the plot for these objects will not be rendered. See example uses below.

The data for the heat map should be either a numpy.ndarray or numpy.matrix object, and the top and left dendrogram
data should be in the form of a (n-1) x 4 linkage matrix used in the scipy hierarchical clustering package.

```python
import pydendroheatmap as pdh
try: import cPickle as pickle
except: import pickle

heatmap_array = pickle.load(open('some_data_file.pickle'))#a numpy.ndarray or numpy.matrix, for this example, let's say mxn array
top_dendrogram = pickle.load(open('another_data_file.pickle'))#a (n-1) x 4 array
side_dendrogram = pickle.load(open('a_third_data_file.pickle'))#a (m-1) x 4 array

heatmap = pdh.DendroHeatMap(heat_map_data=heatmap_array, left_dendrogram=side_dendrogram, top_dendrogram=top_dendrogram)
heatmap.title = 'This is an example'
heatmap.show()

heatmap.colormap = heatmap.yellowBlackBlue

heatmap.show()

heatmap.row_labels = ['some', 'row','labels'] #must have the same number of rows in heat_map_data

heatmap.reset_plot()
heatmap.show()

#excellent, let's export it

heatmap.export('awesome_heatmap_plot.png')
```


To see a built-in example, run these commands in the python interpreter:

```python
from pydendroheatmap import example
example.run()
```

The example should make a plot that will look similar to this:

![Example Image](https://github.com/themantalope/pydendroheatmap/blob/master/pydendroheatmap/exampledata/example.png)


The DendroHeatMap object's `render_plot()` function will generate a heat plot, similar in fashion to the one found here:

http://code.activestate.com/recipes/578175-hierarchical-clustering-heatmap-python/

Each time the DendroHeatMap object's `show()`, `export()`, and `render_plot()` functions are called,
the plot will be reset and any changes that have been made to the plot's instance variables should be taken into account
in the new plot.

A special thanks to [Nathan Salomonis](http://www.cincinnatichildrens.org/bio/s/nathan-salomonis/) for posting the
original example and figuring out much of the parameters for getting the plots in the correct position!
