from .models import Product

class ProductService:

    @staticmethod
    async def get_product(product_id):
        return await Product.objects.aget(id=product_id)