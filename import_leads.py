import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lead_management.settings")
django.setup()

from leadapp.models import (
    Lead,
    Product,
    Region,
    Territory,
    Lead_Status,
    Lead_Source
)

df = pd.read_excel(
    "Product_Lead_Data_Demo.xlsx",
    sheet_name="Lead"
)

for _, row in df.iterrows():

    territory = Territory.objects.get(
        TerritoryID=int(row["TerritoryID"])
    )

    region = Region.objects.get(
        RegionID=int(row["RegionID"])
    )

    product = Product.objects.get(
        ProductID=int(row["ProductID"])
    )

    status = Lead_Status.objects.get(
        StatusID=int(row["StatusID"])
    )

    source = Lead_Source.objects.get(
        LeadSourceID=int(row["LeadSourceID"])
    )

    Lead.objects.create(
        PersonName=row["PersonName"],
        Gender=row["Gender"],
        CompanyName=row["CompanyName"],
        ContactNo=str(row["ContactNo"]),
        Email=row["Email"],
        City=row["City"],
        State=row["State"],

        TerritoryID=territory,
        RegionID=region,
        ProductID=product,
        StatusID=status,
        LeadSourceID=source,

        BusinessNeed=row["BusinessNeed"],
        Lead_Gen_Date=row["Lead_Gen_Date"],

        Added_By=row["Added_By"],
        Added_Dts=row["Added_Dts"],

        ExecutiveID=int(row["ExecutiveID"])
    )
    print("Inserted:", row["PersonName"])

print("Lead data imported successfully.")