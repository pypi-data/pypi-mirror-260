from utils import DIC_ALTERNATIVAS
import scipy.stats as st


def media_contra_valor(columna, valor, nivel_significancia, hipotesis_alternativa='diferente de'):

  hipot = DIC_ALTERNATIVAS[hipotesis_alternativa]

  stat, pvalor = st.ttest_1samp(columna, valor, alternative=hipot)

  if pvalor < nivel_significancia:
    print(f"Rechazamos la hipótesis nula. La media es estadísticamente {hipotesis_alternativa} {valor}.")
  else:
    print(f"No hay evidencia suficiente para rechazar la hipótesis nula. La media no es {hipotesis_alternativa} {valor}.")
    

def comparar_medias(columna1, columna2, nivel_significancia, hipotesis_alternativa='diferente de', equal_var=False):

  hipot = DIC_ALTERNATIVAS[hipotesis_alternativa]

  stat, pvalor = st.ttest_ind(columna1, columna2, alternative=hipot, equal_var=equal_var)

  if pvalor < nivel_significancia:
    print(f"Rechazamos la hipótesis nula. La media 1 es estadísticamente {hipotesis_alternativa} de la media 2.")
  else:
    print(f"No hay evidencia suficiente para rechazar la hipótesis nula. La media 1 no es estadísticamente {hipotesis_alternativa} de la media 2.")


def comparar_varianzas(columna1, columna2, nivel_significancia):

  stat, pvalor = st.levene(columna1, columna2, nivel_significancia)

  if pvalor < nivel_significancia:
    print(f"Rechazamos la hipótesis nula. La varianza 1 es estadísticamente diferente de la varianza 2.")
  else:
    print(f"No hay evidencia suficiente para rechazar la hipótesis nula. La media 1 es estadísticamente igual de la media 2.")
