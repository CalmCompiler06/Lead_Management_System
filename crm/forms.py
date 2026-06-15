import re
from django import forms
from .models import Product, Region, Lead
from datetime import date
class ProductForm(forms.ModelForm):

    is_active = forms.ChoiceField(
        choices=[],
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    class Meta:
        model = Product
        exclude = [
            'productid',
            'added_by',
            'added_dts'
        ]
        widgets = {
            'productname': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Enter Product Name'
                }
            ),
            'categoryid': forms.Select(
                attrs={
                    'class':'form-select'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_values = (
            Product.objects
            .values_list(
                'is_active',
                flat=True
            )
            .distinct()
        )
        self.fields['is_active'].choices = [
            (
                value,
                "Yes" if value == 1 else "No"
            )
            for value in active_values
        ]
    def clean_productname(self):

        productname = self.cleaned_data.get(
            'productname'
        )

        if not productname:

            raise forms.ValidationError(
                "Product name is required"
            )

        if not re.match(
            r'^[A-Za-z ]+$',
            productname
        ):
            raise forms.ValidationError(
                "Product name should contain only alphabets"
            )
        return productname
    
    def clean_categoryid(self):

        categoryid = self.cleaned_data.get(
        'categoryid'
        )

        if not categoryid:

            raise forms.ValidationError(
                "Category is required"
            )

        return categoryid

class RegionForm(forms.ModelForm):

    regionname = forms.ChoiceField(
        choices=[],
        widget=forms.Select(
            attrs={
                'class':'form-select'
            }
        )
    )


    class Meta:

        model = Region

        exclude = [
            'regionid',
            'added_by',
            'added_dts'
        ]


    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)


        region_values = (
            Region.objects
            .values_list(
                'regionname',
                flat=True
            )
            .distinct()
        )

        self.fields['regionname'].choices = [(
            '',
            'Select Region'
            )]+[
            (
                value,
                value
            )
            for value in region_values
            if value
        ]


    def clean_regionname(self):

        regionname = self.cleaned_data.get(
            'regionname'
        )


        if not regionname:

            raise forms.ValidationError(
                "Region name is required"
            )


        return regionname

class LeadForm(forms.ModelForm):
    class Meta:

        model = Lead

        exclude = [
            'leadid',
            'added_by',
            'added_dts'
        ]

        widgets = {

            'lead_gen_date': forms.DateInput(
                attrs={
                    'type':'date',
                    'class':'form-control'
                }
            ),
            'executiveid': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Enter Executive ID'
                }
            ),

            'businessneed': forms.Textarea(
                attrs={
                    'rows':3,
                    'class':'form-control'
                }
            )
        }

    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)

        for field_name, field in self.fields.items():

            if field_name not in [
                'lead_gen_date',
                'businessneed',
                'executiveid'
            ]:

                field.widget.attrs.update({
                    'class':'form-control'
                })

    def clean_personname(self):

        personname = self.cleaned_data.get(
            'personname'
        )
        if not personname:

            raise forms.ValidationError(
                "Person name is required"
            )

        if not re.match(
            r'^[A-Za-z0-9 ]+$',
            personname
        ):
            raise forms.ValidationError(
                "Person name should contain only letters and numbers"
            )
        return personname
    
    def clean_companyname(self):
        companyname = self.cleaned_data.get(
            'companyname'
        )
        if not companyname:

            raise forms.ValidationError(
                "Company name is required"
            )

        if not re.match(
            r'^[A-Za-z0-9 ]+$',
            companyname
        ):
            raise forms.ValidationError(
                "Company name should contain only letters and numbers"
            )
        return companyname

    def clean_contactno(self):

        contactno = self.cleaned_data.get(
            'contactno'
        )

        if not contactno:

            raise forms.ValidationError(
                "Contact number is required"
            )

        if not re.match(
            r'^[0-9]{10}$',
            contactno
        ):

            raise forms.ValidationError(
                "Contact number must contain exactly 10 digits"
            )

        return contactno

    def clean_email(self):

        email = self.cleaned_data.get(
            'email'
        )
        if not email:

            raise forms.ValidationError(
                "Email is required"
            )

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(
            pattern,
            email
        ):
            raise forms.ValidationError(
                "Enter a valid email address"
            )
        return email
    def clean_city(self):

        city = self.cleaned_data.get(
            'city'
        )
        if not city:

            raise forms.ValidationError(
                "City is required"
            )

        if not re.match(
            r'^[A-Za-z0-9 ]+$',
            city
        ):

            raise forms.ValidationError(
                "City should contain only letters and numbers"
            )


        return city

    def clean_state(self):

        state = self.cleaned_data.get(
            'state'
        )
        if not state:

            raise forms.ValidationError(
                "State is required"
            )
        if not re.match(
            r'^[A-Za-z0-9 ]+$',
            state
        ):

            raise forms.ValidationError(
                "State should contain only letters and numbers"
            )
        return state

    def clean_executiveid(self):

        executiveid = self.cleaned_data.get(
            'executiveid'
        )
        if not executiveid:

            raise forms.ValidationError(
                "Executive ID is required"
            )
        if not str(executiveid).isdigit():

            raise forms.ValidationError(
                "Executive ID must be an integer"
            )
        return executiveid

    def clean_businessneed(self):

        businessneed = self.cleaned_data.get(
            'businessneed'
        )
        if not businessneed:

            raise forms.ValidationError(
                "Business need is required"
            )
        return businessneed

    def clean_lead_gen_date(self):

        lead_gen_date = self.cleaned_data.get(
            'lead_gen_date'
        )

        if not lead_gen_date:

            raise forms.ValidationError(
                "Lead generation date is required"
            )


        if lead_gen_date > date.today():

            raise forms.ValidationError(
                "Lead generation date cannot be in the future"
            )
        return lead_gen_date
    
    def clean(self):
        cleaned_data = super().clean()
        required_fields = [
            'gender',
            'territoryid',
            'regionid',
            'productid',
            'statusid',
            'leadsourceid'
        ]
        for field in required_fields:

            if not cleaned_data.get(field):

                self.add_error(
                    field,
                    f"{field} is required"
                )
        return cleaned_data