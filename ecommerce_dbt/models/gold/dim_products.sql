WITH cleaned_data AS (
    SELECT * FROM {{ ref('int_products_cleaned') }}
)
SELECT 
    product_id,
    product_title,
    price,
    category
FROM cleaned_data