import pandas as pd


def VolCalc(Options):

    inputCsvName = Options.ListaCSV
    outputCsvName = Options.salidaCSV
    
    RackDimsC = [float(x) for x in Options.VRackC.split(":")]
    RackDimsR = [float(x) for x in Options.VRackR.split(":")]
    RackDimsS = [float(x) for x in Options.VRackS.split(":")]

    VolRackC = 1
    for DimC in RackDimsC:
        VolRackC *= DimC

    VolRackC_m3 = VolRackC / 1e+6

    VolRackR = 1
    for DimR in RackDimsR:
        VolRackR *= DimR

    VolRackR_m3 = VolRackR / 1e+6 

    VolRackS = 1
    for DimS in RackDimsS:
        VolRackS *= DimS

    VolRackS_m3 = VolRackS / 1e+6

    


    csv_file = pd.read_csv(inputCsvName, encoding="ISO-8859-1")
    dry_group = csv_file.groupby("Condicion").get_group("S")
    # print(dry_group["Volumen Adaptado"].sum())
    dry_total_volume_per_product = dry_group["Volumen (m^3)"].sum()
    dry_total_volume_per_average = dry_group["Volumen Adaptado"].sum()
    rack_members_mark_volume = 1.9
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

    r_cold_group = csv_file.groupby("Condicion").get_group("R")
    c_cold_group = csv_file.groupby("Condicion").get_group("C")

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

    racks = []
    rack_not_full = []
    rack_members_mark_volume = 1.9
    for i in range(len(dry_group)):
        prod_amount = dry_group["C. Maximo"].iloc[i]
        print(prod_amount)
        prod_name = dry_group["DESCRIPCION COMPLETA"].iloc[i]
        print(prod_name)
        _rack = rack_not_full
        _racksize = rack_members_mark_volume
        while prod_amount > 0:
            _racksize -= dry_group["Volumen (m^3)"].iloc[i]
            prod_amount -= 1
            _rack.append(prod_name)
            if _racksize <= 0:
                racks.append(_rack)
                _rack = []
                rack_not_full = []
                _racksize = rack_members_mark_volume
        if _rack:
            racks.append(_rack)
        rack_not_full = _rack

    data = []
    for rack_number, rack in enumerate(racks, start=1):
        product_counts = {}
        for product in rack:
            if product in product_counts:
                product_counts[product] += 1
            else:
                product_counts[product] = 1
        for product, quantity in product_counts.items():
            data.append({"Product": product, "Rack": rack_number, "Quantity": quantity})

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv("rack_inventory.csv", index=False)
