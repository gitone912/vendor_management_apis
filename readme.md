### 1. Overview

**Vendor Management System** is a web application developed using Django and Django REST Framework. The system helps manage vendor profiles, track purchase orders, and calculate vendor performance metrics. By using the application, you can maintain a comprehensive database of vendors, manage purchase orders, and evaluate vendor performance based on various metrics such as on-time delivery rate, quality rating average, average response time, and fulfillment rate.

### 2. Setup

This section provides instructions for setting up the Vendor Management System web application.

#### Prerequisites

Before you begin, make sure you have the following prerequisites installed:

- **Python**: The application requires Python 3.10 or higher.
- **Django**: The application uses the latest stable version of Django.
- **Django REST Framework**: Ensure you have the latest stable version installed.

#### Installation

1. **Clone the repository**: Clone the project's Git repository to your local machine.

   ```shell
   git clone https://github.com/gitone912/vendor_management_apis.git
   ```
3. **Create a virtual environment**: Use Python's virtual environment to manage dependencies.

   ```shell
   python3 -m venv venv
   ```
4. **Activate the virtual environment**: Activate the virtual environment.

   - On macOS/Linux:

     ```shell
     source venv/bin/activate
     ```
   - On Windows:

     ```shell
     venv\Scripts\activate
     ```
5. **Install dependencies**: Install the necessary packages from the `requirements.txt` file.

   ```shell
   pip install -r requirements.txt
   ```
6. **Set up the database**: Configure the database settings in the `settings.py` file. By default, the application is set up to use a local SQLite database. For production use, we recommend configuring the application to use a PostgreSQL database.
7. **Run migrations**: Apply database migrations.

   ```shell
   python manage.py migrate
   ```
8. **Start the development server**: Launch the Django development server.

   ```shell
   python manage.py runserver
   ```

#### Configuration (optional , it will work on default sql lite with no auth)

- **Database**: Modify the `DATABASES` setting in `settings.py` to specify the database you want to use.
- **Authentication**: You may need to configure authentication settings in `settings.py` depending on your requirements. (optional))
- **Other Settings**: Modify other settings such as `ALLOWED_HOSTS` and `DEBUG` based on your deployment environment.

### 3. Features

The Vendor Management System web application offers the following core features:

#### Vendor Profile Management

- **Create Vendors**: Allows you to create new vendor profiles, providing details such as name, contact information, and address.
- **List Vendors**: Lists all vendors in the system.
- **Retrieve Vendor Details**: Allows you to retrieve information about a specific vendor by its ID.
- **Update Vendors**: Enables updating vendor information such as name, contact details, and address.
- **Delete Vendors**: Allows you to delete a vendor from the system.

#### Purchase Order Tracking

- **Create Purchase Orders**: Enables you to create new purchase orders, including order details and vendor references.
- **List Purchase Orders**: Lists all purchase orders in the system with options to filter by vendor.
- **Retrieve Purchase Order Details**: Allows you to retrieve information about a specific purchase order by its ID.
- **Update Purchase Orders**: Enables you to update purchase order details such as status and acknowledgment date.
- **Delete Purchase Orders**: Allows you to delete a purchase order from the system.

#### Vendor Performance Evaluation

- **Performance Metrics**: Calculates and tracks metrics for vendors such as on-time delivery rate, quality rating average, average response time, and fulfillment rate.
- **Retrieve Vendor Performance**: Allows you to retrieve performance metrics for a specific vendor.

These features enable you to effectively manage vendors, track purchase orders, and evaluate vendor performance in the application.

### 4. Data Models ( a whole API document is published here [link](https://documenter.getpostman.com/view/27958555/2sA3JFBQT6) )

The web application uses several data models to represent vendors, purchase orders, and historical performance data.

#### Vendor Model

The `Vendor` model stores essential information about each vendor and their performance metrics.

- **Fields**:
  - `name`: A `CharField` representing the vendor's name.
  - `contact_details`: A `TextField` representing the vendor's contact information.
  - `address`: A `TextField` representing the vendor's physical address.
  - `vendor_code`: A `CharField` representing a unique identifier for the vendor.
  - `on_time_delivery_rate`: A `FloatField` representing the percentage of on-time deliveries.
  - `quality_rating_avg`: A `FloatField` representing the average rating of quality based on purchase orders.
  - `average_response_time`: A `FloatField` representing the average time taken to acknowledge purchase orders.
  - `fulfillment_rate`: A `FloatField` representing the percentage of purchase orders fulfilled successfully.

#### Purchase Order Model

The `Purchase Order` model captures the details of each purchase order and is used to calculate various performance metrics.

- **Fields**:
  - `po_number`: A `CharField` representing a unique identifier for the purchase order.
  - `vendor`: A `ForeignKey` linking to the `Vendor` model.
  - `order_date`: A `DateTimeField` representing the date when the order was placed.
  - `delivery_date`: A `DateTimeField` representing the expected or actual delivery date of the order.
  - `items`: A `JSONField` representing details of items ordered (e.g., name and quantity).
  - `quantity`: An `IntegerField` representing the total quantity of items in the purchase order.
  - `status`: A `CharField` representing the current status of the purchase order (e.g., pending, completed, canceled).
  - `quality_rating`: A `FloatField` representing the rating given to the vendor for the purchase order (nullable).
  - `issue_date`: A `DateTimeField` representing the date when the purchase order was issued to the vendor.
  - `acknowledgment_date`: A `DateTimeField` (nullable) representing the date when the vendor acknowledged the purchase order.

#### Historical Performance Model

The `Historical Performance` model stores historical data on vendor performance, enabling trend analysis.

- **Fields**:
  - `vendor`: A `ForeignKey` linking to the `Vendor` model.
  - `date`: A `DateTimeField` representing the date of the performance record.
  - `on_time_delivery_rate`: A `FloatField` representing the historical record of the on-time delivery rate.
  - `quality_rating_avg`: A `FloatField` representing the historical record of the quality rating average.
  - `average_response_time`: A `FloatField` representing the historical record of the average response time.
  - `fulfillment_rate`: A `FloatField` representing the historical record of the fulfillment rate.

### 5. API Endpoints

The web application provides several RESTful API endpoints for managing vendors and purchase orders, as well as retrieving vendor performance metrics.

#### Vendor Endpoints

- **Create Vendor**: `POST /api/vendors/`
  - Creates a new vendor. Requires a JSON body with the vendor's name, contact details, address, and vendor code.
- **List Vendors**: `GET /api/vendors/`
  - Lists all vendors in the system.
- **Retrieve Vendor**: `GET /api/vendors/<int:pk>/`
  - Retrieves details of a specific vendor by its ID (`pk`).
- **Update Vendor**: `PUT /api/vendors/<int:pk>/`
  - Updates a specific vendor's details by its ID (`pk`). Requires a JSON body with the updated vendor information.
- **Delete Vendor**: `DELETE /api/vendors/<int:pk>/`
  - Deletes a specific vendor by its ID (`pk`).

#### Purchase Order Endpoints

- **Create Purchase Order**: `POST /api/purchase_orders/`
  - Creates a new purchase order. Requires a JSON body with purchase order details such as PO number, vendor, order date, delivery date, items, quantity, and status.
- **List Purchase Orders**: `GET /api/purchase_orders/`
  - Lists all purchase orders in the system with an option to filter by vendor.
- **Retrieve Purchase Order**: `GET /api/purchase_orders/<int:pk>/`
  - Retrieves details of a specific purchase order by its ID (`pk`).
- **Update Purchase Order**: `PUT /api/purchase_orders/<int:pk>/`
  - Updates a specific purchase order by its ID (`pk`). Requires a JSON body with the updated purchase order details.
- **Delete Purchase Order**: `DELETE /api/purchase_orders/<int:pk>/`
  - Deletes a specific purchase order by its ID (`pk`).

#### Vendor Performance Endpoint

- **Retrieve Vendor Performance**: `GET /api/vendors/<int:pk>/performance/`
  - Retrieves performance metrics for a specific vendor by its ID (`pk`). The response includes data such as on-time delivery rate, quality rating average, average response time, and fulfillment rate.

#### Purchase Order Acknowledgment Endpoint

- **Acknowledge Purchase Order**: `POST /api/purchase_orders/<int:pk>/acknowledge/`
  - Acknowledges a purchase order by updating its acknowledgment date. Requires a JSON body with the acknowledgment date.
