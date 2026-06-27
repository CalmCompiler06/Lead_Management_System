from django.shortcuts import render, redirect, get_object_or_404
from .models import Product ,Region , Territory , Status , LeadSource , Product_Category
from .forms import ProductForm, RegionForm , LeadForm 
from django.utils import timezone
import pandas as pd
from django.contrib import messages
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product , Region , Lead
from .serializers import ProductSerializer ,RegionSerializer , LeadSerializer
from rest_framework import status
import getpass
from django.utils import timezone
from django.db.models import Q
from django.db import connection
from django.db import DatabaseError, IntegrityError
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
import logging
from django.db.models import Count
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


logger = logging.getLogger('frontend')

class ProductAPI(APIView):

    def get(self, request):
        try:

            products = Product.objects.all()
            CategoryID = request.GET.get('category')
            if CategoryID:
                products = products.filter(CategoryID=int(CategoryID))
            serializer = ProductSerializer(products, many=True)
            return Response({
            "Success": "Products fetched successfully",
            "count": products.count(),
            "data": serializer.data
        })
        except ValueError:

            return Response(
            {
                "error": "Invalid search parameter."
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        
        except DatabaseError:

            return Response([])

        except Exception:
            return Response([])

    def post(self, request):
        try:

            data = request.data.copy()
            data['Added_By'] = getpass.getuser()
            data['Added_Dts'] = timezone.now()

            serializer = ProductSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                "Success": "Product added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except IntegrityError:

            existing = Product.objects.first()

            if existing:
                return Response(
                ProductSerializer(existing).data
                )
            
        
        except Exception as e:

            return Response(
            {"error": str(e)}
            )

class ProductDetailAPI(APIView):

    def put(self, request, id):

        product = Product.objects.get(ProductID=id)

        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
            "Success": "Product updated successfully",
            "data": serializer.data
        })

        return Response(serializer.errors)

    def delete(self, request, id):

        product = Product.objects.get(ProductID=id)

        product.delete()

        return Response(
            {"Success": "Product deleted successfully"}
        )    
    
class RegionAPI(APIView):

    def get(self, request):
        try:


            regions = Region.objects.all()
            serializer = RegionSerializer(regions, many=True)
            return Response({
            "Success": "Regions fetched successfully",
            "count": regions.count(),
            "data": serializer.data
            })
        except ValueError:

            return Response(
            {
                "error": "Invalid search parameter."
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        
        except DatabaseError:

            return Response([])

        
        except Exception:

            return Response([])

    def post(self, request):
        try:
            data = request.data.copy()
            try:
                data['Added_By'] = getpass.getuser()
            except Exception:
                data['Added_By'] = 'System'

            try:
                data['Added_Dts'] = timezone.now()
            except Exception:
                pass 

            serializer = RegionSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                "Success": "Region added successfully",
                "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )
        
        except IntegrityError:

            existing = Region.objects.first()

            if existing:
                return Response(
                RegionSerializer(existing).data
                )
            
        except Exception as e:

            return Response(
            {"error": str(e)}
            )    

class RegionDetailAPI(APIView):

    def put(self, request, id):

        region = Region.objects.get(RegionID=id)

        serializer = RegionSerializer(
            region,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "Success": "Region updated successfully",
                "data": serializer.data
            })

        return Response(serializer.errors)

    def delete(self, request, id):

        region = Region.objects.get(RegionID=id)

        region.delete()

        return Response(
            {"Success": "Region deleted successfully"}
        )        
    
class LeadAPI(APIView):

    def get(self, request):
        try:
             
            leads = Lead.objects.all()
            LeadID = request.GET.get('lead_id')
            PersonName = request.GET.get('person_name')
            ProductID = request.GET.get('product')
            RegionID = request.GET.get('region')

            if LeadID:
                leads = leads.filter(LeadID=LeadID)

            if PersonName:
                leads = leads.filter(PersonName__icontains=PersonName)

            if ProductID:
                leads = leads.filter(
                ProductID__ProductName__icontains=ProductID
            )

            if RegionID:
                leads = leads.filter(
                RegionID__RegionName__icontains=RegionID
            )

            leads = Lead.objects.select_related(
            'ProductID',
            'RegionID'
            )
        
            serializer = LeadSerializer(
            leads,
            many=True
            )

            return Response({
            "Success": "Leads fetched successfully",
            "count": leads.count(),
            "data": serializer.data
            })
        except ValueError:
            return Response(
            {
                "error": "Invalid search parameter value."
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        
        except DatabaseError:

            leads = []
            return Response(leads)
        
        except Exception:

           return Response([])
    

    def post(self, request):


        try:

            data = request.data.copy()

            try:
                data['Added_By'] = getpass.getuser()
            except Exception:
                data['Added_By'] = 'System'

            try:
                data['Added_Dts'] = timezone.now()
            except Exception:
                pass

            serializer = LeadSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)

            return Response(serializer.errors)

        except IntegrityError:

            existing = Lead.objects.filter(
            ContactNo=data.get('ContactNo')
            ).first()

            if existing:
                return Response(
                LeadSerializer(existing).data
            )

        except DatabaseError:
            return Response(
            {"message": "Database unavailable"}
            )

        except Exception as e:
            return Response(
            {"error": str(e)}
             )

class LeadDetailAPI(APIView):

    def put(self, request, id):
        try:

            lead = Lead.objects.get(
            LeadID=id
            )

            serializer = LeadSerializer(
            lead,
            data=request.data
            )

            if serializer.is_valid():

                serializer.save()

                return Response({
                "Success": "Lead updated successfully",
                "data": serializer.data
                })

            return Response(serializer.errors)
        
        except Lead.DoesNotExist:

            serializer = LeadSerializer(
            data=request.data
            )

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)

            return Response(serializer.errors)
        
        except IntegrityError:

            return Response(
            {
                "error": "Duplicate data found"
            },
            status=400
            )
        
        except Exception as e:

            return Response(
            {
                "error": str(e)
            },
            status=500
            )

    def delete(self, request, id):
        try:

            lead = Lead.objects.get(
            LeadID=id
            )

            lead.delete()

            return Response(
            {"Success": "Lead deleted successfully"}
            )    
        
        except Lead.DoesNotExist:

            return Response(
            {
                "error": "Lead not found"
            },
            status=404
            )
        
        except Exception as e:

            return Response(
            {
                "error": str(e)
            },
            status=500
            )


def upload_lead_excel(request):
    if request.method == "POST" and request.FILES.get('excel_file'):
        file = request.FILES['excel_file']
        
        try:
            df = pd.read_excel(file)
            df.columns = df.columns.str.strip().str.lower()
            
            for index, row in df.iterrows():
                lead_name = row.get('LeadID') 
                email = row.get('email')
                excel_region = str(row.get('RegionID')).strip()
                excel_product = str(row.get('ProductID')).strip()
                status = row.get('status', 'Active') # Defaults to Active if missing
                
                try:
                    # 1. Lookup the actual Region object from the database using Excel text
                    region_obj = Region.objects.get(name__iexact=excel_region)
                    
                    # 2. Lookup the actual Product object from the database using Excel text
                    product_obj = Product.objects.get(name__iexact=excel_product)
                    
                    # 3. Save the Lead securely into the database table
                    Lead.objects.create(
                        name=lead_name,
                        email=email,
                        region=region_obj,    # Assigns the linked database row object
                        product=product_obj,  # Assigns the linked database row object
                        status=status
                    )
                    
                except Region.DoesNotExist:
                    messages.error(request, f"Row {index+2}: Region '{excel_region}' was not found in your database master table.")
                    continue  # Skip this row and keep processing the rest
                except Product.DoesNotExist:
                    messages.error(request, f"Row {index+2}: Product '{excel_product}' was not found in your database master table.")
                    continue
                    
            messages.success(request, "Excel records processed successfully!")
            return redirect('lead_list') # Redirect back to your dashboard list view
            
        except Exception as e:
            messages.error(request, f"Critical error parsing file: {str(e)}")
            return redirect('lead_list')

    return render(request, 'leadapp/upload_form.html') # Adjust template name to match your file

@login_required
def home_dashboard(request):
    return redirect('home')
    #return render(request,'home.html')




# ---------------- HOME ----------------
@login_required
def home(request):

    total_leads = Lead.objects.count()
    total_products = Product.objects.count()
    total_regions = Region.objects.count()

    lead_status_data = (
    Lead.objects
    .values('StatusID__StatusName')
    .annotate(total=Count('LeadID'))
)
    status_labels = []
    status_counts = []

    for item in lead_status_data:
        status_labels.append(item['StatusID__StatusName'])
        status_counts.append(item['total'])

    context = {
        'total_leads': total_leads,
        'total_products': total_products,
        'total_regions': total_regions,

        'status_labels': status_labels,
        'status_counts': status_counts,
    }

    return render(request, 'home.html', context)


# ================= REGION CRUD =================
from django.shortcuts import render
from django.db.models import Q
from django.db import DatabaseError

# ==================== REGION CRUD ====================
@login_required
def region_list(request):
    try:
        # Get the search parameter from the query string
        search = request.GET.get('search', '').strip()
        
        regions = Region.objects.all()
        
        if search:
            # Check if the user is searching for a numeric ID
            if search.isdigit():
                regions = regions.filter(
                    Q(RegionID=int(search)) |
                    Q(RegionName__iexact=f"Region {search}")
                )
            else:
                # Substring case-insensitive lookup for text matches
                regions = regions.filter(RegionName__icontains=search)
                
    except DatabaseError:
        regions = []
        
    except Exception as e:
        logger.error(
            f"Error in region_list view: {str(e)}",
            exc_info=True
        )
        regions = []
        
    return render(
        request, 
        'region/region_list.html', 
        {'regions': regions, 'search_value': search}
    )

@login_required
def add_region(request):
    form = RegionForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('region_list')

    return render(request, 'region/region_form.html', {'form': form})

@login_required
def edit_region(request, pk):
    region = get_object_or_404(Region, RegionID=pk)
    
    if request.method =="POST":
        form = RegionForm(request.POST or None, instance=region)
        if form.is_valid():
            form.save()
            return redirect('region_list')
    else:
        form = RegionForm(instance=region)    
    return render(request, 'region/region_form.html', {'form': form})

@login_required
def delete_region(request, id):
    region = get_object_or_404(Region, id=id)
    region.delete()
    return redirect('region_list')


# ================= PRODUCT CRUD =================
@login_required
def product_list(request):
    try:
        # Get the search query from the search input element
        search = request.GET.get('search', '').strip()
        
        # Pull products along with their category relationships
        products = Product.objects.select_related('CategoryID')
        
        if search:
            # Case A: If user enters an explicit number ID (e.g., "1" or "10")
            if search.isdigit():
                products = products.filter(
                    Q(ProductID=int(search)) |
                    Q(CategoryID__CategoryID=int(search)) |
                    Q(ProductName__iexact=f"Product {search}")
                )
            # Case B: If user enters a full tag name (e.g., "product 10")
            elif search.lower().startswith('product '):
                products = products.filter(ProductName__iexact=search)
            # Case C: General text partial matches
            else:
                products = products.filter(
                    Q(ProductName__icontains=search) |
                    Q(CategoryID__CategoryName__icontains=search)
                )
                
    except DatabaseError:
        products = []
        
    except Exception as e:
        logger.error(f"Error in product_list view: {str(e)}", exc_info=True)
        products = []
        
    # Return context including the search term to populate the form box
    return render(
        request, 
        'product/product_list.html', 
        {'products': products, 'search_value': search}
    )

@login_required
def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'product/product_form.html', {'form': form})

@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, ProductID=id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'product/product_form.html', {'form': form})

@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, ProductID=id)
    product.delete()
    return redirect('product_list')

@login_required
def lead_list(request):
    try:
       
        search = request.GET.get('search', '').strip()
        
        leads = Lead.objects.select_related(
            'ProductID',
            'RegionID'
        )
        
        if search:
            
            if search.isdigit():
                leads = leads.filter(
                    Q(PersonName__iexact=f"Person {search}") |
                    Q(CompanyName__iexact=f"Company {search}") |
                    Q(ProductID__ProductName__icontains=search) |
                    Q(RegionID__RegionName__icontains=search)
                )
            
           
            elif search.lower().startswith('person ') or search.lower().startswith('company '):
                leads = leads.filter(
                    Q(PersonName__iexact=search) |
                    Q(CompanyName__iexact=search)
                )
                
            # Case 3: Standard fallback for regular search text (e.g., searching for product names)
            else:
                leads = leads.filter(
                    Q(PersonName__icontains=search) |
                    Q(ProductID__ProductName__icontains=search) |
                    Q(RegionID__RegionName__icontains=search)
                )
                
    except DatabaseError:
        leads = []
        
    except Exception as e:
        logger.error(f"Error in lead_list view: {str(e)}", exc_info=True)
        leads = []
        
    return render(
        request,
        'lead/lead_list.html',
        {'leads': leads}
    )

@login_required
def add_lead(request):
    try:

        if request.method == 'POST':
            form = LeadForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('lead_list')
        else:
            form = LeadForm()

        lead_sources = LeadSource.objects.all()
        products = Product.objects.all()
        regions = Region.objects.all()
        territories = Territory.objects.all()
        statuses = Status.objects.all()

    except Exception as e:
        logger.error(
            f"Error in add_list view: {str(e)}",
            exc_info=True
        )

        form = LeadForm()    

    return render(request, 'lead/add_lead.html', {
        'form': form,
        'lead_sources': lead_sources,
        'statuses': statuses,
        'products': products,
        'regions': regions,
        'territories': territories,
    })

@login_required
def edit_lead(request, id):
    lead = get_object_or_404(Lead, pk=id)
    
    if request.method == 'POST':
        # 2. Populate the form with POST data and the existing instance
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('lead_list')  # Redirect back to your dashboard name
    else:
        # 3. GET request: Pre-populate the form fields with the current lead data
        form = LeadForm(instance=lead)
        
    # 4. Send the form and the lead object to the template
    return render(request, 'lead/lead_form.html', {
        'form': form,
        'lead': lead
    })

@login_required
def delete_lead(request, id):

    try:

        lead = Lead.objects.get(LeadID=id)

        lead.delete()

    except Lead.DoesNotExist:

        pass

    except Exception as e:
        logger.error(
            f"Error in delete_lead view: {str(e)}",
            exc_info=True
        )

        pass

    return redirect('lead_list')

   
@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            # 1. Stop Django from saving directly to the database just yet
            product = form.save(commit=False)
            
            product.added_by = request.user      # Fills Added_By with the logged-in user session
            product.added_dts = timezone.now()   # Fills Added_Dts with the current timestamp
            
            # Save to database
            product.save()
            return redirect('product_list')  # Replace with your actual redirect URL name
    else:
        form = ProductForm()
        
    return render(request, 'product/product_form.html', {'form': form})


@login_required
def lead_analytics(request):

    lead_status_data = (
        Lead.objects
        .values('StatusID__StatusName')
        .annotate(total=Count('LeadID'))
    )

    labels = []
    counts = []

    for item in lead_status_data:
        labels.append(item['StatusID__StatusName'])
        counts.append(item['total'])

    context = {
        'labels': labels,
        'counts': counts
    }

    return render(
        request,
        'lead_analytics.html',
        context
    )

@login_required
def product_analytics(request):

    product_data = (
        Lead.objects
        .values('ProductID__ProductName')
        .annotate(total=Count('LeadID'))
        .order_by('-total')
    )

    labels = []
    counts = []

    for item in product_data:
        labels.append(item['ProductID__ProductName'])
        counts.append(item['total'])

    context = {
        'labels': labels,
        'counts': counts
    }

    return render(
        request,
        'product_analytics.html',
        context
    )

@login_required
def region_analytics(request):

    region_data = (
        Lead.objects
        .values('RegionID__RegionName')
        .annotate(total=Count('LeadID'))
        .order_by('-total')
    )

    labels = []
    counts = []

    for item in region_data:
        labels.append(item['RegionID__RegionName'])
        counts.append(item['total'])

    total_regions = Region.objects.count()

    total_leads = Lead.objects.count()

    top_region = (
        Lead.objects
        .values('RegionID__RegionName')
        .annotate(total=Count('LeadID'))
        .order_by('-total')
        .first()
    )

    context = {
        'labels': labels,
        'counts': counts,

        'total_regions': total_regions,
        'total_leads': total_leads,
        'top_region': top_region
    }

    return render(
        request,
        'region_analytics.html',
        context
    )

@login_required
def product_bulk_upload(request):

    print("METHOD:", request.method)
    print("FILES:", request.FILES)

    if request.method == 'POST':

        try:

            excel_file = request.FILES.get('excel_file')

            if not excel_file:

                messages.error(
                    request,
                    "Please select an Excel file."
                )

                return redirect('product_list')

            df = pd.read_excel(excel_file)

            print("Excel loaded successfully")
            print("Columns:", df.columns.tolist())
            print(df.head())

            required_columns = [
                'ProductName',
                'CategoryID',
                'Is_Active'
            ]

            if not all(
                col in df.columns
                for col in required_columns
            ):

                messages.error(
                    request,
                    "This is not a valid excel file. Please upload a valid excel file."
                )

                return redirect('product_list')

            uploaded_count = 0

            for index, row in df.iterrows():

                product_name = str(
                    row['ProductName']
                ).strip()

                category = str(
                    row['CategoryID']
                ).strip()

                is_active = row['Is_Active']
                print("CHECKING REQUIRED COLUMNS")
                print(required_columns)

                # Product Name Validation

                if not product_name or product_name.lower() == 'nan':

                    messages.error(
                        request,
                        f"Product Name is empty at row {index + 2}"
                    )

                    continue

                # Duplicate Product Validation

                if Product.objects.filter(
                    ProductName__iexact=product_name
                ).exists():

                    messages.warning(
                        request,
                        f"{product_name} already exists."
                    )

                    continue

                # Category Validation

                if not category or category.lower() == 'nan':

                    messages.error(
                        request,
                        f"Category is empty at row {index + 2}"
                    )

                    continue

                # IsActive Validation

                if pd.isna(is_active):

                    is_active = True

                try:

                    category_obj = Product_Category.objects.get(
                        CategoryName__iexact=category
                    )

                except Product_Category.DoesNotExist:

                    messages.error(
                        request,
                        f"Category '{category}' does not exist."
                    )

                    continue

                print("REACHED NEW CREATE BLOCK")

                Product.objects.create(
                    ProductName=product_name,
                    CategoryID=category_obj,
                    Is_Active=is_active,
                    Added_By=getpass.getuser()

                )

                uploaded_count += 1

            if uploaded_count > 0:

                messages.success(
                    request,
                    f"{uploaded_count} product(s) uploaded successfully."
                )

            else:

                messages.warning(
                    request,
                    "No products were uploaded."
                )

            return redirect('product_list')

        except Exception as e:
            import traceback


            print("ERROR:", e)
            traceback.print_exc()

            logger.error(
            f"Product Bulk Upload Error: {str(e)}",
            exc_info=True
            )

            #messages.error(
            #request,
            #"This is not a valid excel file. Please upload a valid excel file."
           #)

        missing_cols = [
            col for col in required_columns
            if col not in df.columns
        ]

        messages.error(
            request,
            f"Missing columns: {missing_cols}"
            )
 
        return redirect('product_list')


def login_view(request):

    if request.user.is_authenticated:
        return redirect('home_dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home_dashboard')

        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(request, 'login.html')


def logout_view(request):

    logout(request)

    return redirect('login')    
    


@login_required
def region_bulk_upload(request):

    print("METHOD:", request.method)
    print("FILES:", request.FILES)

    if request.method == 'POST':

        try:

            excel_file = request.FILES.get('excel_file')

            if not excel_file:

                messages.error(
                    request,
                    "Please select an Excel file."
                )

                return redirect('region_list')

            # Read Excel
            df = pd.read_excel(excel_file)

            print("Excel Loaded Successfully")
            print("Columns:", df.columns.tolist())
            print(df.head())

            # Required column
            required_columns = [
                'RegionName'
            ]

            if not all(col in df.columns for col in required_columns):

                messages.error(
                    request,
                    "This is not a valid excel file. Please upload a valid excel file."
                )

                return redirect('region_list')

            uploaded_count = 0

            for index, row in df.iterrows():

                region_name = str(
                    row['RegionName']
                ).strip()

                # Validation 1 : Empty Region Name

                if not region_name or region_name.lower() == "nan":

                    messages.error(
                        request,
                        f"Region Name is empty at row {index + 2}"
                    )

                    continue

                # Validation 2 : Duplicate Region

                if Region.objects.filter(
                    RegionName__iexact=region_name
                ).exists():

                    messages.warning(
                        request,
                        f"{region_name} already exists."
                    )

                    continue

                # Insert Record

                Region.objects.create(

                    RegionName=region_name,
                    Added_By=getpass.getuser()

                )

                uploaded_count += 1

            if uploaded_count > 0:

                messages.success(
                    request,
                    f"{uploaded_count} region(s) uploaded successfully."
                )

            else:

                messages.warning(
                    request,
                    "No regions were uploaded."
                )

            return redirect('region_list')

        except Exception as e:

            import traceback

            print("ERROR:", e)
            traceback.print_exc()

            logger.error(
                f"Region Bulk Upload Error: {str(e)}",
                exc_info=True
            )

            messages.error(
                request,
                "This is not a valid excel file. Please upload a valid excel file."
            )

            return redirect('region_list')

    return redirect('region_list')    

@login_required
def lead_bulk_upload(request):

    if request.method == "POST":

        try:

            excel_file = request.FILES.get("excel_file")

            if not excel_file:

                messages.error(
                    request,
                    "Please select an Excel file."
                )

                return redirect("lead_list")

            df = pd.read_excel(excel_file)

            required_columns = [

                "PersonName",
                "CompanyName",
                "ContactNo",
                "Email",
                "Product",
                "Region",
                "Status",
                "LeadSource"

            ]

            if not all(col in df.columns for col in required_columns):

                messages.error(
                    request,
                    "This is not a valid excel file. Please upload a valid excel file."
                )

                return redirect("lead_list")

            uploaded_count = 0

            for index, row in df.iterrows():

                person_name = str(row["PersonName"]).strip()
                company = str(row["CompanyName"]).strip()
                contact = str(row["ContactNo"]).strip()
                email = str(row["Email"]).strip()

                product = str(row["Product"]).strip()
                region = str(row["Region"]).strip()
                status = str(row["Status"]).strip()
                source = str(row["LeadSource"]).strip()

                # -----------------------------
                # Validation
                # -----------------------------

                if person_name == "" or person_name.lower() == "nan":

                    messages.error(
                        request,
                        f"Person Name is empty at row {index+2}"
                    )

                    continue

                if company == "" or company.lower() == "nan":

                    messages.error(
                        request,
                        f"Company Name is empty at row {index+2}"
                    )

                    continue

                if Product.objects.filter(
                    ProductName__iexact=product
                ).exists():

                    product_obj = Product.objects.get(
                        ProductName__iexact=product
                    )

                else:

                    messages.error(
                        request,
                        f"Product '{product}' does not exist."
                    )

                    continue

                if Region.objects.filter(
                    RegionName__iexact=region
                ).exists():

                    region_obj = Region.objects.get(
                        RegionName__iexact=region
                    )

                else:

                    messages.error(
                        request,
                        f"Region '{region}' does not exist."
                    )

                    continue

                if Status.objects.filter(
                    StatusName__iexact=status
                ).exists():

                    status_obj = Status.objects.get(
                        StatusName__iexact=status
                    )

                else:

                    messages.error(
                        request,
                        f"Status '{status}' does not exist."
                    )

                    continue

                if LeadSource.objects.filter(
                    LeadSourceName__iexact=source
                ).exists():

                    source_obj = LeadSource.objects.get(
                        LeadSourceName__iexact=source
                    )

                else:

                    messages.error(
                        request,
                        f"Lead Source '{source}' does not exist."
                    )

                    continue

                # Duplicate Validation

                if Lead.objects.filter(

                    PersonName__iexact=person_name,
                    CompanyName__iexact=company

                ).exists():

                    messages.warning(
                        request,
                        f"{person_name} already exists."
                    )

                    continue

                Lead.objects.create(

                    PersonName=person_name,
                    CompanyName=company,
                    ContactNo=contact,
                    Email=email,

                    ProductID=product_obj,
                    RegionID=region_obj,
                    StatusID=status_obj,
                    LeadSourceID=source_obj,

                    Added_By=getpass.getuser()

                )

                uploaded_count += 1

            if uploaded_count > 0:

                messages.success(
                    request,
                    f"{uploaded_count} Lead(s) uploaded successfully."
                )

            else:

                messages.warning(
                    request,
                    "No Leads were uploaded."
                )

        except Exception as e:

            print(e)

            messages.error(
                request,
                "This is not a valid excel file. Please upload a valid excel file."
            )

    return redirect("lead_list")


@login_required
def export_products(request):

    products = Product.objects.select_related('CategoryID').all()

    data = []

    for product in products:

        data.append({

            "Product ID": product.ProductID,
            "Product Name": product.ProductName,
            "Category": product.CategoryID.CategoryName,
            "Is Active": product.Is_Active,
            "Added By": product.Added_By,
            "Added Date": product.Added_Dts.strftime("%d-%m-%Y %H:%M")

        })

    df = pd.DataFrame(data)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="Products.xlsx"'

    with pd.ExcelWriter(response, engine="openpyxl") as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Products"
        )

    return response

@login_required
def export_regions(request):

    regions = Region.objects.all()

    data = []

    for region in regions:

        data.append({

            "Region ID": region.RegionID,
            "Region Name": region.RegionName

        })

    df = pd.DataFrame(data)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="Regions.xlsx"'

    with pd.ExcelWriter(
        response,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Regions"
        )

    return response


@login_required
def lead_export(request):

    leads = Lead.objects.select_related(
        'ProductID',
        'RegionID'
    ).all()

    data = []

    for lead in leads:

        data.append({

            "LeadID": lead.LeadID,
            "PersonName": lead.PersonName,
            "CompanyName": lead.CompanyName,
            "Email": lead.Email,
            "ContactNo": lead.ContactNo,
            "Product": lead.ProductID.ProductName,
            "Region": lead.RegionID.RegionName,
            "Status": lead.StatusID.StatusName if lead.StatusID else "",
            "LeadSource": lead.LeadSourceID.SourceName if lead.LeadSourceID else ""

        })

    df = pd.DataFrame(data)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="Lead_List.xlsx"'

    df.to_excel(
        response,
        index=False,
        engine="openpyxl"
    )

    return response