import pandas as pd


def getVolumenCongelados():
    # Read the existing CSV file where racks and products are listed
    archivo = pd.read_csv("volCalculado.csv")

    # Read the product data
    productos = pd.read_csv("Prod7.csv")

    # Filter frozen products (Condicion 'C')
    frozen_products = productos[productos["Condicion"].str.strip() == "C"]

    # Prepare the frozen products data
    # Assume 'DESCRIPCION COMPLETA' is the product name and 'C. Ajustado' is the quantity
    frozen_products = frozen_products[["DESCRIPCION COMPLETA", "C. Ajustado"]].copy()
    frozen_products.rename(
        columns={"DESCRIPCION COMPLETA": "Product", "C. Ajustado": "Quantity"},
        inplace=True,
    )

    # Assign all frozen products to rack 'C1'
    frozen_products["Rack"] = "C1"

    # Rearrange columns to match the existing CSV
    frozen_products = frozen_products[["Product", "Rack", "Quantity"]]

    # Combine the DataFrames using pd.concat
    archivo = pd.concat([archivo, frozen_products], ignore_index=True)

    # Save the updated CSV
    archivo.to_csv("volCalculado.csv", index=False)

    print("Frozen products have been added to 'volCalculado.csv' with Rack 'C1'.")


# Run the function
getVolumenCongelados()
