# Lead Management System

A Django-based Lead Management System integrated with Microsoft SQL Server for managing Products, Regions, and Leads. The project includes both web-based CRUD operations and REST APIs with validations and error handling.

## Features

### Product Module

* Add Product
* Update Product
* Delete Product
* View Product List
* Product APIs (GET, POST, PUT, DELETE)

### Region Module

* Add Region
* Update Region
* Delete Region
* View Region List
* Region APIs (GET, POST, PUT, DELETE)

### Lead Module

* Add Lead
* Update Lead
* Delete Lead
* View Lead List
* Lead APIs (GET, POST, PUT, DELETE)

## Technologies Used

* Python
* Django
* Django REST Framework
* Microsoft SQL Server
* HTML
* Bootstrap
* Git & GitHub

## API Endpoints

### Product APIs

```text
GET     /api/products/
GET     /api/products/<id>/
POST    /api/products/create/
PUT     /api/products/update/<id>/
DELETE  /api/products/delete/<id>/
```

### Region APIs

```text
GET     /api/regions/
GET     /api/regions/<id>/
POST    /api/regions/create/
PUT     /api/regions/update/<id>/
DELETE  /api/regions/delete/<id>/
```

### Lead APIs

```text
GET     /api/leads/
GET     /api/leads/<id>/
POST    /api/leads/create/
PUT     /api/leads/update/<id>/
DELETE  /api/leads/delete/<id>/
```

## Validations Implemented

### Product

* Product Name required
* Product Name allows only alphabets and spaces
* Category required
* Is Active required

### Region

* Region Name required
* Region selection restricted to database values

### Lead

* Person Name validation
* Company Name validation
* Contact Number validation
* Email validation
* City validation
* State validation
* Executive ID validation
* Lead Generation Date validation
* Foreign Key validations

## Automatic Fields

* `Added_By` populated using Python `getpass`
* `Added_Dts` populated using Django `timezone.now()`

## Setup Instructions

### Clone Repository

```bash
git clone <repository-url>
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Server

```bash
python manage.py runserver
```

## Learning Outcomes

* Django CRUD Operations
* Django Forms
* Django REST Framework
* Serializer Validations
* API Development
* MSSQL Integration
* Git & GitHub Workflow
* Error Handling
* Database Relationships

## Team Project

Developed as part of an internship training program using Django, DRF, and Microsoft SQL Server.
