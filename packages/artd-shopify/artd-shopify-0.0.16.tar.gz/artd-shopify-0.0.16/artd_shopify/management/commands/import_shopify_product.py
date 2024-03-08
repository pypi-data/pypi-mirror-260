from django.core.management.base import BaseCommand
from artd_partner.models import Partner
from artd_shopify.utils.shopify_graphql import ShopifyGraphQl


class Command(BaseCommand):
    help = "Import Shopify products for a specific partner"

    def add_arguments(self, parser):
        # Define aquí los parámetros del comando
        parser.add_argument("partner_slug", type=str, help="PArtner slug")

    def handle(self, *args, **options):
        partner_slug = options["partner_slug"]
        try:
            partner = Partner.objects.filter(
                partner_slug=partner_slug,
            ).first()
            sgq = ShopifyGraphQl(partner)
            sgq.store_products_from_shopify()
            sgq.store_categories()
            sgq.store_vendors()
            sgq.store_products_from_shopify_to_artd()
            self.stdout.write(self.style.SUCCESS("Products imported"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
