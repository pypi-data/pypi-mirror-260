def anova_1way(): # one way anova with filters
    print("a1 = ols('X~Y',data=df).fit())  one_anova = sm.stats.anova_lm(a1,typ=1)\none_anova")
def anova_2way(): # two way anova with filter
    print("a1 = ols('X~Y+Z',data=df).fit())\ntwo_anova = sm.stats.anova_lm(a1,typ=2)\ntwo_anova")
def imports():# all imports required
    print("import numpy as np \nimport pandas as pd \nimport matplotlib.pyplot as plt\nimport statsmodels.stats.multicomp as mc\nfrom statsmodels.formula.api import ols\nfrom statsmodels.multivariate.manova import MANOVA\nimport statsmodels.api as sm\nimport scipy.stats as stats")
def multicomp(): # Multicomparison
    print("tuk = mc.MultiComparison(df['Balance'], df['Region'] + df['Married'] + df['Student'] + df['Own'])\n"
      "tuk1 = tuk.tukeyhsd()\n"
      "df1 = pd.DataFrame(tuk1.summary())\n"
      "df1 = df1.rename(columns=df1.iloc[0].astype(str)).drop(df1.index[0])\n"
      "df1['reject'] = df1['reject'].astype(str).to_list()\n"
      "df1[df1['reject'] == 'True']\n"
      "df1.head()")

def ttest(): # T-Testing
    print("stats.ttest_ind(list1,list2,equal_var=True,alternative='greater')")
    print("mu = 25\n"
      "n = len(a)\n"
      "df = n - 1\n"
      "xbar = np.mean(a)\n"
      "sd = stdev(a)\n"
      "se = sd / np.sqrt(n)\n"
      "tcal = (xbar - mu) / se\n"
      "print(tcal)\n"
      "alpha = 0.01 / 2\n"
      "ttableR = t.ppf(1 - alpha, df)\n"
      "ttableL = t.ppf(alpha, df)\n"
      "print(ttableL, '     ', ttableR)\n"
      "t.pdf(tcal, df)\n"
      "print(np.mean(a))\n"
      "print(mu + ttableL * se, '         ', mu + ttableR * se)\n"
      "stats.ttest_1samp(a, popmean=25, alternative='two-sided')")


def lab1():
    print("pdf=(1/np.sqrt(2*np.pi))*np.exp(-a1)")
    print("stats.norm.cdf(24,21,5)")
    print("stats.norm.ppf(0.9,1500,300)")

def lab2():
    print("from scipy import stats")
    print("pmf=stats.binom.pmf(k,n,p)")
    print("cdf= stats.binom.cdf(k,n,p)")
    print("pmf=stats.poisson.pmf(k,mean)")
    print("cdf=stats.poisson.cdf(k,mean)")
    print("binom=stats.binom.pmf(0,n,p)")

def lab3():
    print("y=[sepal,sepal_width,petal,petal_width]\np=[0,1]\ny1=[]\ndef log_lh(p,y):\n    mu=p[0]\n    sd=p[1]\n    lh=np.sum(np.log(norm.pdf(y[i],mu,sd)))\n   return -lh\ndef constrain(p):\nsd=p[1]\nreturn sd\na1=[]\nfor i in range (0,len(y)):\n cons = {'type':'ineq','fun':constrain}\na=minimize(log_lh,p,args=(y[i],),constraints=cons) \na1.append(a)\na1")

def random():
    print("x=np.random.uniform(0,0.99,100)")
def bernoulli():
    print("from scipy.optimize import minimize\nfrom scipy.stats import bernoulli")
    print("x0 = np.random.uniform(0, 0.99, 100)\n"
      "x0 = (x0 < 0.1) * 1\n"
      "x1 = np.random.uniform(0, 0.99, 100)\n"
      "x1 = (x1 < 0.2) * 1\n"
      "x2 = np.random.uniform(0, 0.99, 100)\n"
      "x2 = (x2 < 0.3) * 1\n"
      "x3 = np.random.uniform(0, 0.99, 100)\n"
      "x3 = (x3 < 0.9) * 1\n"

      "y = [x0, x1, x2, x3]\n"

      "p = [0.01]\n"
      "def log_lh(p, y):\n"
      "    lh = np.sum(np.log(p**y * (1 - p)**(1 - y)))\n"
      "    return -lh\n"

      "def constrain(p):\n"
      "    return p\n"

      "a1 = []\n"
      "for i in range(0, len(y)):\n"
      "    cons = {'type': 'ineq', 'fun': constrain}\n"
      "    a = minimize(log_lh, p, args=(y[i],), constraints=cons)\n"
      "    a1.append(a)\n"

      "a1\n"
      "df = pd.DataFrame(a1)\n"
      "print(df.iloc[:, 0])")
def ztest():
    print("from scipy.stats import norm \n"
        "Mu = 84\n"
      "sample_mean = 81.5\n"
      "population_sd = 10\n"
      "std_err = population_sd / np.sqrt(75)\n"
      "z_calc = (sample_mean - 84) / std_err\n"
      "z_calc\n"
      "ztable_r = norm.ppf(0.995, 0, 1)\n"
      "ztable_l = norm.ppf(0.005, 0, 1)\n"
      "print(ztable_r, ztable_l)")
def pandas():
    print("df = pd.read_csv('Iris.csv', index_col=5)\n"
      "df = pd.read_csv('Iris.csv', header=None)\n"
      "df = pd.read_csv('Iris.csv', skiprows=[0], header=None)")
def cv2():
    print("a = plt.imread('khush.jpeg')\n"
      "plt.imshow(a)\n"
      "a.shape\n"
      "plt.imshow(a[:, :, 0])")

def ztest_ind():
    print("# Return of HDFC bank is same as TCS\n"
      "# H0: mu(hdfc) = mu(tcs)\n"
      "# Ha: mu(hdfc) != mu(tcs)\n"
      "mu = 82\n"
      "Xbar_hdfc = 86\n"
      "Xbar_tcs = 82\n"
      "n_hdfc = 60\n"
      "n_tcs = 75\n"
      "sd_hdfc = 6\n"
      "sd_tcs = 9\n"
      "a = 0.01\n"
      "df = n_hdfc + n_tcs - 2\n"
      "se = np.sqrt((sd_hdfc**2) / n_hdfc + (sd_tcs**2) / n_tcs)\n"
      "zcal = ((Xbar_hdfc - Xbar_tcs) - 0) / se\n"
      "z_r = norm.ppf(1 - a/2, 0, 1)\n"
      "z_l = norm.ppf(a/2, 0, 1)\n"
      "t_r = t.ppf(1 - a/2, df)\n"
      "t_l = t.ppf(a/2, df)")


def anova():
    print("MST = TSS / ((num_a + num_b + num_c) - 1)\n"
      "MSB = Between / (2 - 1)\n"
      "MSW = within_total / (30 - 3)\n"
      "Fcalc = MSB / MSW\n"
      "critical_value = stats.t.ppf(1 - alpha, df2)\n"
      "tval = critical_value * (MSB / MSW) ** 0.5")


