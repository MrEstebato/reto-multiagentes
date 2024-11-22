import numpy as np
import pandas as pd

# Dimensiones de los racks
                      # X   |   Y   |   Z
Dim_rackS = np.array([195.5, 182.9, 60.96])
Dim_rackR = np.array([122.0, 160.0, 46.0])
Dim_rackC = np.array([213.61, 208.03, 80.01])

# Volumen de los racks
Vol_rackS = np.prod(Dim_rackS)
Vol_rackR = np.prod(Dim_rackR)
Vol_rackC = np.prod(Dim_rackC)

print('El volumen de los racks secos es: ', Vol_rackS/1000000, 'm^3')
print('El volumen de los racks refrigerados es: ', Vol_rackR/1000000, 'm^3')
print('El volumen de los congeladores es: ', Vol_rackC/1000000, 'm^3')

print('------------------------------------------------------')

Num_racksR = 4
Vol_total_racksR = Num_racksR * Vol_rackR
print('El volumen total de los racks refrigerados es: ', Vol_total_racksR/1000000, 'm^3')

print('------------------------------------------------------')

# Margen de seguridad (30%)
margen_seguridad = 1.3
Vol_camara = Vol_total_racksR * margen_seguridad

# Calculamos dimensiones considerando las proporciones de los racks
altura_camara = Dim_rackR[1] * 1.2  # 20% más alto que el rack
ancho_camara = (Dim_rackR[2] * 2) * 1.4  # Espacio para 2 racks lado a lado + 40% margen
largo_camara = (Dim_rackR[0] * 2) * 1.4  # Espacio para 2 racks en profundidad + 40% margen

print('------------------------------------------------------')
print('Dimensiones recomendadas para la cámara de refrigeración:')
print(f'Altura: {altura_camara/100:.2f} m')
print(f'Ancho: {ancho_camara/100:.2f} m')
print(f'Largo: {largo_camara/100:.2f} m')
print(f'Volumen de la cámara: {(altura_camara * ancho_camara * largo_camara)/1000000:.2f} m^3')