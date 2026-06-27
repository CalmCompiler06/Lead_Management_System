import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lead_management.settings")
django.setup()

from leadapp.models import Lead, Product, Region

df = pd.read_excel("Product_Lead_Data_Demo.xlsx", sheet_name="Lead")

for _, row in df.iterrows():

    product = Product.objects.get(ProductID=row["ProductID"])
    region = Region.objects.get(RegionID=row["RegionID"])

    Lead.objects.create(
        PersonName=row["PersonName"],
        CompanyName=row["CompanyName"],
        Email=row["Email"],
        ContactNo=row["ContactNo"],
        Gender=row["Gender"],
        BusinessNeed=row["BusinessNeed"],
        ProductID=product,
        RegionID=region
    )

print("Lead data imported successfully!")