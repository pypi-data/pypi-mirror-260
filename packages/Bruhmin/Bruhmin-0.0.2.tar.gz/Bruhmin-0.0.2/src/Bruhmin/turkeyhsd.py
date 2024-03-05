def prin_ols_1way():
    print("a1 = ols('X~Y',data=df).fit())  print(sm.stats.anova_lm(a1,typ=1)")
def prin_ols_2way():
    print("a1 = ols('X~Y+Z',data=df).fit())  print(sm.stats.anova_lm(a1,typ=2)")
    
