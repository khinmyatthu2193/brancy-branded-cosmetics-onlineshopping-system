from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, SubCategory


class StoreFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_store", verbosity=0)

    def test_seed_command_is_idempotent(self):
        initial_count = Product.objects.count()
        call_command("seed_store", verbosity=0)
        self.assertEqual(Product.objects.count(), initial_count)

    def test_catalogue_pages_render_products(self):
        product = Product.objects.first()
        category = Category.objects.first()
        subcategory = SubCategory.objects.first()
        urls = [
            reverse("home"),
            reverse("shoppage"),
            reverse("productDetail", args=[product.id]),
            reverse("product_list_by_category", args=[category.id]),
            reverse("product_list_by_subcategory", args=[subcategory.id]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_search_returns_matching_product(self):
        response = self.client.post(reverse("search"), {"searched": "Velvet"})
        self.assertContains(response, "Zero Velvet Tint")
