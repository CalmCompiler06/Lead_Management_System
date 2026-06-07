import getpass;
from .models import Product, Region, Lead
from .forms import ProductForm, RegionForm, LeadForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Max

def home(request):
    return render(request, 'home.html')

def product_list(request):

    products = Product.objects.all()

    return render(
        request,
        'product/product_list.html',
        {'products': products}
    )

def add_product(request):

    if request.method == 'POST':

        form = ProductForm(request.POST)

        if form.is_valid():

            product = form.save(commit=False)

            max_id = Product.objects.aggregate(
                Max('productid')
            )['productid__max']

            product.productid = (max_id or 0) + 1

            product.added_by = getpass.getuser()
            product.added_dts = timezone.now()

            product.save()

            return redirect('product_list')

    else:

        form = ProductForm()

    return render(
        request,
        'product/product_form.html',
        {
            'form': form,
            'title': 'Add Product'
        }
    )


def edit_product(request, id):

    product = get_object_or_404(
        Product,
        pk=id
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect(
                'product_list'
            )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        'product/product_form.html',
        {
            'form': form,
            'title': 'Edit Product'
        }
    )


def delete_product(request, id):

    product = get_object_or_404(
        Product,
        pk=id
    )

    product.delete()

    return redirect(
        'product_list'
    )

def region_list(request):

    regions = Region.objects.all()

    return render(
        request,
        'region/region_list.html',
        {'regions': regions}
    )


def add_region(request):

    if request.method == 'POST':

        form = RegionForm(request.POST)

        if form.is_valid():

            region = form.save(commit=False)
            max_id = Region.objects.aggregate( Max('regionid'))['regionid__max']

            region.regionid = (max_id or 0) + 1
            region.added_by = getpass.getuser()
            region.added_dts = timezone.now()

            region.save()

            return redirect('region_list')
    else:
        form = RegionForm()

    return render(
        request,
        'region/region_form.html',
        {
            'form': form,
            'title': 'Add Region'
        }
    )


def edit_region(request, id):

    region = get_object_or_404(
        Region,
        pk=id
    )

    if request.method == 'POST':

        form = RegionForm(
            request.POST,
            instance=region
        )

        if form.is_valid():
            form.save()
            return redirect('region_list')

    else:

        form = RegionForm(
            instance=region
        )

    return render(
        request,
        'region/region_form.html',
        {
            'form': form,
            'title': 'Edit Region'
        }
    )


def delete_region(request, id):

    region = get_object_or_404(
        Region,
        pk=id
    )

    region.delete()

    return redirect('region_list')


def lead_list(request):

    leads = Lead.objects.all()

    return render(
        request,
        'lead/lead_list.html',
        {
            'leads': leads
        }
    )

def add_lead(request):

    if request.method == 'POST':

        form = LeadForm(request.POST)

        if form.is_valid():

            lead = form.save(commit=False)
            max_id = Lead.objects.aggregate(Max('leadid'))['leadid__max']

            lead.leadid = (max_id or 0) + 1
            lead.added_by = getpass.getuser()
            lead.added_dts = timezone.now()

            lead.save()

            return redirect('lead_list')

    else:

        form = LeadForm()

    return render(
        request,
        'lead/lead_form.html',
        {
            'form': form,
            'title': 'Add Lead'
        }
    )
def edit_lead(request, id):

    lead = get_object_or_404(
        Lead,
        pk=id
    )

    if request.method == 'POST':

        form = LeadForm(
            request.POST,
            instance=lead
        )

        if form.is_valid():

            form.save()

            return redirect(
                'lead_list'
            )

    else:

        form = LeadForm(
            instance=lead
        )

    return render(
        request,
        'lead/lead_form.html',
        {
            'form': form,
            'title': 'Edit Lead'
        }
    )


def delete_lead(request, id):

    lead = get_object_or_404(
        Lead,
        pk=id
    )

    lead.delete()

    return redirect(
        'lead_list'
    )