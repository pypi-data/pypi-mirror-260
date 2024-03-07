from artd_partner.models import Partner
from artd_product.models import (
    Product,
    Category,
    RootCategory,
    Brand,
    Tax,
    Image as ShopifyImage,
    ProductImage,
    GroupedProduct,
)
from artd_shopify.models import (
    ShopifyGraphQlCredential,
    ShopifyProduct,
    ShopifyBrand,
    ShopifyCategory,
)
import os
from urllib.parse import urlparse
import requests
import json
import requests
from io import BytesIO
from PIL import Image
from django.core.files import File
from artd_shopify.utils.graphql.queries import (
    MAIN_NODE_REQUIRED_INFO,
    NODE_REQUIRED_INFO,
)
from artd_price_list.models import PriceList
from artd_stock.models import Stock
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOCAL_PATH = os.path.join("media/product/images/")


class ShopifyGraphQl:
    __partner = None
    __shopify_credential = None
    __vendor = None
    __shopify_credential = None
    __store_key = None
    __api_version = None
    __api_key = None
    __api_secret = None
    __access_token = None
    __product_counter = None
    __brand_prefix = None
    __category_regular_expression = None
    __endpoint = None

    def __init__(self, partner: Partner):
        self.__partner = partner
        self.__shopify_credential = ShopifyGraphQlCredential.objects.get(
            partner=partner
        )
        self.__vendor = self.__shopify_credential.vendor
        self.__store_key = self.__shopify_credential.store_key
        self.__api_version = self.__shopify_credential.api_version
        self.__api_key = self.__shopify_credential.api_key
        self.__api_secret = self.__shopify_credential.api_secret
        self.__access_token = self.__shopify_credential.access_token
        self.__product_counter = self.__shopify_credential.product_counter
        self.__brand_prefix = self.__shopify_credential.brand_prefix
        self.__category_regular_expression = (
            self.__shopify_credential.category_regular_expression
        )
        self.__endpoint = f"https://{self.__store_key}.myshopify.com/admin/api/{self.__api_version}/graphql.json"
        self.__headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.__access_token,
        }

    def make_shopify_graphql_request(self, query, variables=None):
        self.__endpoint = f"https://{self.__store_key}.myshopify.com/admin/api/{self.__api_version}/graphql.json"
        data = {
            "query": query,
            "variables": variables,
        }
        response = requests.post(
            self.__endpoint,
            headers=self.__headers,
            data=json.dumps(data),
        )

        return response.json()

    def get_products(self, page_size=20):
        cursor = None
        all_products = []

        while True:
            graphql_query = """
            query ($pageSize: Int!, $cursor: String) {
                products(first: $pageSize, after: $cursor) {
                    edges {
                        node {
                            %s
                            variants(first: 50) {
                                edges {
                                    node {
                                        %s
                                    }
                                }
                            }
                        }
                    }
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                }
            }
            """ % (
                MAIN_NODE_REQUIRED_INFO,
                NODE_REQUIRED_INFO,
            )
            variables = {
                "pageSize": page_size,
                "cursor": cursor,
            }
            response = self.make_shopify_graphql_request(
                graphql_query,
                variables,
            )
            products = (
                response.get("data", {})
                .get("products", {})
                .get(
                    "edges",
                    [],
                )
            )
            all_products.extend(products)
            page_info = (
                response.get("data", {})
                .get("products", {})
                .get(
                    "pageInfo",
                    {},
                )
            )
            has_next_page = page_info.get(
                "hasNextPage",
                False,
            )
            cursor = page_info.get(
                "endCursor",
                None,
            )

            if not has_next_page:
                break

        return all_products

    def create_or_check_folder(self, folder_path):
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                print(f"The folder '{folder_path}' has been created.")
            except OSError as e:
                print(f"Error creating the folder '{folder_path}': {e}")
        else:
            print(f"The folder '{folder_path}' already exists.")

    def get_id_from_gid_string(self, string: str):
        splited_string = string.split("/")
        return splited_string[-1]

    def get_extension_from_url(self, url):
        file_path = urlparse(url).path
        file_name, extension = os.path.splitext(file_path)
        return extension

    def store_image_locally(self, src, id):
        # Generar el nombre del archivo
        extension = self.get_extension_from_url(src)
        name = f"{id}{extension}"

        # Reemplazar caracteres problemáticos en el nombre del archivo
        name = (
            name.replace("..png", ".png")
            .replace("..jpg", ".jpg")
            .replace("..jpeg", ".jpeg")
            .replace("..gif", ".gif")
            .replace("..webp", ".webp")
            .replace("..bmp", ".bmp")
            .replace("..tiff", ".tiff")
            .replace("..svg", ".svg")
            .replace("..ico", ".ico")
        )

        # Verificar si la imagen ya existe localmente
        local_path = os.path.join("media/product/images/", name)
        print(f"Local path: {local_path}")
        if os.path.exists(local_path):
            print(f"La imagen {name} ya existe localmente.")
            return File(open(local_path, "rb"), name=name)

        # Descargar la imagen
        response = requests.get(src)
        response.raise_for_status()

        # Almacenar la imagen localmente
        with open(local_path, "wb") as file:
            file.write(response.content)

        print(f"La imagen {name} se almacenó localmente correctamente.")

        # Crear y retornar el objeto File
        image = File(open(local_path, "rb"), name=name)
        return image

    def store_image_locally_old(self, src, id):
        response = requests.get(src)
        response.raise_for_status()
        extension = self.get_extension_from_url(src)
        name = f"{id}{extension}"
        name = name.replace("..png", ".png")
        name = name.replace("..jpg", ".jpg")
        name = name.replace("..jpeg", ".jpeg")
        name = name.replace("..gif", ".gif")
        name = name.replace("..webp", ".webp")
        name = name.replace("..bmp", ".bmp")
        name = name.replace("..tiff", ".tiff")
        name = name.replace("..svg", ".svg")
        name = name.replace("..ico", ".ico")
        print(f"Image {name} stored successfully.")
        image = File(BytesIO(response.content), name=name)
        return image

    def delete_image_file(self, file_path):
        try:
            os.remove(file_path)
            print(f"File {file_path} deleted successfully.")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    def save_artd_images(self, images):
        stored_images = []
        image_list = images.get("edges", [])
        self.create_or_check_folder(LOCAL_PATH)
        for image_node in image_list:
            image = image_node.get("node", {})
            src = image.get("src", None)
            id = self.get_id_from_gid_string(image.get("id", None))
            image_source = {
                "name": "shopify",
                "id": id,
                "partner": self.__partner.id,
            }
            if (
                ShopifyImage.objects.filter(
                    external_id=id,
                    partner=self.__partner,
                ).count()
                == 0
            ):
                image = ShopifyImage.objects.create(
                    image=self.store_image_locally(src, id),
                    alt=f"{id}",
                    external_id=id,
                    partner=self.__partner,
                    source=image_source,
                )
                stored_images.append(image)
            else:
                image = ShopifyImage.objects.filter(
                    external_id=id,
                    partner=self.__partner,
                ).first()
                stored_images.append(image)

        return stored_images

    def store_products_from_shopify(self):
        products = self.get_products(250)
        for product in products:
            node = product.get("node", {})
            id = self.get_id_from_gid_string(node.get("id", None))
            title = node.get("title", None)
            if (
                ShopifyProduct.objects.filter(
                    product_id=id,
                    partner=self.__partner,
                ).count()
                == 0
            ):
                shopify_product = ShopifyProduct(
                    product_id=id,
                    json_data=product,
                    partner=self.__partner,
                    name=title,
                )
                shopify_product.save()
            else:
                ShopifyProduct.objects.filter(
                    product_id=id,
                    partner=self.__partner,
                ).update(json_data=product)
        return True

    def get_categories_from_full_name(self, full_name):
        categories = full_name.split(">")
        categories_list = []
        for category in categories:
            category = category.strip()
            categories_list.append(category)
        return categories_list

    def store_categories(self):
        if (
            RootCategory.objects.filter(
                name=self.__vendor,
                partner=self.__partner,
            ).count()
            == 0
        ):
            root_category = RootCategory.objects.create(
                name=self.__vendor,
                partner=self.__partner,
            )
        else:
            root_category = RootCategory.objects.get(
                name=self.__vendor,
                partner=self.__partner,
            )

        first_category = True

        products = ShopifyProduct.objects.all()
        for product in products:
            node = product.json_data.get("node", {})
            category = node.get("productCategory", None)
            tax = Tax.objects.first()
            if category is not None:
                product_taxonomy_node = category.get("productTaxonomyNode", {})
                full_name = product_taxonomy_node.get("fullName", None)
                categories = self.get_categories_from_full_name(full_name)
                counter = 0
                for category_name in categories:
                    # ArtD CAtegories
                    if first_category:
                        if (
                            Category.objects.filter(
                                name=category_name,
                                root_category=root_category,
                                partner=self.__partner,
                            ).count()
                            == 0
                        ):
                            category = Category.objects.create(
                                name=category_name,
                                root_category=root_category,
                                partner=self.__partner,
                            )
                        first_category = False
                    else:
                        if (
                            Category.objects.filter(
                                name=category_name,
                                root_category=root_category,
                                partner=self.__partner,
                            ).count()
                            == 0
                        ):
                            previous_category = Category.objects.filter(
                                name=categories[counter - 1],
                                partner=self.__partner,
                            ).first()

                            category = Category.objects.create(
                                name=category_name,
                                partner=self.__partner,
                                parent=previous_category,
                            )
                    # Shopify categories
                    if (
                        ShopifyCategory.objects.filter(
                            name=category_name,
                            artd_partner=self.__partner,
                        ).count()
                        == 0
                    ):
                        ShopifyCategory.objects.create(
                            name=category_name,
                            artd_partner=self.__partner,
                            json_data=product_taxonomy_node,
                            artd_tax=tax,
                        )
                    else:
                        ShopifyCategory.objects.filter(
                            name=category_name,
                            artd_partner=self.__partner,
                        ).update(json_data=product_taxonomy_node)
                    counter = counter + 1

    def store_vendors(self):
        products = ShopifyProduct.objects.all()
        for product in products:
            node = product.json_data.get("node", {})
            vendor = node.get("vendor", None)
            if vendor is not None:
                if (
                    ShopifyBrand.objects.filter(
                        name=vendor,
                        artd_partner=self.__partner,
                    ).count()
                    == 0
                ):
                    ShopifyBrand.objects.create(
                        name=vendor,
                        artd_partner=self.__partner,
                    )
                if (
                    Brand.objects.filter(
                        name=vendor,
                    ).count()
                    == 0
                ):
                    Brand.objects.create(
                        name=vendor,
                    )

    def store_products_from_shopify_to_artd(self):
        all_products = ShopifyProduct.objects.all()
        for product in all_products:
            node = product.json_data.get("node", {})
            id = node.get("id", None)
            title = node.get("title", None)
            description = node.get("description", None)
            description_html = node.get("descriptionHtml", None)
            images = node.get("images", [])
            handle = node.get("handle", None)
            options = node.get("options", [])
            online_store_preview_url = node.get("onlineStorePreviewUrl", None)
            product_category = node.get("productCategory", None)
            product_type = node.get("productType", None)
            seo = node.get("seo", None)
            meta_description = seo.get("description", None)
            meta_description = "" if meta_description is None else meta_description
            meta_title = seo.get("title", None)
            meta_title = "" if meta_title is None else meta_title
            status = node.get("status", None)
            tags = node.get("tags", None)
            total_inventory = node.get("totalInventory", None)
            total_variants = node.get("totalVariants", None)
            vendor = node.get("vendor", None)
            variants = node.get("variants", {}).get("edges", [])
            first_product = True
            option_list = []
            if product_category is None:
                category = None
                artd_category = Category.objects.first()
                tax = Tax.objects.first()
            else:
                category = ShopifyCategory.objects.filter(
                    name=product_category.get("productTaxonomyNode", {}).get(
                        "name", None
                    ),
                    artd_partner=self.__partner,
                ).first()
                artd_category = Category.objects.filter(
                    name=category.name,
                    partner=self.__partner,
                ).first()
                tax = category.artd_tax
            for option in options:
                id = self.get_id_from_gid_string(option.get("id", None))
                name = option.get("name", None)
                values = option.get("values", [])
                option_list.append(
                    {
                        "id": id,
                        "name": name,
                        "values": values,
                    }
                )
            shopify_images = self.save_artd_images(images)
            variant_products = []
            brand = Brand.objects.filter(name=vendor).first()
            if brand is None:
                brand = Brand.objects.first()
            for variant in variants:
                variant_node = variant.get("node", {})
                variant_id = variant_node.get("id", None)
                variant_id = self.get_id_from_gid_string(variant_id)
                variant_title = variant_node.get("title", None)
                variant_sku = variant_node.get("sku", None)
                variant_price = variant_node.get("price", None)
                variant_weight = variant_node.get("weight", None)
                variant_inventory_quantity = variant_node.get("inventoryQuantity", None)

                if variant_title == "Default Title":
                    variant_title = title

                source = {
                    "name": "shopify",
                    "id": variant_id,
                    "partner": self.__partner.id,
                }

                if first_product:
                    sku = variant_sku
                    first_product = False
                if (
                    Product.objects.filter(
                        partner=self.__partner,
                        external_id=variant_id,
                    ).count()
                    == 0
                ):
                    try:
                        product = Product.objects.create(
                            partner=self.__partner,
                            source=source,
                            json_data=variant,
                            external_id=variant_id,
                            url_key=handle,
                            meta_title=meta_title,
                            meta_description=meta_description,
                            meta_keywords="",
                            type="physical",
                            name=variant_title,
                            sku=variant_sku,
                            description=description_html,
                            short_description=description,
                            tax=tax,
                            weight=variant_weight,
                            unit_of_measure="kg",
                            measure=variant_weight,
                            variations=option_list,
                            brand=brand,
                        )
                        product.categories.add(artd_category)
                        Stock.objects.create(
                            partner=self.__partner,
                            product=product,
                            stock=variant_inventory_quantity,
                        )
                        PriceList.objects.create(
                            partner=self.__partner,
                            product=product,
                            regular_price=variant_price,
                        )
                    except Exception as e:
                        print(f"Error creating product: {e}")
                        product = None
                else:
                    try:
                        product = Product.objects.filter(
                            partner=self.__partner,
                            external_id=variant_id,
                        ).first()
                        Product.objects.filter(
                            partner=self.__partner,
                            external_id=variant_id,
                        ).update(
                            json_data=variant,
                            url_key=handle,
                            meta_title=meta_title,
                            meta_description=meta_description,
                            meta_keywords="",
                            type="physical",
                            name=variant_title,
                            sku=variant_sku,
                            description=description_html,
                            short_description=description,
                            tax=tax,
                            weight=variant_weight,
                            unit_of_measure="kg",
                            measure=variant_weight,
                            variations=option_list,
                            brand=brand,
                        )
                        product.categories.clear()
                        product.categories.add(artd_category)
                        Stock.objects.filter(
                            partner=self.__partner,
                            product=product,
                        ).update(stock=variant_inventory_quantity)
                        PriceList.objects.filter(
                            partner=self.__partner,
                            product=product,
                        ).update(regular_price=variant_price)
                    except Exception as e:
                        print(f"Error updating product: {e}")
                        product = None
                if product is not None:
                    variant_products.append(product)
                    for shopify_image in shopify_images:
                        if (
                            ProductImage.objects.filter(
                                product=product,
                                image=shopify_image,
                            ).count()
                            == 0
                        ):
                            source = {
                                "name": "shopify",
                                "id": variant_id,
                                "partner": self.__partner.id,
                            }
                            ProductImage.objects.create(
                                source=source,
                                external_id=variant_id,
                                product=product,
                                image=shopify_image,
                            )

            if (
                GroupedProduct.objects.filter(
                    partner=self.__partner,
                    external_id=variant_id,
                ).count()
                == 0
            ):
                grouped_product = GroupedProduct.objects.create(
                    source=source,
                    json_data=node,
                    external_id=variant_id,
                    partner=self.__partner,
                    url_key=handle,
                    name=title,
                    sku=sku,
                    description=description_html,
                    short_description=description,
                    variations=options,
                )
                for product in variant_products:
                    grouped_product.products.add(product)
            else:
                grouped_product = GroupedProduct.objects.filter(
                    partner=self.__partner,
                    external_id=variant_id,
                ).first()
                GroupedProduct.objects.filter(
                    partner=self.__partner,
                    external_id=variant_id,
                ).update(
                    source=source,
                    json_data=node,
                    url_key=handle,
                    name=title,
                    sku=sku,
                    description=description_html,
                    short_description=description,
                    variations=options,
                )
                grouped_product.products.clear()
                for product in variant_products:
                    grouped_product.products.add(product)
