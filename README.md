## SKLVL PRODUCT RECOMMENDATION

## INSTALLATIONS
- #### Install requirement library
    ```bash
    pip install -r requirements.txt
    ```

## USAGE
- #### Generate Dataset
    ```bash
    python generate_dataset.py
    ```
    This script will create dataset like this. Stored in `./dataset` folder.

| purchase_date | customer_id | product_id | product_description                          | category        | price | ratings | page_views | time_spent | age | gender |
|---------------|-------------|------------|----------------------------------------------|-----------------|-------|---------|------------|------------|-----|--------|
| 2023-01-28    | 1           | ELE004     | SmartTech 4K Ultra HD TV                     | Electronics     | 556   | 4.6     | 14         | 163        | 25  | female |
| 2023-01-28    | 2           | HOM002     | Gourmet Chef Stainless Steel Cookware Set    | Home & Kitchen  | 143   | 3.6     | 10         | 87         | 49  | male   |
| 2023-01-20    | 3           | BEA003     | GlowBeauty Vitamin C Serum                   | Beauty          | 219   | 4.6     | 42         | 117        | 19  | male   |
| 2023-01-18    | 4           | ELE002     | PowerPulse Wireless Earbuds                  | Electronics     | 395   | 4.9     | 49         | 70         | 30  | male   |
| 2023-01-10    | 5           | BEA001     | RadiantSkin Anti-Aging Cream                 | Beauty          | 924   | 4.7     | 22         | 173        | 50  | female |

## PRODUCT RECOMMENDATION APPROACH 

- #### Collaborative Filtering (Cosine Similarity)

    Collaborative filtering is a method used by recommendation systems to predict the preferences of a user by collecting preferences from many users. The underlying assumption is that if a user A has the same opinion as user B on one issue, A is more likely to have B's opinion on a different issue than that of a randomly chosen user.

- #### Cosine Similarity

    Cosine similarity is a metric used to measure how similar two items or users are. It is calculated by finding the cosine of the angle between two non-zero vectors in a multi-dimensional space. The cosine similarity between two vectors A and B is given by:

    ![Cosine Similarity](/assets/cosine_similarity_equation.jpg)

    Where:
    - \( A \cdot B \) is the dot product of vectors A and B.
    - \( \|A\| \) is the magnitude of vector A.
    - \( \|B\| \) is the magnitude of vector B.

- #### Steps to Implement Collaborative Filtering with Cosine Similarity

    1. **Create User-Item Matrix**: Construct a matrix where each row represents a user, each column represents an item, and each cell represents the rating given by a user to an item.

    2. **Compute Cosine Similarity**: Calculate the cosine similarity between the user vectors or item vectors to measure their similarity.

    3. **Generate Recommendations**:
        - For user-based filtering, recommend items that similar users have liked.
        - For item-based filtering, recommend items that are similar to items the user has liked.

- #### Example

    Consider the following user-item matrix:

    | User/Item | Item1 | Item2 | Item3 | Item4 |
    |-----------|-------|-------|-------|-------|
    | User1     | 4     | 0     | 3     | 5     |
    | User2     | 5     | 1     | 0     | 4     |
    | User3     | 3     | 2     | 5     | 0     |

    To compute the cosine similarity between User1 and User2:

    1. **User1 Vector**: [4, 0, 3, 5]
    2. **User2 Vector**: [5, 1, 0, 4]

    Cosine similarity calculation:

    ```
    cosine_similarity(User1, User2) = (4*5 + 0*1 + 3*0 + 5*4) / (sqrt(4^2 + 0^2 + 3^2 + 5^2) * sqrt(5^2 + 1^2 + 0^2 + 4^2))
    ```

    ```
    cosine_similarity(User1, User2) = (20 + 0 + 0 + 20) / (sqrt(16 + 0 + 9 + 25) * sqrt(25 + 1 + 0 + 16))
    ```

    ```
    cosine_similarity(User1, User2) = 40 / (sqrt(50) * sqrt(42))
    ```

    ```
    cosine_similarity(User1, User2) = 40 / sqrt(2100) ≈ 40 / 45.83 ≈ 0.872
    ```

    A high cosine similarity (close to 1) indicates that User1 and User2 have similar preferences.

## INFERENCE
- #### WEB APP USAGE
    ```bash
    gradio app.py
    ```
- #### GRADIO WEB APP
    [APP](https://mghazalli-simple-product-recommendation.hf.space "Web App")