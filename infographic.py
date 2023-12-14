import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

#12P

#eccentricity
ecc_12P = 0.954591
ecc_29P = 0.044321
#perihelion
peri_h_12P = 0.780784 #AU
peri_h_29P = 5.783492 #AU

R_sun = 696340E3 / 1.5E11 #AU
i_12P = 90 - 74.1911
i_29P = 9.3604
th_12P = np.radians(i_12P)
th_29P = np.radians(i_29P)

a_12P = peri_h_12P / (1 - ecc_12P)
b_12P = a_12P * np.sqrt(1 - ecc_12P**2)
a_29P = peri_h_29P / (1 - ecc_29P)
b_29P = a_29P * np.sqrt(1 - ecc_29P**2)

fp_12P = (a_12P) - peri_h_12P
fp_29P = (a_29P) - peri_h_29P

# (x**2/a**2) + (y**2/b**2) = 1

def ellipse(a, b, angle = 0, x_c = 0, y_c = 0):
    x = np.arange(-a, a, 0.00001)
    y_p = np.sqrt(y_c + b**2 - (((x)**2 * b**2) / a**2))
    y_n = -np.sqrt(y_c + b**2 - (((x)**2 * b**2) / a**2))
    f_x = x_c - np.sqrt(a**2 - b**2) * np.cos(angle)
    f_y = y_c - np.sqrt(a**2 - b**2) * np.sin(angle)
    return np.concatenate((x, x)), np.concatenate((y_p, y_n)), f_x, f_y

c_sun = ellipse(R_sun, R_sun)
Earth = ellipse(1, 1)
twlvP = ellipse(a_12P, b_12P, th_12P)
twntninP = ellipse(a_29P, b_29P, th_29P)
cent_x_12P = -fp_12P
cent_y_12P = 0
x_p_12P = (twlvP[0] - cent_x_12P)*np.cos(th_12P) - (twlvP[1] - cent_y_12P)*np.sin(th_12P) 
y_p_12P = (twlvP[0] - cent_x_12P)*np.sin(th_12P) + (twlvP[1] - cent_y_12P)*np.cos(th_12P)
cent_x_29P = -fp_29P
cent_y_29P = 0
x_p_29P = (twntninP[0] - cent_x_29P)*np.cos(th_29P) - (twntninP[1] - cent_y_29P)*np.sin(th_29P) 
y_p_29P = (twntninP[0] - cent_x_29P)*np.sin(th_29P) + (twntninP[1] - cent_y_29P)*np.cos(th_29P)

plt.figure(figsize=(5,5))
# plt.plot(twlvP[0], twlvP[1], 'kx', markersize=1, label='12P')
plt.plot(x_p_12P, y_p_12P, 'kx', markersize=1, label='12P')
plt.plot(x_p_29P, y_p_29P, 'rx', markersize=1, label='29P')
plt.plot(Earth[0], Earth[1], 'b-', label='Earth')
plt.axvline(0, color='black')
plt.axhline(0, color='black')
plt.plot(c_sun[0], c_sun[1], 'o', markersize=5, color='yellow', label='Sun')
plt.xlabel('Distance from the Sun in AU')
plt.ylabel('Distance from the Sun in AU')
plt.ylim(-7.5, 7.5)
plt.xlim(-7.5, 7.5)
plt.legend(loc='best')