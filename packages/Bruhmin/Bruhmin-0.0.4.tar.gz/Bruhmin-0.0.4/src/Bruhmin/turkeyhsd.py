def anova_1way(): # one way anova with filters
    print("a1 = ols('X~Y',data=df).fit())  one_anova = sm.stats.anova_lm(a1,typ=1)\none_anova")
def anova_2way(): # two way anova with filter
    print("a1 = ols('X~Y+Z',data=df).fit())\ntwo_anova = sm.stats.anova_lm(a1,typ=2)\ntwo_anova")
def imports():# all imports required
    print("import numpy as np \nimport pandas as pd \nimport matplotlib.pyplot as plt\nimport statsmodels.stats.multicomp as mc\nfrom statsmodels.formula.api import ols\nfrom statsmodels.multivariate.manova import MANOVA\nimport statsmodels.api as sm\nimport scipy.stats as stats")
def multicomp(): # Multicomparison
    print("tukey = mc.MultiComparison(df['Target'],df['Var1']+df['Var2'])\ntukey = tukey.tukeyhsd()\ntukey.summary()")
def ttest(): # T-Testing
    print("stats.ttest_ind(list1,list2,equal_var=True,alternative='greater')")