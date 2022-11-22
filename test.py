from home.models import Product

Product_name="Carrot"
price= "100"
quantity = "50"
image = "E:\images\placeholder_2"
date ="27/04/2022"

r = Product(Product_name=Product_name, price=price, quantity=quantity, image=image, date=date)
r.save()