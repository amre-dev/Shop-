from django.core.management.base import BaseCommand
from store.models import Category, Product, ProductImage
from django.core.files.base import ContentFile
import io

class Command(BaseCommand):
    help = 'Seed sample categories and products (no images)'
    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()
        cat = Category.objects.create(name='إلكترونيات', position=1)
        p1 = Product.objects.create(category=cat, name='سماعة لاسلكية V-100', price=30.00, quantity=10)
        p2 = Product.objects.create(category=cat, name='كيبل USB-C', price=8.00, quantity=25)
        self.stdout.write(self.style.SUCCESS('Sample data created.'))
