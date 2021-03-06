# JupyterLab for query Crawlers Data

This file will introduce the process of prepare the environment to execute Jupyter Notebooks in JupyterLab.

## Install and Configure JupiterLab

We will supose that you already have the latest version of Anaconda distribution in your local system

The first thing we should do is create a conda environment that will contain the versions of Python, JupyterLab, and other dependencies.

```
conda create -n davinci-res-api-lab pip python=3.6

The following packages will be downloaded:
    package                    |            build
    ---------------------------|-----------------
    pip-10.0.1                 |           py36_0         1.8 MB
    openssl-1.0.2o             |       h20670df_0         3.4 MB
    sqlite-3.23.1              |       he433501_0         1.5 MB
    xz-5.2.3                   |       h5e939de_4         365 KB
    libgcc-ng-7.2.0            |       hdf63c60_3         6.1 MB
    libstdcxx-ng-7.2.0         |       hdf63c60_3         2.5 MB
    python-3.6.5               |       hc3d631a_2        29.4 MB
    certifi-2018.4.16          |           py36_0         142 KB
    ca-certificates-2018.03.07 |                0         124 KB
    setuptools-39.1.0          |           py36_0         550 KB
    wheel-0.31.0               |           py36_0          62 KB
    ------------------------------------------------------------
                                           Total:        46.0 MB
``` 

We activate the new environment:

```
conda activate davinci-res-api-lab

(davinci-res-api-lab) $
```

Then we are ready to install JupyterLab

```
conda install jupyterlab
```

We need to configure Jupyter to be made available beyond localhost:

```
jupyter notebook --generate-config

Writing default config to: .jupyter/jupyter_notebook_config.py

vi .jupyter/jupyter_notebook_config.py

## The IP address the notebook server will listen on.
c.NotebookApp.ip = '*'
```

We should configure Jupyter to have a general password (instead of a new autogenerated token on every start):

```
jupyter notebook password
Enter password:
Verify password:

Wrote hashed password to .jupyter/jupyter_notebook_config.json
```

Now we are ready to launch Jupyter and access on HTTP port 8888:

```
jupyter lab
```

## Configure JupyterLab to have access to the python environment

From inside the environment we need to install ipykernel using pip:

```
pip install ipykernel
```

And now we can install the new kernel:

```
ipython kernel install --user --name=davinci-res-api-lab
```


## Configure Cassandra Client (DSE)

We only need to install the dse driver (or cassandra-driver):

```
pip install dse-driver
```

Example of how to connect to Cassandra from a notebook:

```
try:
    from dse.cluster import Cluster
except ImportError:
    from cassandra.cluster import Cluster
    
cluster = Cluster(['10.0.0.0'])  # provide contact points and port
session = cluster.connect('keyspace')
rows = session.execute('select * from table limit 5;')

for row in rows:
    print row.id
```


## Using Pandas to manage the data

We can capture the results in a Pandas dataframe (if the data fits in memory):

```
conda install pandas
```

And convert the query results into a pandas dataframe:

```
import pandas as pd

rows = session.execute('select * from table;')
df = pd.DataFrame(list(rows))
```

## Altair

[Altair](https://altair-viz.github.io/getting_started/overview.html) is a declarative statistical visualization library for Python, based on Vega and Vega-Lite.

Altair offers a powerful and concise visualization grammar that enables you to build a wide range of statistical visualizations quickly.

Install Altair and its dependencies:

```
conda install -c conda-forge altair vega_datasets
``` 

Here is an example of using the Altair API to quickly visualize a dataset with an interactive scatter plot.

```
import altair as alt

# load a simple dataset as a pandas DataFrame
from vega_datasets import data
cars = data.cars()

alt.Chart(cars).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
).interactive()
```


## Install interactive widgets

Learning and experimenting with data become truly immersive when user can interactively control the parameters of the model and see the effect (almost) real-time.

there is a big effort to introduce elements called [ipywidgets](http://jupyter.org/widgets.html), which renders fun and interactive controls on the Jupyter notebook. Based on these core elements, several 2D and 3D dynamic data visualization projects (e.g. bqplot, ipyleaflet) are also growing in size and scope.

We have two options for installing ipywidgets:

- Use pip, you also have to enable the ipywidget extension in your notebook to render it next time you start the notebook:

```
pip install ipywidgets
jupyter nbextension enable --py widgetsnbextension
```

- do a Conda install:

```
conda install -c conda-forge ipywidgets
``` 

And we need to install the Jupyter Lab extension:

```
conda install nodejs
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

Example:

```
# Imports
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets as widgets
from IPython.display import display
```

```
# Show a select with two options
widgets.Select(
    options=['Current', 'Consolidated'],
    value='Current',
    description='Financial Information Type:',
    disabled=False
)


```
