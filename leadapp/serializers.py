from rest_framework import serializers
from .models import Product , Region , Lead
import getpass
from django.utils import timezone
from datetime import date

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'Added_By': {'required': False},
            'Added_Dts': {'required': False},   
        }
    def validate_ProductName(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Product Name is required"
            )

        if len(value) < 3:
            raise serializers.ValidationError(
                "Product name must be at least 3 characters."
            )
        
        if value.isdigit():
            raise serializers.ValidationError(
                "Product name cannot contain only numbers."
            )
        
        if Product.objects.filter(
            ProductName__iexact=value
        ).exists():
            raise serializers.ValidationError(
                "Product already exists."
            )

        return value
            

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        extra_kwargs = {
            'Added_By': {'required': False},
            'Added_Dts': {'required': False},   
        }

    def validate_RegionName(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Region Name is required"
            )

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Region name must be at least 3 characters."
            )

        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError(
                "Region name should contain only alphabets."
            )

        if Region.objects.filter(
            RegionName__iexact=value
        ).exists():
            raise serializers.ValidationError(
                "Region already exists."
            )

        return value
    

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'   
        extra_kwargs = {
            'Added_By': {'required': False},
            'Added_Dts': {'required': False},   
        }
    def validate_Email(self, value):

        if "@gmail.com" not in value:
            raise serializers.ValidationError(
                "Enter valid Gmail address."
            )
        
        if Lead.objects.filter(
            Email__iexact=value
        ).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def validate_ContactNo(self, value):

        if len(str(value)) != 10:
            raise serializers.ValidationError(
                "Contact number must be 10 digits."
            )
        
        if not str(value).isdigit():
            raise serializers.ValidationError(
                "Contact number must contain digits only."
            )

        return value 

    def validate_PersonName(self, value):

        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError(
                "Name should contain only alphabets."
            )

        return value   
    
    def validate_CompanyName(self, value):

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Company name must be at least 3 characters."
            )

        return value
    
    def validate_BusinessNeed(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Business Need cannot be empty."
            )

        return value
    
    def validate_Lead_Gen_Date(self, value):

        if value > date.today():
            raise serializers.ValidationError(
                "Lead generation date cannot be in future."
            )

        return value
    
    def validate(self, data):

        if not data.get('PersonName'):
            raise serializers.ValidationError(
                {"PersonName": "Lead Name is required"}
            )

        if not data.get('CompanyName'):
            raise serializers.ValidationError(
                {"CompanyName": "Company Name is required"}
            )

        if not data.get('ContactNo'):
            raise serializers.ValidationError(
                {"ContactNo": "Contact Number is required"}
            )

        if not data.get('ProductID'):
            raise serializers.ValidationError(
                {"ProductID": "Product is required"}
            )
        
        if not data.get('RegionID'):
            raise serializers.ValidationError(
                {"RegionID": "Region is required"}
            )

        return data
    
    def validate(self, data):
        person_name = data.get('PersonName')
        company_name = data.get('CompanyName')
        contact_no = data.get('ContactNo')

        if Lead.objects.filter(
        PersonName=person_name,
        CompanyName=company_name
    ).exists():
            raise serializers.ValidationError(
            "Lead already exists with same Name and Company."
        )

        if Lead.objects.filter(ContactNo=contact_no).exists():

            raise serializers.ValidationError(
            {"ContactNo": "Contact Number already exists."}
        )

        return data