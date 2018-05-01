import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.optimize import curve_fit
from uncertainties import unumpy

mpl.use('pgf')
mpl.rcParams.update({
    'pgf.preamble': r'\usepackage{siunitx}',
})

def exp(x, m, n):
    return np.exp(m*x + n)



gamma_null = np.genfromtxt("content/gamma_null.txt", unpack=True)
gamma_pb = np.genfromtxt("content/gamma_pb.txt", unpack=True)
gamma_zn = np.genfromtxt("content/gamma_zn.txt", unpack=True)

gamma_pb[2] *= 10
gamma_zn[2] *= 2


d_n = np.sqrt(gamma_null[1])
d_pb = np.sqrt(gamma_pb[1])
d_zn = np.sqrt(gamma_zn[1])

d_n/= gamma_null[0]
d_pb/= gamma_pb[0]
d_zn/= gamma_zn[0]

gamma_pb[0] = gamma_pb[1]/gamma_pb[0] - gamma_null[1]/gamma_null[0]
gamma_pb[1] = np.sqrt( d_pb**2 + d_n**2 )

gamma_zn[0] = gamma_zn[1]/gamma_zn[0] - gamma_null[1]/gamma_null[0]
gamma_zn[1] = np.sqrt( d_zn**2 + d_n**2 )

#for i in range(gamma_pb[0].size):
#    print(gamma_pb[:,i])
#for i in range(gamma_zn[0].size):
#    print(gamma_zn[:,i])


## dn = sqrt(n)
## dc = sqrt(c)
## d(c/t) = sqrt(c)/t
## d(n/t') = sqrt(n)/t'
## C = c/t - n/t'
## dC = sqrt( (d(c/t))² + (d(n/t'))² )
## dC = sqrt( c/t² + n/t'² )

## f(x) = x - y
## gauß: sqrt(dx² + dy²)
## dx = sqrt(x)
## sqrt(sqrt(x)² + sqrt(y)²)

params, covar = curve_fit(exp, gamma_pb[2], gamma_pb[0], absolute_sigma=True, sigma = gamma_pb[1])
uparams = unumpy.uarray(params, np.sqrt(np.diag(covar)))
print("Parameter m und n(=e^A) für Bleiabschirmung: ")
print(uparams)


plt.errorbar(gamma_pb[2], gamma_pb[0], yerr = gamma_pb[1], elinewidth=0.7, capthick=0.7, capsize=3, fmt=".", color="xkcd:blue", label="Messwerte für Pb-Abschirmung")
plt.plot(gamma_pb[2], exp(gamma_pb[2], *params), color="xkcd:orange", label="lin. Fit")
plt.yscale("log")
plt.xlabel(r"Dicke$/\si{\milli\meter}$")
plt.ylabel(r"Aktivität$/\si{\becquerel}$")
plt.legend()
plt.tight_layout()
plt.grid(which="both")
plt.savefig("build/gamma_pb.pdf")
plt.clf()

#####

params, covar = curve_fit(exp, gamma_zn[2], gamma_zn[0], absolute_sigma=True, sigma = gamma_zn[1])
uparams = unumpy.uarray(params, np.sqrt(np.diag(covar)))
print("Parameter m und n(=e^A) für Zinkabschirmung: ")
print(uparams)


plt.errorbar(gamma_zn[2], gamma_zn[0], yerr = gamma_zn[1], elinewidth=0.7, capthick=0.7, capsize=3, fmt=".", color="xkcd:blue", label="Messwerte für Zn-Abschirmung")
plt.plot(gamma_zn[2], exp(gamma_zn[2], *params), color="xkcd:orange", label="lin. Fit")
plt.yscale("log")
plt.xlabel(r"Dicke$/\si{\milli\meter}$")
plt.ylabel(r"Aktivität$/\si{\becquerel}$")
plt.legend()
plt.tight_layout()
plt.grid(which="both")
plt.savefig("build/gamma_zn.pdf")
plt.clf()

#####


beta_null = np.genfromtxt("content/beta_null.txt", unpack=True)
beta = np.genfromtxt("content/beta.txt", unpack=True)
beta[1] = beta[3]
beta[3] = beta[2]
beta[2] = beta[0]
beta[0] = beta[3]

#print(beta_null)
print(beta)

d_n = np.sqrt(beta_null[1])
d_b = np.sqrt(beta[1])

d_n/= beta_null[0]
d_b/= beta[0]

beta[0] = beta[1]/beta[0] - beta_null[1]/beta_null[0]
beta[1] = np.sqrt( d_b**2 + d_n**2 )

#for i in range(beta[0].size):
#    if(beta[0][i]-beta[1][i] < 0):
#        beta[1][i] = beta[0][i] * 0.1
#beta[0] += 0.1
#for i in range(beta[0].size):
#    print(beta[:,i])

#µm * 2.7 g/cm³ = cm/10.000 * 2.7 * g / cm³
#2.7*g/cm² = 10000µm*2.7*g/cm³

beta[2]*=2.7/10000

## dn = sqrt(n)
## dc = sqrt(c)
## d(c/t) = sqrt(c)/t
## d(n/t') = sqrt(n)/t'
## C = c/t - n/t'
## dC = sqrt( (d(c/t))² + (d(n/t'))² )
## dC = sqrt( c/t² + n/t'² )

pivot = 6
pivot2 = 3

params, covar = curve_fit(exp, beta[2,:pivot2], beta[0,:pivot2], absolute_sigma=True, sigma = beta[1,:pivot2], p0=(10,0))
uparams = unumpy.uarray(params, np.sqrt(np.diag(covar)))
print("Parameter m und n(=e^A) für Aluminiumabschirmung: ")
print(uparams)


plt.errorbar(beta[2], beta[0], yerr = beta[1], elinewidth=0.7, capthick=0.7, capsize=3, fmt=".", color="xkcd:blue", label="Messwerte für Al-Abschirmung")

plt.plot(beta[2], exp(beta[2], *params), color="xkcd:blue", label="linearer Fit 1")

params, covar = curve_fit(exp, beta[2,pivot:], beta[0,pivot:], absolute_sigma=True, sigma = beta[1,pivot:], p0=(-100,3))
uparams = unumpy.uarray(params, np.sqrt(np.diag(covar)))
print("Parameter m und n(=e^A) für Aluminiumabschirmung: ")
print(uparams)

plt.plot(beta[2], exp(beta[2], *params), color="xkcd:orange", label="linearer Fit 2")

plt.yscale("log")
plt.xlabel(r"R$/\si{\gram\per\centi\meter\squared}$")
plt.ylabel(r"Aktivität$/\si{\becquerel}$")
plt.legend()
plt.tight_layout()
plt.grid(which="both")
plt.savefig("build/beta.pdf")
plt.clf()
