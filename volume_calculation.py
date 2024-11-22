import pandas as pd
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from Packers import SimplePacker, AdvancedPacker
from Node import Rect
from binpacking import sort, plot, draw_rect, sort_types
import sys


def calculate_volume(Options):

    inputCsvName = Options.ListaCSV
    outputCsvName = Options.salidaCSV

    RackDimsC = [float(x) for x in Options.VRackC.split(":")]
    RackDimsR = [float(x) for x in Options.VRackR.split(":")]
    RackDimsS = [float(x) for x in Options.VRackS.split(":")]

    VolRackC = 1
    for DimC in RackDimsC:
        VolRackC *= DimC

    VolRackC_m3 = VolRackC / 1e6

    VolRackR = 1
    for DimR in RackDimsR:
        VolRackR *= DimR

    VolRackR_m3 = VolRackR / 1e6

    VolRackS = 1
    for DimS in RackDimsS:
        VolRackS *= DimS

    VolRackS_m3 = VolRackS / 1e6

    csv_file = pd.read_csv(inputCsvName, encoding="ISO-8859-1")
    dry_group = csv_file.groupby("Condicion").get_group("S")
    r_cold_group = csv_file.groupby("Condicion").get_group("R")
    c_cold_group = csv_file.groupby("Condicion").get_group("C")

    # print(dry_group["Volumen Adaptado"].sum())
    dry_total_volume_per_product = dry_group["Volumen (m^3)"].sum()
    dry_total_volume_per_average = dry_group["Volumen Adaptado"].sum()
    rack_members_mark_volume = 1.9
    rack_capacity = rack_members_mark_volume  # Modificar si se desea cambiar el tamaño de los racks para congelados y refrigerados
    rack_uline_volume = 0.90
    print(
        f"El volumen total de los productos secos es \n---------------------------------------\n {dry_total_volume_per_product} m^3 \n"
    )
    print(
        f"Considerando el consumo promedio por producto el volumen necesario seria: \n---------------------------------------\n {dry_total_volume_per_average} m^3 \n"
    )
    print(
        f"Por lo tanto considerando los volumenes \n Rack Members Mark: {rack_members_mark_volume} m^3\n Rack Uline: {rack_uline_volume} m^3 \n ---------------------"
    )
    print(
        f"Se necesitarian: \n ------------------------------------\n {dry_total_volume_per_average/rack_members_mark_volume} Racks Member Mark \n"
    )

    print(10 * "\n")

    # print(dry_group["Volumen Adaptado"].sum())
    cold_total_volume_per_product = (
        r_cold_group["Volumen (m^3)"].sum() + c_cold_group["Volumen (m^3)"].sum()
    )
    cold_total_volume_per_average = (
        r_cold_group["Volumen Adaptado"].sum() + c_cold_group["Volumen Adaptado"].sum()
    )
    cold_total_volume_per_product *= 1.1
    cold_total_volume_per_average *= 1.1
    rack_members_mark_volume = 2.18
    rack_uline_volume = 0.90
    print(
        f"El volumen total de los productos refrigerados y congelados es \n---------------------------------------\n {cold_total_volume_per_product} m^3 \n"
    )
    print(
        f"Considerando el consumo promedio por producto el volumen necesario seria: \n---------------------------------------\n {cold_total_volume_per_average} m^3 \n"
    )
    print(
        f"Por lo tanto considerando los volumenes \n Rack Members Mark: {rack_members_mark_volume} m^3\n Rack Uline: {rack_uline_volume} m^3 \n ---------------------"
    )
    print(
        f"Se necesitarian: \n ------------------------------------\n {cold_total_volume_per_average/rack_uline_volume} Racks Uline \n"
    )

    print(dry_group)

    rack_capacity = {"S": VolRackS_m3, "R": VolRackR_m3, "C": VolRackC_m3}
    racks = {"S": [], "R": [], "C": []}
    current_rack = {"S": [], "R": [], "C": []}
    current_racksize = {"S": 0, "R": 0, "C": 0}

    racks_dimension = []
    current_rack_dimensions = []

    for condition in ["S", "R", "C"]:
        total_rack_capacity = rack_capacity[condition]
        condition_products = csv_file[csv_file["Condicion"] == condition]
        for _, row in condition_products.iterrows():
            prod_amount = int(row["C. Ajustado"])
            prod_name = row["DESCRIPCION COMPLETA"]
            volume_per_unit = float(row["Volumen Ajustado"])
            current_dimensions = (float(row["Altura"]/100), float(row['Ancho']/100))

            if volume_per_unit > total_rack_capacity:
                print(
                    f"El producto {prod_name} es muy grande para el rack de tipo {condition}"
                )
                continue

            while prod_amount > 0:
                remaining_capacity = total_rack_capacity - current_racksize[condition]
                if remaining_capacity >= volume_per_unit:
                    current_rack[condition].append(prod_name)
                    current_racksize[condition] += volume_per_unit
                    prod_amount -= 1
                    if (condition == "S"):
                        current_rack_dimensions.append(current_dimensions)
                else:
                    # Rack is full, save it and start a new rack
                    racks[condition].append(current_rack[condition])
                    current_rack[condition] = []
                    current_racksize[condition] = 0
                    
                    if (condition == "S"):
                        racks_dimension.append(current_rack_dimensions)
                        current_dimensions = (0, 0)
                        current_rack_dimensions = []

            # After processing all items, check if the current rack has items
        if current_rack[condition]:
            racks[condition].append(current_rack[condition])
            current_rack[condition] = []
            current_racksize[condition] = 0
            
            if (condition == "S"):
                racks_dimension.append(current_rack_dimensions)
                current_rack_dimensions = []
                current_dimensions = (0, 0)

    # Prepare data for CSV
    data = []
    print(racks_dimension)

    def process_racks(rack_list, condition):
        for idx, rack in enumerate(rack_list, start=1):
            rack_name = f"{condition}{idx}"
            product_counts = {}
            for product in rack:
                product_counts[product] = product_counts.get(product, 0) + 1
            for product, quantity in product_counts.items():
                data.append(
                    {"Product": product, "Rack": rack_name, "Quantity": quantity}
                )

    # Process racks for each condition
    process_racks(racks["S"], "S")
    process_racks(racks["R"], "R")
    process_racks(racks["C"], "C")

    # Create DataFrame and save to CSV
    df_output = pd.DataFrame(data)
    df_output.to_csv(outputCsvName, index=False)

    size = (1.22, 1.60)
    
    for i in range(len(racks_dimension)):
    #rects = [Rect(d) for d in dims]
        new_rects = [Rect(d) for d in racks_dimension[i]]

        print(new_rects)

        sys.setrecursionlimit(20000)
        p = SimplePacker(*size)
        #p = AdvancedPacker(*size)
    
        new_rects = p.fit(new_rects)
        print(new_rects)
        plot(1.22, 1.6, new_rects)


if __name__ == "__main__":
    calculate_volume()
    
