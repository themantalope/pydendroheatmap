from setuptools import setup

def readme():
    f = open('README.txt','r')
    text = f.read()
    f.close()
    return text

setup(name='pydendroheatmap',
      version='1.0',
      description='Tool for creating heatmaps, where rows and columns are organized by hierarchical clusters'
                  'as seen in http://code.activestate.com/recipes/578175-hierarchical-clustering-heatmap-python/',
      url='',
      author='Matt Antalek',
      author_email='matthew.antalek@northwestern.edu',
      license='MIT',
      packages=['pydendroheatmap'],
      setup_requires=['numpy'],
      install_requires = [
          'numpy',
          'scipy',
          'matplotlib',

      ],
      long_description=readme(),
      classifiers=['Topic :: Scientific/Engineering :: Visualization'],
      include_package_data=True)