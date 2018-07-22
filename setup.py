from setuptools import setup

def readme():
    with open('README.md', 'r') as f:
        text = f.read()

    return text

setup(name='pydendroheatmap',
      version='1.5',
      description='Tool for creating heatmaps, where rows and columns are organized by hierarchical clusters'
                  ' as seen in http://code.activestate.com/recipes/578175-hierarchical-clustering-heatmap-python/',
      url='https://github.com/themantalope/pydendroheatmap',
      author='Matt Antalek Jr',
      author_email='matthew.antalek@northwestern.edu',
      license='MIT',
      packages=['pydendroheatmap'],
      setup_requires=['numpy',
                      'scipy',
            'matplotlib',],
      install_requires = [],
      long_description=readme(),
      classifiers=['Topic :: Scientific/Engineering :: Visualization'],
      include_package_data=True)
