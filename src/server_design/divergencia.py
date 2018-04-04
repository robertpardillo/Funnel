
import matplotlib.pyplot as plt
import numpy as np

incre_phi = list()
incre_phi_val = 0
iteracion = list()
for i in range(500):
    iteracion.append(i)
    incre_phi_val += 0.01
    incre_phi.append(2**incre_phi_val*np.sin(2*np.pi*i/25+np.pi/2))
plt.figure()
plt.plot(iteracion, incre_phi)

plt.show()

incre_phi = list()
iteracion = list()
for i in range(500):
    iteracion.append(i)
    incre_phi_val = 4*np.sin(2*np.pi*i/25)
    incre_phi.append(incre_phi_val)

plt.figure()
plt.plot(iteracion, incre_phi)
plt.savefig('imprecision.pdf',format='pdf')
plt.show()

incre_phi = list()
iteracion = list()
incre_phi_val = 0
for i in range(500):
    iteracion.append(i)
    incre_phi_val += 0.1
    incre_phi.append((1/(incre_phi_val**0.2+incre_phi_val))*np.sin(2 * np.pi * i / 25 +np.pi/2))

plt.figure()
plt.plot(iteracion, incre_phi)
plt.savefig('convergencia.pdf',format='pdf')
plt.show()