import re
from rest_framework import serializers
from .models import Product, Region, Lead
from datetime import date

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

        read_only_fields = (
            'productid',
            'added_by',
            'added_dts'
        )

    def validate_productname(self,value):
        if not value:
            raise serializers.ValidationError(
                "Product name is required"
            )

        if not re.match(
            r'^[A-Za-z ]+$',
            value
        ):
            raise serializers.ValidationError(
                "Product name should contain only alphabets"
            )

        return value
    def validate_categoryid(self,value):

        if not value:

            raise serializers.ValidationError(
                "Category is required"
            )

        return value
    def validate_is_active(self,value):

        if value is None:

           raise serializers.ValidationError(
                "Is Active field is required"
            )

        if value not in [0,1]:

            raise serializers.ValidationError(
                "Is Active value must be either 0 or 1"
            )

        return value

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'

        read_only_fields = (
            'regionid',
            'added_by',
            'added_dts'
        )
    def validate_regionname(self,value):

        if not value:

            raise serializers.ValidationError(
                "Region name is required"
            )
        
        available_regions = list(Region.objects.values_list(
            'regionname',
            flat = True
        ))

        if value not in available_regions:

            raise serializers.ValidationError(
                {
                    "message": "Invalid region name. Please select a region from available regions.",
                    "available_regions": available_regions
                }
            )
        return value


class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = (
            'leadid',
            'added_by',
            'added_dts'
        )

    def validate_personname(self,value):
        if not value:
            raise serializers.ValidationError(
                "Person name is required"
            )
        if not re.match(
            r'^[A-Za-z0-9 ]+$',
            value
        ):
            raise serializers.ValidationError(
                "Person name should contain only letters and numbers"
            )
        return value

    def validate_companyname(self,value):
        if not value:
            raise serializers.ValidationError(
                "Company name is required"
            )
        if not re.match(
            r'^[A-Za-z0-9 ]+$',
            value
        ):
            raise serializers.ValidationError(
                "Company name should contain only letters and numbers"
            )

        return value

    def validate_contactno(self,value):
        if not value:
            raise serializers.ValidationError(
                "Contact number is required"
            )
        if not re.match(
            r'^[0-9]{10}$',
            value
        ):
            raise serializers.ValidationError(
                "Contact number must contain exactly 10 digits"
            )
        return value

    def validate_email(self,value):
        if not value:
            raise serializers.ValidationError(
                "Email is required"
            )
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(
            pattern,
            value
        ):
            raise serializers.ValidationError(
                "Enter a valid email address"
            )
        return value
    
    def validate_city(self,value):
        if not value:
            raise serializers.ValidationError(
                "City is required"
            )
        if not re.match(
            r'^[A-Za-z0-9 ]+$',
            value
        ):
            raise serializers.ValidationError(
                "City should contain only letters and numbers"
            )
        return value

    def validate_state(self,value):
        if not value:
            raise serializers.ValidationError(
                "State is required"
            )
        if not re.match(
            r'^[A-Za-z0-9 ]+$',
            value
        ):
            raise serializers.ValidationError(
                "State should contain only letters and numbers"
            )
        return value
    def validate_executiveid(self,value):

        if value is None:

            raise serializers.ValidationError(
                "Executive ID is required"
            )


        if not str(value).isdigit():

            raise serializers.ValidationError(
                "Executive ID must be integer"
            )


        return value

    def validate_gender(self,value):
        if not value:
            raise serializers.ValidationError(
                "Gender is required"
            )
        return value
    
    def validate(self,data):

        required_fields = [
            'productid',
            'regionid',
            'territoryid',
            'statusid',
            'leadsourceid',
            'businessneed',
            'lead_gen_date'
        ]
        for field in required_fields:

            if not data.get(field):

                raise serializers.ValidationError(
                    {
                        field:
                        f"{field} is required"
                    }
                )
        return data
    def validate_businessneed(self,value):
        if not value:
            raise serializers.ValidationError(
                "Business need is required"
            )
        return value    
    
    def validate_lead_gen_date(self, value):

        if not value:

            raise serializers.ValidationError(
                "Lead generation date is required"
            )


        if value > date.today():

            raise serializers.ValidationError(
                "Lead generation date cannot be in the future"
            )


        return value