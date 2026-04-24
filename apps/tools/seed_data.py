from django.core.management.base import BaseCommand
from faker import Faker
import random
from products.models import Category, Products
from store.models import Store, Inventory

class Command(BaseCommand):
    help = 'Seeds the database with Categories, Products, Stores, and Inventory'

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write("Clearing old data...")
        Inventory.objects.all().delete()
        Store.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Creating Categories...")
        category_names = [
            "Electronics", "Clothing", "Home & Garden", "Sports", "Toys",
            "Books", "Automotive", "Beauty", "Health", "Grocery",
            "Furniture", "Jewelry", "Pet Supplies", "Tools", "Shoes"
        ]
        categories = []
        for name in category_names:
            cat = Category.objects.create(name=name)
            categories.append(cat)

        self.stdout.write("Creating 1000 Products...")
        products_to_create = []
        for _ in range(1000):
            product = Product(
                title=fake.catch_phrase(),
                description=fake.text(),
                price=round(random.uniform(5.00, 500.00), 2), 
                category=random.choice(categories) 
            )
            products_to_create.append(product)
            
        Product.objects.bulk_create(products_to_create)
        all_products = list(Product.objects.all())

        self.stdout.write("Creating 20 Stores...")
        stores_to_create = []
        for _ in range(20):
            store = Store(
                name=f"{fake.company()} Store",
                location=fake.city()
            )
            stores_to_create.append(store)
            
        Store.objects.bulk_create(stores_to_create)
        all_stores = list(Store.objects.all())

        self.stdout.write("Creating Inventory records...")
        inventory_to_create = []
        for store in all_stores:
            random_300_products = random.sample(all_products, 300)
            
            for product in random_300_products:
                inv = Inventory(
                    store=store,
                    product=product,
                    quantity=random.randint(0, 100) 
                )
                inventory_to_create.append(inv)
        Inventory.objects.bulk_create(inventory_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))