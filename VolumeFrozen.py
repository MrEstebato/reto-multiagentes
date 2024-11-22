import pandas as pd
    
archivo = pd.read_csv('volCalculado.csv')
productos = pd.read_csv('Prod6.csv')

productos_congelados = archivo[archivo['Rack'].isin(['C1', 'C2'])]
print(productos_congelados)

print('------------------------------------------------------')

# Dimensiones y cantidades productos congelados
dimensiones_congelados = productos[productos['PRODUCTO'].str.strip().isin([
    'MARQUETA ALITAS',
    'PAPAS A LA FRANCESAS',
    'BONELESS'
])][['PRODUCTO', 'Altura', 'Largo', 'Ancho']]

dimensiones_congelados['PRODUCTO'] = dimensiones_congelados['PRODUCTO'].str.strip()

print(dimensiones_congelados)

print('------------------------------------------------------')

cantidades = productos_congelados[['Product', 'Quantity']].copy()
cantidades['Product'] = cantidades['Product'].replace('PAPAS MCCAIN', 'PAPAS A LA FRANCESAS')

cantidades = cantidades.rename(columns={
    'Product': 'PRODUCTO',
    'Quantity': 'Cantidad'
})

dimensiones_congelados = dimensiones_congelados.merge(cantidades, on='PRODUCTO', how='left')

# Volumen individual
dimensiones_congelados['Volumen_cm3'] = (
    dimensiones_congelados['Altura'] * 
    dimensiones_congelados['Largo'] * 
    dimensiones_congelados['Ancho']
)

# Volumen total por producto
dimensiones_congelados['Volumen_total_cm3'] = dimensiones_congelados['Volumen_cm3'] * dimensiones_congelados['Cantidad']
dimensiones_congelados['Volumen_total_m3'] = dimensiones_congelados['Volumen_total_cm3'] / 1000000

print('\nVolumen total por producto en metros cúbicos:')
print(dimensiones_congelados[['PRODUCTO', 'Cantidad', 'Volumen_total_m3']])

print('------------------------------------------------------')

volumen_total = dimensiones_congelados['Volumen_total_m3'].sum()
print('\nVolumen total de todos los productos en metros cúbicos:')
print(volumen_total, 'm^3')
