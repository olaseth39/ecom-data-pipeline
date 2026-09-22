SELECT 
    id AS product_id,
    title AS product_title,
    price,
    category,
    description,
    image AS image_url  -- Changed from image_url to image
FROM ECOM_DB.RAW.PRODUCTS_RAW