import json
import pandas as pd
import gradio as gr
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler


def calculate_rfm(df):
    # Current date
    current_date = df["purchase_date"].max() + pd.Timedelta(days=1)

    # RFM Calculation
    rfm = (
        df.groupby("customer_id")
        .agg(
            {
                "purchase_date": lambda x: (current_date - x.max()).days,
                "product_id": "count",
                "price": "sum",
            }
        )
        .rename(
            columns={
                "purchase_date": "recency",
                "product_id": "frequency",
                "price": "monetary",
            }
        )
        .reset_index()
    )

    return rfm


def preprocess_data(data):
    # Handle missing values
    data.fillna(0, inplace=True)

    # Encode categorical variables
    data_encoded = pd.get_dummies(data, columns=["gender"], prefix="encoded", dtype=int)

    # Scale numerical features
    scaler = MinMaxScaler()
    numerical_cols = ["ratings", "page_views", "time_spent", "age"]
    data_encoded[numerical_cols] = scaler.fit_transform(data_encoded[numerical_cols])

    return data_encoded


def compute_cosine_similarity(data):
    # Calculate RFM
    rfm = calculate_rfm(data)
    rfm_matrix = rfm[["recency", "frequency", "monetary"]]

    preprocessed_data = preprocess_data(data)

    # Combine preprocessed_data with RFM
    combined_data = pd.concat([preprocessed_data, rfm_matrix], axis=1)

    used_columns = [
        "ratings",
        "page_views",
        "time_spent",
        "age",
        "encoded_female",
        "encoded_male",
        "recency",
        "frequency",
        "monetary",
    ]

    cosine_sim = cosine_similarity(combined_data[used_columns])
    cosine_sim_df = pd.DataFrame(
        cosine_sim, index=rfm["customer_id"], columns=rfm["customer_id"]
    )
    return cosine_sim_df


def get_recommendations(customer_id, top_n=3):

    df = pd.read_csv("./dataset/dataset.csv")
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])

    # Compute Cosine Similarity
    cosine_sim_df = compute_cosine_similarity(df)

    similar_customers = (
        cosine_sim_df[customer_id].sort_values(ascending=False).index[1:]
    )

    recommended_products = []
    for similar_customer in similar_customers[: top_n + 1]:
        products = df[df["customer_id"] == similar_customer]["product_id"].values
        recommended_products.extend(products)

    recommended_products = list(
        set(recommended_products)
        - set(df[df["customer_id"] == customer_id]["product_id"].values)
    )

    # Read the dictionary from the JSON file
    with open("./dataset/product_description.json", "r") as json_file:
        product_description = json.load(json_file)

    # Result list to store dictionaries
    result_list = []

    for product_id in recommended_products:
        for category, products in product_description.items():
            if product_id in products:
                result_dict = {
                    "product id": product_id,
                    "product categories": category,
                    "product description": products[product_id],
                }
                result_list.append(result_dict)
                break

    result_df = pd.DataFrame(result_list)

    return result_df


inputs = [
    gr.Number(
        value=67, label="Customer ID", minimum=1, maximum=100, precision=0, step=1
    ),
    gr.Dropdown(
        value=3,
        choices=[3, 4, 5],
        label="Number of recommendation products",
    ),
]

outputs = gr.Dataframe(label="Recommended Products", datatype=["str", "str", "str"])

demo = gr.Interface(
    fn=get_recommendations,
    inputs=inputs,
    outputs=outputs,
    title="Simple Product Recommendation System",
    description="Get product recommendations based on customer similarity.",
    allow_flagging="never",
)

if __name__ == "__main__":
    demo.launch()
