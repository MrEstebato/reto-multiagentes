import pandas as pd

def main():
    csv_file = pd.read_csv("Productos.csv")
    dry_group = csv_file.groupby("Condicion").get_group("S")
    #print(dry_group["Volumen Promedio"].sum())
    dry_total_volume_per_product = dry_group["Volumen (m^3)"].sum()
    dry_total_volume_per_average = dry_group["Volumen Promedio"].sum()
    rack_members_mark_volume = 2.18
    rack_uline_volume = 0.90
    print(f"El volumen total de los productos secos es \n---------------------------------------\n {dry_total_volume_per_product} m^3 \n")
    print(f"Considerando el consumo promedio por producto el volumen necesario seria: \n---------------------------------------\n {dry_total_volume_per_average} m^3 \n")
    print(f"Por lo tanto considerando los volumenes \n Rack Members Mark: {rack_members_mark_volume} m^3\n Rack Uline: {rack_uline_volume} m^3 \n ---------------------")
    print(f"Se necesitarian: \n ------------------------------------\n {dry_total_volume_per_average/rack_members_mark_volume} Racks Member Mark \n {dry_total_volume_per_average/rack_uline_volume} Racks Uline \n")

    print(10*"\n")

    r_cold_group = csv_file.groupby("Condicion").get_group("R")
    c_cold_group = csv_file.groupby("Condicion").get_group("C")


    #print(dry_group["Volumen Promedio"].sum())
    cold_total_volume_per_product = r_cold_group["Volumen (m^3)"].sum() + c_cold_group["Volumen (m^3)"].sum()
    cold_total_volume_per_average = r_cold_group["Volumen Promedio"].sum() + c_cold_group["Volumen Promedio"].sum()
    rack_members_mark_volume = 2.18
    rack_uline_volume = 0.90
    print(f"El volumen total de los productos refrigerados y congelados es \n---------------------------------------\n {cold_total_volume_per_product} m^3 \n")
    print(f"Considerando el consumo promedio por producto el volumen necesario seria: \n---------------------------------------\n {cold_total_volume_per_average} m^3 \n")
    print(f"Por lo tanto considerando los volumenes \n Rack Members Mark: {rack_members_mark_volume} m^3\n Rack Uline: {rack_uline_volume} m^3 \n ---------------------")
    print(f"Se necesitarian: \n ------------------------------------\n {cold_total_volume_per_average/rack_members_mark_volume} Racks Member Mark \n {cold_total_volume_per_average/rack_uline_volume} Racks Uline \n")


if __name__ == "__main__":
    main()