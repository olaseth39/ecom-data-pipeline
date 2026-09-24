WITH source_data AS (
    SELECT * FROM {{ ref('stg_products') }}
)
SELECT 
    product_id,
    TRIM(product_title) AS product_title,
    CAST(price AS FLOAT) AS price,
    TRIM(category) AS category,
    description,
    image_url
FROM source_data