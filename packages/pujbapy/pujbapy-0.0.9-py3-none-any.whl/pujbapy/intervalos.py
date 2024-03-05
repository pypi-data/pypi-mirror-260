import scipy.stats as st
import numpy as np

def intervalo_media(datos, columna, alpha):

    conf_level = 1 - alpha

    dof = len(datos[columna] - 1)
    loc = datos[columna].mean()
    scale = st.sem(datos[columna])


    conf_int = st.t.interval(conf_level, 
                         dof, 
                         loc=loc, 
                         scale=scale)
    
    return conf_int

def intervalo_diferencia_medias(datos, columna1, columna2, equal_var=True, alpha=0.05):

    res = st.ttest_ind(datos[columna1], datos[columna2], equal_var=equal_var)

    return res.confidence_interval(1 - alpha)

def intervalo_varianzas(datos, columna1, columna2, alpha=0.05):

    var1 = np.var(datos[columna1])
    var2 = np.var(datos[columna2])

    dof1 = len(datos[columna1]) - 1 
    dof2 = len(datos[columna2]) - 1

    F = st.f(dfn=dof1, dfd=dof2)

    fstat1 = F.ppf(alpha / 2)
    fstat2 = F.ppf(1 - (alpha / 2))

    int1 = fstat1 * (var1 / var2)
    int2 = fstat2 * (var1 / var2)
    
    return int1, int2
