ArtD Shopify
============
ArtD Shopify is a package that connects with a store developed in Shopify and extracts products, their variants, prices, stock and images and other data.
---------------------------------------------------------------------------------------------------------------------------------------------------------
1. Add to your INSTALLED_APPS setting like this:
``INSTALLED_APPS = [
        ...
        'django-json-widget'
        'artd_location',
        'artd_partner',
        'artd_product',
        'artd_product_price',
        'artd_stock',
    ]
``
2. Run ``python manage.py migrate`` to create the models.

3. Run the seeder data:
``python manage.py create_countries``
``python manage.py create_colombian_regions``
``python manage.py create_colombian_cities``
``python manage.py create_taxes``

4. After you've installed the migrations and set up login details, you can import the information from Shopify
``python manage.py import_shopify_product <<partner_slug>>``