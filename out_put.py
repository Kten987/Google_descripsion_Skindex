import pandas as pd
from crawl import convert_productname, google_search
import time
import re

def input_product_name(source = "Thinh_Assignment.csv"):
    df = pd.read_csv(source).drop_duplicates()
    product_name_list = df["productName"].tolist()

    return product_name_list

list_output = []

def get_output(product_name_list):
    len_list = len(product_name_list)

    for product_name in product_name_list:
        count_product_processing = product_name_list.index(product_name) + 1
        if count_product_processing % 10 == 0:
            time.sleep(3)
            print(f"Done {product_name} -- estimated: {count_product_processing*100 /len_list}% -- products left: {len_list - count_product_processing}")
        # Clean product name, ex: The Auragins Glow Complexion Serum 14% Vitamin C ... -> The Auragins Glow Complexion Serum
        productName_clean = re.split("\d+\.\d+%|\d+%", product_name)[0].strip()

        productName_clean = convert_productname(productName_clean)

        try:
            output = google_search(productName_clean)
            list_output.append({"productName": product_name, "Google descriptions": output , "process": "Success"})

        except Exception as e:
            list_output.append({"productName": product_name, "Google descriptions": "", "process": "Error"})
            print(f"Error: {e} because of {product_name}")

    df_output = pd.DataFrame(list_output)
    return df_output


if __name__ == "__main__":
    product_name_list = input_product_name("Thinh_Assignment.csv")
    results = get_output(product_name_list)
    # Left join input and output vì input có duplicate
    in_put = pd.read_csv("Thinh_Assignment.csv")
    results = pd.merge(in_put["productName"], results, on="productName", how="left")
    results.to_csv("output_5.csv", index=False)