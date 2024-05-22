import random
import json
import pandas as pd


def generate_dataset(path):
    num_items = 5
    num_customers = 100

    # Generate customer IDs and related information
    customer_ids = [id for id in range(1, num_customers + 1)]
    ages = [random.randint(18, 50) for _ in range(num_customers)]
    genders = ["male", "female"]

    # Generate unique product IDs for each category
    categories = ["Electronics", "Clothing", "Home & Kitchen", "Beauty"]
    unique_product_ids = {
        category: [f"{category[:3].upper()}{i:03d}" for i in range(1, num_items + 1)]
        for category in categories
    }

    # Read the dictionary from the JSON file
    with open("./dataset/product_description.json", "r") as json_file:
        product_description = json.load(json_file)

    # Generate purchase dates
    purchase_dates = [f"2023-01-{d:02d}" for d in range(1, 32)]
    random.shuffle(purchase_dates)
    purchase_dates *= (num_customers // len(purchase_dates)) + 1
    purchase_dates = purchase_dates[:num_customers]

    # Generate data
    data = []
    for customer_id in customer_ids:
        product_categories = random.choice(categories)
        product_id = random.choice(unique_product_ids[product_categories])
        # Access and print the product description
        for _, products in product_description.items():
            if product_id in products:
                product_desc = products[product_id]
                continue
        purchase_date = random.choice(purchase_dates)
        price = random.randint(20, 1000)
        ratings = round(random.uniform(3.5, 5.0), 1)
        page_views = random.randint(10, 50)
        time_spent = random.randint(60, 240)
        age = random.choice(ages)
        gender = random.choice(genders)
        data.append(
            [
                purchase_date,
                customer_id,
                product_id,
                product_desc,
                product_categories,
                price,
                ratings,
                page_views,
                time_spent,
                age,
                gender,
            ]
        )

    # Create DataFrame
    df = pd.DataFrame(
        data,
        columns=[
            "purchase_date",
            "customer_id",
            "product_id",
            "product_description",
            "category",
            "price",
            "ratings",
            "page_views",
            "time_spent",
            "age",
            "gender",
        ],
    )

    print(df.head())

    df.to_csv(path, index=False)


if __name__ == "__main__":
    path = "./dataset/dataset.csv"
    generate_dataset(path)
