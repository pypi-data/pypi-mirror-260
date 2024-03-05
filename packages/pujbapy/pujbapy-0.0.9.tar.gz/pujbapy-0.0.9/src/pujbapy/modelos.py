import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan

def regresion_lineal(datos, variable_y, variables_x, test_het=False, het=False):

  y = datos[variable_y]
  x = sm.add_constant(datos[variables_x])
  model = sm.OLS(y, x)
  reg = model.fit()
  

  if test_het:
    lm, plm, f, pf = het_breuschpagan(reg.resid, x)
    print(f"p valor: {pf}")
    if pf < 0.05:
      print('***' * 10)
      print("Existe evidencia de heterocedasticidad.")
      print('***' * 10)
      het = True
  if het:
    print(reg.get_robustcov_results().summary())
  else:
    print(reg.summary()) 

def regresion_logistica(datos, variable_y, variables_x, efectos_marginales=False):
  y = datos[variable_y]
  x = sm.add_constant(datos[variables_x])
  model = sm.Logit(y, x)
  reg = model.fit()
  print(reg.summary())

  if efectos_marginales:
    print("***" * 10)
    print("Efectos marginales")
    print("***" * 10)
    res = reg.get_margeff()
    print(res.summary())

def regresion_vi(datos, variable_y, endogena, variables_exog, mostrar_primera_etapa=False):

  y = datos[variable_y]
  # 1ra etapa
  endog = datos[endogena]
  exog = sm.add_constant(datos[variables_exog])
  model = sm.OLS(endog, exog)
  reg = model.fit()
  endog_adj = reg.fittedvalues

  if mostrar_primera_etapa:
    print('***' * 10)
    print('Primera etapa')
    print('***' * 10)
    print(reg.summary())

  # 2da etapa

  exog[f'{endogena}_fitted'] = reg.fittedvalues
  model = sm.OLS(y, exog)
  reg = model.fit()
  print(reg.summary())  




