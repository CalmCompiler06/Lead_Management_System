from rest_framework import serializers
from .models import Product,Region,Lead


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product

        fields = '__all__'

        read_only_fields = (
            'productid',
            'added_by',
            'added_dts'
        )

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'

        read_only_fields = (
            'regionid',
            'added_by',
            'added_dts'
)


class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead
        fields = '__all__'

        read_only_fields = (
            'leadid',
            'added_by',
            'added_dts'
        )