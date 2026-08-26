from django.core.management.base import BaseCommand

from store.models import Brand, Category, Product, SkinType, SubCategory


SAMPLE_PRODUCTS = [
    ("BR001", "Hydrating Facial Cleanser", 28000, "Skincare", "Cleansers", "CeraVe", "products/almond1.png", False, 0),
    ("BR002", "Daily Moisturizing Lotion", 32000, "Skincare", "Moisturizers", "CeraVe", "products/almond2.png", True, 27000),
    ("BR003", "Zero Velvet Tint", 24500, "Makeup", "Lip Color", "Rom&nd", "products/3_Romand_Zero_Velvet_Tint_Baked_Series1.jpg", False, 0),
    ("BR004", "Glassing Melting Balm", 26000, "Makeup", "Lip Color", "Rom&nd", "products/2_Romand_Glasting_Melting_Balm1.jpg", True, 22000),
    ("BR005", "True Match Foundation", 45000, "Makeup", "Foundation", "L'Oreal Paris", "products/3_Loreal_Paris_True_Match_Liquid_Foundation1.png", False, 0),
    ("BR006", "Lash Paradise Mascara", 35000, "Makeup", "Eye Makeup", "L'Oreal Paris", "products/1_Loreal_Paris_Lash_Paradise_Mascara1.jpg", False, 0),
]


class Command(BaseCommand):
    help = "Create a small, repeatable sample catalogue for local development."

    def handle(self, *args, **options):
        normal, _ = SkinType.objects.get_or_create(name="Normal", defaults={"description": "Balanced skin"})
        created_count = 0
        for code, name, price, category_name, subcategory_name, brand_name, image, is_sale, sale_price in SAMPLE_PRODUCTS:
            category, _ = Category.objects.get_or_create(name=category_name)
            subcategory, _ = SubCategory.objects.get_or_create(name=subcategory_name, category=category)
            brand, _ = Brand.objects.get_or_create(name=brand_name)
            _, created = Product.objects.update_or_create(
                pdID=code,
                defaults={
                    "name": name,
                    "price": price,
                    "category": category,
                    "subCategory": subcategory,
                    "brand": brand,
                    "description": f"A sample {name.lower()} for exploring the BRANCY shop.",
                    "is_sale": is_sale,
                    "sale_price": sale_price,
                    "main_image": image,
                    "secondary_image": image,
                    "extra_image1": image,
                    "extra_image2": image,
                    "key_ingredients": "See product packaging for the complete ingredient list.",
                    "how_to_use": "Apply as directed and discontinue use if irritation occurs.",
                    "skin_type": normal,
                },
            )
            created_count += int(created)
        self.stdout.write(self.style.SUCCESS(
            f"Sample catalogue ready: {len(SAMPLE_PRODUCTS)} products ({created_count} created)."
        ))
