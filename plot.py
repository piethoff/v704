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


plt.errorbar(gamma_pb[2], gamma_pb[0], yerr = gamma_pb[1], elinewidth=0.7, capthick=0.7, capsize=3, fmt=".", color="xkcd:blue", label="Messwerte für Bleiabschirmung")
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


plt.errorbar(gamma_zn[2], gamma_zn[0], yerr = gamma_zn[1], elinewidth=0.7, capthick=0.7, capsize=3, fmt=".", color="xkcd:blue", label="Messwerte für Zinkabschirmung")
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
##beta[0] = beta[2]
##beta[2] = beta[1]
##beta[1] = beta[3]

print(beta_null)
print(beta)

d_n = np.sqrt(beta_null[1])
d_b = np.sqrt(beta[1])

d_n/= beta_null[0]
d_b/= beta[0]

beta[0] = beta[1]/beta[0] - beta_null[1]/beta_null[0]
beta[1] = np.sqrt( d_b**2 + d_n**2 )
print(beta)

## dn = sqrt(n)
## dc = sqrt(c)
## d(c/t) = sqrt(c)/t
## d(n/t') = sqrt(n)/t'
## C = c/t - n/t'
## dC = sqrt( (d(c/t))² + (d(n/t'))² )
## dC = sqrt( c/t² + n/t'² )

pivot = 6

##params, covar = curve_fit(exp, beta[2][:pivot], beta[0][:pivot], absolute_sigma=True, sigma = beta[1][:pivot])
##uparams = unumpy.uarray(params, np.sqrt(np.diag(covar)))
##print("Parameter m und n(=e^A) für Aluminiumabschirmung: ")
##print(uparams)


plt.errorbar(beta[2], beta[0], yerr = beta[1], elinewidth=0.7, capthick=0.7, capsize=3, fmt=".", color="xkcd:blue", label="Messwerte für Aluminiumabschirmung")

#plt.plot(gamma_zn[2], exp(gamma_zn[2], *params), color="xkcd:orange", label="lin. Fit")
#plt.plot(gamma_zn[2], exp(gamma_zn[2], *params), color="xkcd:orange", label="lin. Fit")

plt.yscale("log")
plt.xlabel(r"R$/\si{\kg\per\meter\squared}$")
plt.ylabel(r"Aktivität$/\si{\becquerel}$")
plt.legend()
plt.tight_layout()
plt.grid(which="both")
plt.savefig("build/beta.pdf")
plt.clf()
