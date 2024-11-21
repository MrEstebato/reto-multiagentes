import pandas as pd
import time


def main():
    csv_file = pd.read_csv("Prod6.csv", encoding="ISO-8859-1")
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

    racks = {"S": [], "R": [], "C": []}
    current_rack = {"S": [], "R": [], "C": []}
    current_racksize = {"S": rack_capacity, "R": rack_capacity, "C": rack_capacity}

    for condition in ["S", "R", "C"]:
        condition_products = csv_file[csv_file["Condicion"] == condition]
        for _, row in condition_products.iterrows():
            prod_amount = int(row["C. Ajustado"])
            prod_name = row["DESCRIPCION COMPLETA"]
            volume_per_unit = float(row["Volumen Ajustado"])

            if volume_per_unit > rack_capacity:
                # Si el producto es muy grande para el rack
                print(f"El producto {prod_name} es muy grande para el rack")
                continue

            while prod_amount > 0:
                if current_racksize[condition] >= volume_per_unit:
                    current_rack[condition].append(prod_name)
                    current_racksize[condition] -= volume_per_unit
                    prod_amount -= 1
                    if current_racksize[condition] == 0:
                        racks[condition].append(current_rack[condition])
                        current_rack[condition] = []
                        current_racksize[condition] = rack_capacity
                else:
                    # Si el producto es muy grande para el rack, inicia uno nuevo.
                    if current_rack[condition]:
                        racks[condition].append(current_rack[condition])
                    current_rack[condition] = []
                    current_racksize[condition] = rack_capacity

        # Añade los productos restantes al rack
        if current_rack[condition]:
            racks[condition].append(current_rack[condition])
            current_rack[condition] = []
            current_racksize[condition] = rack_capacity

    data = []

    def process_racks(rack_list, prefix):
        for idx, rack in enumerate(rack_list, start=1):
            rack_name = f"{prefix}{idx}"
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
    df_output.to_csv("rack_inventory.csv", index=False)


if __name__ == "__main__":
    main()
