import numpy as np
import matplotlib.pyplot as plt

# Required inputs, airfoil number and chord length
airfoil = 4420
c = 1

m = (airfoil // 1000) / 100 * 1.0
p = ((airfoil // 100) % 10) / 10 * 1.0
t = airfoil % 100 / 100 * 1.0

x = np.linspace(0, c, 100)

yt = 5 * t * (0.2969 * np.sqrt(x / c) - 0.126 * (x / c) - 0.3516 *
              (x / c)**2 + 0.2843 * (x / c)**3 - 0.1015 * (x / c)**4)

yc = np.piecewise(x, [x <= p * c, x > p * c], [
    lambda x: m / p**2 * (2 * p * (x / c) - (x / c)**2), lambda x: m /
    (1 - p)**2 * ((1 - 2 * p) + 2 * p * (x / c) - (x / c)**2)
])

dyc = np.piecewise(x, [x <= p * c, x > p * c], [
    lambda x: 2 * m / p**2 * (p - (x / c)), lambda x: 2 * m / (1 - p)**2 *
    (p - (x / c))
])

theta = np.arctan(dyc)

xu = x - yt * np.sin(theta)
xl = x + yt * np.sin(theta)

yu = yc + yt * np.cos(theta)
yl = yc - yt * np.cos(theta)

plt.plot(xu, yu, 'b-')
plt.plot(xl, yl, 'b-')
plt.plot(x, yc, 'k--')
plt.xlim(0, c)
plt.ylim(-c, c)
plt.title('NACA ' + str(airfoil) + ' Airfoil')
plt.grid()
plt.xlabel("x/c")
plt.ylabel("t/c")
plt.savefig("AirfoilShape.png")
plt.show()
