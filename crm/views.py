import getpass;
from .models import Product, Region, Lead
from .forms import ProductForm, RegionForm, LeadForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Max

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import (ProductSerializer,RegionSerializer,LeadSerializer)
from django.shortcuts import get_object_or_404

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

@api_view(['GET'])
def product_api(request):

    products = Product.objects.all()

    serializer = ProductSerializer(
        products,
        many=True
    )

    return Response({
        "success": True,
        "count": products.count(),
        "data": serializer.data
    })

@api_view(['GET'])
def product_detail_api(request, productid):

    try:

        product = Product.objects.get(
            pk=productid
        )

        serializer = ProductSerializer(product)

        return Response({
            "success": True,
            "data": serializer.data
        })

    except Product.DoesNotExist:

        return Response({
            "success": False,
            "message": "Product Not Found"
        })

@api_view(['GET'])
def region_api(request):

    regions = Region.objects.all()

    serializer = RegionSerializer(
        regions,
        many=True
    )

    return Response({
        "success": True,
        "count": regions.count(),
        "data": serializer.data
    })

@api_view(['GET'])
def region_detail_api(request, regionid):

    try:

        region = Region.objects.get(
            pk=regionid
        )

        serializer = RegionSerializer(region)

        return Response({
            "success": True,
            "data": serializer.data
        })

    except Region.DoesNotExist:

        return Response({
            "success": False,
            "message": "Region Not Found"
        })

@api_view(['GET'])
def lead_api(request):

    leads = Lead.objects.all()

    serializer = LeadSerializer(
        leads,
        many=True
    )

    return Response({
        "success": True,
        "count": leads.count(),
        "data": serializer.data
    })

@api_view(['GET'])
def lead_detail_api(request, leadid):

    try:

        lead = Lead.objects.get(
            pk=leadid
        )

        serializer = LeadSerializer(lead)

        return Response({
            "success": True,
            "data": serializer.data
        })

    except Lead.DoesNotExist:

        return Response({
            "success": False,
            "message": "Lead Not Found"
        })

@api_view(['POST'])
def product_create_api(request):

    serializer = ProductSerializer(
        data=request.data
    )

    if serializer.is_valid():

        max_id = Product.objects.aggregate(
            Max('productid')
        )['productid__max']

        serializer.save(
            productid=(max_id or 0) + 1,
            added_by=getpass.getuser(),
            added_dts=timezone.now()
        )

        return Response({
            "success": True,
            "message": "Product Added Successfully"
        })

    return Response({
        "success": False,
        "message": "Failed to Add Product",
        "errors": serializer.errors
})

@api_view(['POST'])
def region_create_api(request):

    serializer = RegionSerializer(
        data=request.data
    )

    if serializer.is_valid():

        max_id = Region.objects.aggregate(
            Max('regionid')
        )['regionid__max']

        serializer.save(
            regionid=(max_id or 0) + 1,
            added_by=getpass.getuser(),
            added_dts=timezone.now()
        )

        return Response({
            "success": True,
            "message": "Region Added Successfully"
        })

    return Response({
        "success": False,
        "message": "Failed to Add Region",
        "errors": serializer.errors
})


@api_view(['POST'])
def lead_create_api(request):

    serializer = LeadSerializer(
        data=request.data
    )

    if serializer.is_valid():

        max_id = Lead.objects.aggregate(
            Max('leadid')
        )['leadid__max']

        serializer.save(
            leadid=(max_id or 0) + 1,
            added_by=getpass.getuser(),
            added_dts=timezone.now()
        )

        return Response({
            "success": True,
            "message": "Lead Added Successfully"
        })

    return Response({
        "success": False,
        "message": "Failed to Add Lead",
        "errors": serializer.errors
})


@api_view(['PUT'])
def product_update_api(request, productid):

    try:

        product = Product.objects.get(
            pk=productid
        )

        old_data = ProductSerializer(product).data

        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                added_by=getpass.getuser(),
                added_dts=timezone.now()
            )

            return Response({
                "success": True,
                "message": "Product Updated Successfully",
                "old_data": old_data,
                "new_data": serializer.data
            })

        return Response({
            "success": False,
            "message": "Failed to Update Product",
            "errors": serializer.errors
        })

    except Product.DoesNotExist:

        return Response({
            "success": False,
            "message": "Product Not Found"
        })


@api_view(['DELETE'])
def product_delete_api(request, productid):

    product = get_object_or_404(
        Product,
        pk=productid
    )

    product.delete()

    return Response({
        "success": True,
        "message": "Product Deleted Successfully"
    })


@api_view(['PUT'])
def region_update_api(request, regionid):

    try:

        region = Region.objects.get(
            pk=regionid
        )

        old_data = RegionSerializer(region).data

        serializer = RegionSerializer(
            region,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                added_by=getpass.getuser(),
                added_dts=timezone.now()
            )

            return Response({
                "success": True,
                "message": "Region Updated Successfully",
                "old_data": old_data,
                "new_data": serializer.data
            })

        return Response({
            "success": False,
            "message": "Failed to Update Region",
            "errors": serializer.errors
        })

    except Region.DoesNotExist:

        return Response({
            "success": False,
            "message": "Region Not Found"
        })


@api_view(['DELETE'])
def region_delete_api(request, regionid):

    region = get_object_or_404(
        Region,
        pk=regionid
    )

    region.delete()

    return Response({
        "success": True,
        "message": "Region Deleted Successfully"
    })


@api_view(['PUT'])
def lead_update_api(request, leadid):

    try:

        lead = Lead.objects.get(
            pk=leadid
        )

        old_data = LeadSerializer(lead).data

        serializer = LeadSerializer(
            lead,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                added_by=getpass.getuser(),
                added_dts=timezone.now()
            )

            return Response({
                "success": True,
                "message": "Lead Updated Successfully",
                "old_data": old_data,
                "new_data": serializer.data
            })

        return Response({
            "success": False,
            "message": "Failed to Update Lead",
            "errors": serializer.errors
        })

    except Lead.DoesNotExist:

        return Response({
            "success": False,
            "message": "Lead Not Found"
        })


@api_view(['DELETE'])
def lead_delete_api(request, leadid):

    lead = get_object_or_404(
        Lead,
        pk=leadid
    )

    lead.delete()

    return Response({
        "success": True,
        "message": "Lead Deleted Successfully"
    })