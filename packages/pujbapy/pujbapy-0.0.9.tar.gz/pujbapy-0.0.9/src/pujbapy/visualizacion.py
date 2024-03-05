import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use("https://raw.githubusercontent.com/cortizbon/pujbapy/main/viz/pujbapy_style.mplstyle")

def histograma(datos, 
               variable, 
               bins=30, 
               guardar=False,
               alpha=1,
               titulo=None):
  col = datos[variable]
  fig, ax = plt.subplots(1, 1)
  if type(titulo) == str:
    ax.set_title(titulo)
  ax.hist(col, bins=bins, alpha=alpha)
  if guardar:
    fig.savefig("histograma.jpeg")

  return fig


def grafico_barras(datos, 
                   variable_x, 
                   variable_y,
                   guardar=False,
                   titulo=None):
  fig, ax = plt.subplots(1, 1)
  if type(titulo) == str:
    ax.set_title(titulo)

  sns.barplot(datos, 
              x=variable_x, 
              y=variable_y, 
              estimator='count', 
              errorbar=None,
              ax=ax)
  
  if guardar:
    fig.savefig("bar.jpeg")

  return fig

def grafico_dispersion(datos, 
                       variable_x, 
                       variable_y, 
                       hue=None, 
                       size=None, 
                       style=None, 
                       guardar=False,
                       titulo=None):
  fig, ax = plt.subplots(1, 1)
  sns.scatterplot(datos, 
                  x=variable_x, 
                  y=variable_y, 
                  hue=hue,
                  size=size,
                  style=style,
                  ax=ax)
  if type(titulo) == str:
    ax.set_title(titulo)

  if guardar:
    fig.savefig("scatter.jpeg")

  return fig

def grafico_caja(datos, 
                 variable_x, 
                 variable_y, 
                 hue=None,
                 guardar=False,
                 titulo=None):
  fig, ax = plt.subplots(1, 1)

  if type(titulo) == str:
    ax.set_title(titulo)
  sns.boxplot(datos,
              x=variable_x,
              y=variable_y,
              hue=hue,
              ax=ax)
  if guardar:
    fig.savefig("box.jpeg")

  return fig