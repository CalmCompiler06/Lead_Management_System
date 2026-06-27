from django.db import models


class Product_Category(models.Model):
    CategoryID = models.AutoField(primary_key=True)
    CategoryName = models.CharField(max_length=100)
    Added_By = models.CharField(max_length=100)
    Added_Dts = models.DateTimeField()

    class Meta:
        db_table = 'Product_Category'
        managed = False

    def __str__(self):
        return f"{self.CategoryID} - {self.CategoryName}"


class Region(models.Model):
    RegionID = models.AutoField(primary_key=True)
    RegionName = models.CharField(max_length=100)
    Added_By = models.CharField(max_length=100)
    Added_Dts = models.DateTimeField()

    class Meta:
        db_table = 'Region'
        managed = False

    def __str__(self):
        return self.RegionName


class Lead_Status(models.Model):
    StatusID = models.AutoField(primary_key=True)
    StatusName = models.CharField(max_length=100)
    Added_By = models.CharField(max_length=100)
    Added_Dts = models.DateTimeField()

    class Meta:
        db_table = 'Lead_Status'
        managed = False

    def __str__(self):
        return self.StatusName


class Lead_Source(models.Model):
    LeadSourceID = models.AutoField(primary_key=True)
    LeadSourceName = models.CharField(max_length=100)
    Added_By = models.CharField(max_length=100)
    Added_Dts = models.DateTimeField()

    class Meta:
        db_table = 'Lead_Source'
        managed = False

    def __str__(self):
        return self.LeadSourceName


class Product(models.Model):
    ProductID = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=100)

    CategoryID = models.ForeignKey(
        Product_Category,
        on_delete=models.PROTECT,
        db_column='CategoryID'
    )

    Is_Active = models.BooleanField(default=True)
    Added_By = models.CharField(max_length=100)
    Added_Dts = models.DateTimeField(auto_now_add = True)
    

    class Meta:
        db_table = 'Product'
        
        managed = False

    def __str__(self):
        return self.ProductName


class Territory(models.Model):
    TerritoryID = models.AutoField(primary_key=True)
    TerritoryName = models.CharField(max_length=100)

    RegionID = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_column='RegionID'
    )

    Added_By = models.CharField(max_length=100)
    Added_Dts = models.DateTimeField()

    class Meta:
        db_table = 'Territory'
        managed = False

    def __str__(self):
        return self.TerritoryName


class Lead(models.Model):
    LeadID = models.AutoField(primary_key=True)
    PersonName = models.CharField(max_length=100)
    Gender = models.CharField(max_length=20)
    CompanyName = models.CharField(max_length=150)
    ContactNo = models.CharField(max_length=15)
    Email = models.EmailField()
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    GENDER_CHOICES =[
        ('Male' , 'Male'),
        ('Female' ,'Female'),
        ('Other' , 'Other'),
    ]
    Gender = models.CharField(max_length=10 , choices=GENDER_CHOICES, blank=True , null=True)


    TerritoryID = models.ForeignKey(
        Territory,
        on_delete=models.CASCADE,
        db_column='TerritoryID'
    )

    RegionID = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_column='RegionID'
    )

    ProductID = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column='ProductID'
    )

    StatusID = models.ForeignKey(
        Lead_Status,
        on_delete=models.CASCADE,
        db_column='StatusID'
    )

    LeadSourceID = models.ForeignKey(
        Lead_Source,
        on_delete=models.CASCADE,
        db_column='LeadSourceID'
    )
    #StatusID = models.ForeignKey(Lead_Status, on_delete=models.SET_NULL, null=True, blank=True)
    #LeadSourceID = models.ForeignKey(Lead_Source, on_delete=models.SET_NULL, null=True, blank=True)

    BusinessNeed = models.CharField(max_length=255)

    Lead_Gen_Date = models.DateField()

    Added_By = models.CharField(max_length=100)
    Added_Dts = models.DateTimeField()

    ExecutiveID = models.IntegerField()


    class Meta:
        db_table = 'Lead'
        managed = False

    def __str__(self):
        return self.PersonName

class Status(models.Model):
    StatusID = models.AutoField(primary_key=True , db_column = 'StatusID')
    StatusName = models.CharField(max_length=100 , db_column = 'StatusName')

    class Meta:
        db_table = 'Lead_Status'

    def _str_(self):
        return self.StatusName
    
class LeadSource(models.Model):
    LeadSourceID = models.AutoField(primary_key=True)
    LeadSourceName = models.CharField(max_length=100)

    class Meta:
        db_table = 'Lead_Source'
        managed = False

    def _str_(self):
        return self.LeadSourceName    

   