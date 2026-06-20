import logging
import getpass;
from .models import Product, Region, Lead
from .forms import ProductForm, RegionForm, LeadForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Max

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import (ProductSerializer,RegionSerializer,LeadSerializer)

logger = logging.getLogger(__name__)

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
    try:
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                product = form.save(commit=False)
                max_id = Product.objects.aggregate(Max('productid'))['productid__max']
                product.productid = (max_id or 0) + 1
                product.added_by = getpass.getuser()
                product.added_dts = timezone.now()
                product.save()
                return redirect('product_list')
        else:
            form = ProductForm()

        return render(request, 'product/product_form.html', {'form': form, 'title': 'Add Product'})

    except Exception:
        logger.exception("Unexpected error in add_product")
        return redirect('product_list')


def edit_product(request, id):
    try:
        product = get_object_or_404(Product, pk=id)

        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return redirect('product_list')
        else:
            form = ProductForm(instance=product)

        return render(request, 'product/product_form.html', {'form': form, 'title': 'Edit Product'})

    except Exception:
        logger.exception("Unexpected error in edit_product")
        return redirect('product_list')


def delete_product(request, id):
    try:
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return redirect('product_list')
    except Exception:
        logger.exception("Unexpected error in delete_product")
        return redirect('product_list')


def region_list(request):

    regions = Region.objects.all()

    return render(
        request,
        'region/region_list.html',
        {'regions': regions}
    )


def add_region(request):
    try:
        if request.method == 'POST':
            form = RegionForm(request.POST)
            if form.is_valid():
                region = form.save(commit=False)
                max_id = Region.objects.aggregate(Max('regionid'))['regionid__max']
                region.regionid = (max_id or 0) + 1
                region.added_by = getpass.getuser()
                region.added_dts = timezone.now()
                region.save()
                return redirect('region_list')
        else:
            form = RegionForm()

        return render(request, 'region/region_form.html', {'form': form, 'title': 'Add Region'})

    except Exception:
        logger.exception("Unexpected error in add_region")
        return redirect('region_list')


def edit_region(request, id):
    try:
        region = get_object_or_404(Region, pk=id)

        if request.method == 'POST':
            form = RegionForm(request.POST, instance=region)
            if form.is_valid():
                form.save()
                return redirect('region_list')
        else:
            form = RegionForm(instance=region)

        return render(request, 'region/region_form.html', {'form': form, 'title': 'Edit Region'})

    except Exception:
        logger.exception("Unexpected error in edit_region")
        return redirect('region_list')


def delete_region(request, id):
    try:
        region = get_object_or_404(Region, pk=id)
        region.delete()
        return redirect('region_list')
    except Exception:
        logger.exception("Unexpected error in delete_region")
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
    try:
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

        return render(request, 'lead/lead_form.html', {'form': form, 'title': 'Add Lead'})

    except Exception:
        logger.exception("Unexpected error in add_lead")
        return redirect('lead_list')


def edit_lead(request, id):
    try:
        lead = get_object_or_404(Lead, pk=id)

        if request.method == 'POST':
            form = LeadForm(request.POST, instance=lead)
            if form.is_valid():
                form.save()
                return redirect('lead_list')
        else:
            form = LeadForm(instance=lead)

        return render(request, 'lead/lead_form.html', {'form': form, 'title': 'Edit Lead'})

    except Exception:
        logger.exception("Unexpected error in edit_lead")
        return redirect('lead_list')


def delete_lead(request, id):
    try:
        lead = get_object_or_404(Lead, pk=id)
        lead.delete()
        return redirect('lead_list')
    except Exception:
        logger.exception("Unexpected error in delete_lead")
        return redirect('lead_list')

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
        product = Product.objects.filter(pk=productid).first()

        if not product:
            return Response(
                {"success": False, "message": "Product Not Found"},
                status=404
            )

        serializer = ProductSerializer(product)
        return Response({"success": True, "data": serializer.data})

    except Exception:
        logger.exception("Unexpected error in product_detail_api")
        return Response(
            {"success": False, "message": "Internal server error"},
            status=500
        )

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

api_view(['GET'])
def region_detail_api(request, regionid):
    try:
        region = Region.objects.filter(pk=regionid).first()

        if not region:
            return Response(
                {"success": False, "message": "Region Not Found"},
                status=404
            )

        serializer = RegionSerializer(region)
        return Response({"success": True, "data": serializer.data})

    except Exception:
        logger.exception("Unexpected error in region_detail_api")
        return Response(
            {"success": False, "message": "Internal server error"},
            status=500
        )

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
        lead = Lead.objects.filter(pk=leadid).first()

        if not lead:
            return Response(
                {"success": False, "message": "Lead Not Found"},
                status=404
            )

        serializer = LeadSerializer(lead)
        return Response({"success": True, "data": serializer.data})

    except Exception:
        logger.exception("Unexpected error in lead_detail_api")
        return Response(
            {"success": False, "message": "Internal server error"},
            status=500
        )

@api_view(['POST'])
def product_create_api(request):
    try:
        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=400
            )

        max_id = Product.objects.aggregate(
            Max('productid')
        )['productid__max']

        serializer.save(
            productid=(max_id or 0) + 1,
            added_by=getpass.getuser(),
            added_dts=timezone.now()
        )

        return Response(
            {"success": True, "message": "Product added successfully"},
            status=201
        )

    except Exception as e:
        logger.exception(
            f"Unexpected error in product_create_api: {str(e)}"
        )
        return Response(
            {"success": False, "message": "Internal server error"},
            status=500
        )

@api_view(['POST'])
def region_create_api(request):
    try:
        serializer = RegionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=400
            )

        max_id = Region.objects.aggregate(
            Max('regionid')
        )['regionid__max']

        serializer.save(
            regionid=(max_id or 0) + 1,
            added_by=getpass.getuser(),
            added_dts=timezone.now()
        )

        return Response(
            {"success": True, "message": "Region Added Successfully"},
            status=201
        )

    except Exception:
        logger.exception("Unexpected error in region_create_api")
        return Response(
            {"success": False, "message": "Internal server error"},
            status=500
        )

@api_view(['POST'])
def lead_create_api(request):
    try:
        serializer = LeadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=400
            )

        max_id = Lead.objects.aggregate(
            Max('leadid')
        )['leadid__max']

        serializer.save(
            leadid=(max_id or 0) + 1,
            added_by=getpass.getuser(),
            added_dts=timezone.now()
        )

        return Response(
            {"success": True, "message": "Lead Added Successfully"},
            status=201
        )

    except Exception:
        logger.exception("Unexpected error in lead_create_api")
        return Response(
            {"success": False, "message": "Internal server error"},
            status=500
        )

@api_view(['PUT'])
def product_update_api(request, productid):
    try:
        product = Product.objects.filter(pk=productid).first()
        if not product:
            return Response({"success": False, "message": "Product Not Found"}, status=404)

        old_data = ProductSerializer(product).data
        serializer = ProductSerializer(product, data=request.data)

        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=400)

        serializer.save(added_by=getpass.getuser(), added_dts=timezone.now())

        return Response({
            "success": True,
            "message": "Product Updated Successfully",
            "old_data": old_data,
            "new_data": serializer.data
        })

    except Exception:
        logger.exception("Unexpected error in product_update_api")
        return Response({"success": False, "message": "Internal server error"}, status=500)


@api_view(['DELETE'])
def product_delete_api(request, productid):
    try:
        product = Product.objects.filter(pk=productid).first()
        if not product:
            return Response({"success": False, "message": "Product Not Found"}, status=404)

        product.delete()
        return Response({"success": True, "message": "Product Deleted Successfully"})

    except Exception:
        logger.exception("Unexpected error in product_delete_api")
        return Response({"success": False, "message": "Internal server error"}, status=500)


@api_view(['PUT'])
def region_update_api(request, regionid):
    try:
        region = Region.objects.filter(pk=regionid).first()

        if not region:
            return Response(
                {"success": False, "message": "Region Not Found"},
                status=404
            )

        old_data = RegionSerializer(region).data
        serializer = RegionSerializer(region, data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=400
            )

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

    except Exception:
        logger.exception("Unexpected error in region_update_api")
        return Response(
            {"success": False, "message": "Internal server error"},
            status=500
        )


@api_view(['DELETE'])
def region_delete_api(request, regionid):
    try:
        region = Region.objects.filter(pk=regionid).first()

        if not region:
            return Response(
                {"success": False, "message": "Region Not Found"},
                status=404
            )

        region.delete()
        return Response(
            {"success": True, "message": "Region Deleted Successfully"}
        )

    except Exception:
        logger.exception("Unexpected error in region_delete_api")
        return Response(
            {"success": False, "message": "Internal server error"},
            status=500
        )

@api_view(['PUT'])
def lead_update_api(request, leadid):
    try:
        lead = Lead.objects.filter(pk=leadid).first()

        if not lead:
            return Response(
                {"success": False, "message": "Lead Not Found"},
                status=404
            )

        old_data = LeadSerializer(lead).data
        serializer = LeadSerializer(lead, data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=400
            )

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

    except Exception:
        logger.exception("Unexpected error in lead_update_api")
        return Response(
            {"success": False, "message": "Internal server error"},
            status=500
        )


@api_view(['DELETE'])
def lead_delete_api(request, leadid):
    try:
        lead = Lead.objects.filter(pk=leadid).first()

        if not lead:
            return Response(
                {"success": False, "message": "Lead Not Found"},
                status=404
            )

        lead.delete()
        return Response(
            {"success": True, "message": "Lead Deleted Successfully"}
        )

    except Exception:
        logger.exception("Unexpected error in lead_delete_api")
        return Response(
            {"success": False, "message": "Internal server error"},
            status=500
        )