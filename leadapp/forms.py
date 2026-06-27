from django import forms
from .models import Product, Region , Lead , Territory , Lead_Status , LeadSource


class ProductForm(forms.ModelForm):
    # 1. Added Product ID as a read-only display field
    ProductID= forms.CharField(
        label="ProductID",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'placeholder': 'Auto-generated'})
    )

    # 2. Changed Is Active to a Dropdown with the label "Status"
    is_active = forms.ChoiceField(
        label="Status",
        choices=[(True, 'Active'), (False, 'Inactive')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=True
    )

    class Meta:
        model = Product
        fields = ['ProductName', 'CategoryID'] 
        labels = {
            'CategoryID': 'Category'
        }

        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category_id': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()

        product_name = cleaned_data.get('ProductName')
        product_code = cleaned_data.get('ProductCode')

        if not product_name:
            raise forms.ValidationError("Product Name is required")

        if not product_code:
            raise forms.ValidationError("Product Code is required")

        return cleaned_data


class RegionForm(forms.ModelForm):
    REGION_CHOICES = [
        ('', '--- Select a Region ---'),
        ('North', 'North'),
        ('South', 'South'),
        ('East', 'East'),
        ('West', 'West'),
    ]

    RegionName = forms.ChoiceField(
        choices=REGION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'required': 'required'})
    )

    class Meta:
        model = Region
        fields = ['RegionName']
        widgets = {
            'RegionName':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter region name...'
            })
        }
    def __init__(self,*args,**kwargs):
        super(RegionForm,self).__init__(*args,**kwargs)
        if self.instance and self.instance.pk:
            self.fields['RegionName'].initial = self.instance.RegionName

    def clean_RegionName(self):
        region_name = self.cleaned_data['RegionName']

        if len(region_name) < 3:
            raise forms.ValidationError(
                "Region name must be at least 3 characters."
            )

        return region_name    
    
    def clean(self):
        cleaned_data = super().clean()

        region_name = cleaned_data.get('RegionName')

        if not region_name:
            raise forms.ValidationError("Region Name is required")

        return cleaned_data


# ---------------- LEAD FORM ----------------
class LeadForm(forms.ModelForm):
    TerritoryID = forms.ModelChoiceField(
        queryset=Territory.objects.all(),
        empty_label="Select Territory"
    )

    StatusID = forms.ModelChoiceField(
        queryset=Lead_Status.objects.all(),
        empty_label="-----------",
        widget=forms.Select(attrs={'class' : 'form-select'})
    )

    LeadSourceID = forms.ModelChoiceField(
        queryset=LeadSource.objects.all(),
        empty_label="-----------",
        required = False,
        widget=forms.Select(attrs={'class' : 'form-select'})
    )

    class Meta:
        model = Lead
        fields = '__all__'

        widgets = {
            'PersonName': forms.TextInput(attrs={   # lead_name
                'class': 'form-control'
            }),
            'Email': forms.EmailInput(attrs={  #email
                'class': 'form-control'
            }),
            'ContactNo': forms.TextInput(attrs={  #phone
                'class': 'form-control'
            }),
            'product': forms.Select(attrs={
                'class': 'form-control'
            }),
            'region': forms.Select(attrs={
                'class': 'form-control'
            }),
        }  
        field_order = ['Email', 'City', 'State', 'TerritoryID', 'ProductID', 'RegionID', 'StatusID', 'Lead_Gen_Date', 'BusinessNeed']
        def __init__(self,*args,**kwargs):
            super(LeadForm,self).__init__(*args,**kwargs)
            #if 'StatusID' in self.fields:
             #   self.fields['StatusID'].to_field_name = 'StatusID'
            #if 'LeadSourceID' in self.fields:
             #   self.fields['LeadSourceID'].to_field_name = 'LeadSourceID'
            self.fields['StatusID'].queryset = Lead_Status.objects.all()   
            #self.fields['LeadSourceID'].queryset = LeadSource.objects.all()  

    def clean_Email(self):
        email = self.cleaned_data['Email']

        if "@gmail.com" not in email:
            raise forms.ValidationError(
                "Please enter a valid Gmail address."
            )

        return email

    def clean_ContactNo(self):
        contact = self.cleaned_data['ContactNo']

        if len(contact) != 10:
            raise forms.ValidationError("Contact Number must be 10 digits")
        
        if not contact.isdigit():
            raise forms.ValidationError(
                "Contact number must contain digits only."
            )

        return contact

    
    def clean(self):
        cleaned_data = super().clean()
        person_name = cleaned_data.get('PersonName')
        company_name = cleaned_data.get('CompanyName')
        if Lead.objects.filter(
        PersonName=person_name,
        CompanyName=company_name
    ).exists():
            raise forms.ValidationError(
            "Lead already exists"
        )
        return cleaned_data    
    

def clean(self):
        cleaned_data = super().clean()

        person_name = cleaned_data.get('PersonName')
        company_name = cleaned_data.get('CompanyName')
        contact_no = cleaned_data.get('ContactNo')
        product = cleaned_data.get('ProductID')
        region = cleaned_data.get('RegionID')

        if not person_name:
            raise forms.ValidationError("Lead Name is required")

        if not company_name:
            raise forms.ValidationError("Company Name is required")

        if not contact_no:
            raise forms.ValidationError("Contact Number is required")

        if not product:
            raise forms.ValidationError("Product is required")

        if not region:
            raise forms.ValidationError("Region is required")

        return cleaned_data