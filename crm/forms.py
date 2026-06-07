from django import forms
from .models import Product, Region, Lead


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        exclude = [
            'productid',
            'added_by',
            'added_dts'
        ]


class RegionForm(forms.ModelForm):

    class Meta:
        model = Region

        exclude = [
            'regionid',
            'added_by',
            'added_dts'
        ]


class LeadForm(forms.ModelForm):

    class Meta:
        model = Lead

        exclude = ['leadid','added_by', 'added_dts']

        widgets = {
            'lead_gen_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'businessneed': forms.Textarea(
                attrs={
                    'rows': 3
                }
            )
        }