# Inventory Management System (IMS)

[![Python Flask](https://img.shields.io/badge/Python-Flask-blue.svg)](https://flask.palletsprojects.com/)

A full-stack, role-based Inventory Management System built with Flask, MySQL, and JavaScript. This application allows a business to manage its items, stock, orders, and users through a clean, responsive web interface.

**Live Demo:** [https://5kyscream.pythonanywhere.com/](https://5kyscream.pythonanywhere.com/)

## Features

* **Secure Authentication:** User registration and login system with hashed passwords (`bcrypt`).
* **Role-Based Access Control (RBAC):** Different permissions for `admin`, `manager`, `staff`, and `sales` roles.
* **Item Management (Admin/Manager):** Full CRUD (Create, Read, Update, Delete) functionality for inventory items.
* **Stock Management (Admin/Manager/Staff):** Add and update stock levels and locations for items.
* **Order Processing (All Roles):** Place new sales or purchase orders.
* **Reporting (Admin/Manager):** View a summary report of all stock.
* **Interactive UI:** Modern frontend with live table filtering and click-to-edit forms.

## System Design

This project was built from a set of software engineering blueprints, which can be found in the project documentation:

* **Class Diagram:** The database schema is a direct implementation of the UML Class Diagram, with tables for `User`, `Item`, `Stock`, and `Order`, and foreign keys to represent their relationships.
* **Data Flow Diagrams (DFDs):** The application's logic (`main.py`) implements the processes defined in the DFDs, such as "Order Processing" and "User Administration".
* **Sequence Diagram:** The login flow, for example, is a step-by-step implementation of the corresponding UML Sequence Diagram, showing the interaction between the User, FlaskApp, and Database.

## Technologies Used

* **Backend:** [Python](https://www.python.org/), [Flask](https://flask.palletsprojects.com/)
* **Database:** [MySQL](https://www.mysql.com/)
* **Frontend:** HTML5, CSS3, [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
* **Deployment:** [PythonAnywhere](https://www.pythonanywhere.com/)

## Setup and Installation (Local)

To run this project on your local machine, follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/5kyscream/inventory-management.git](https://github.com/5kyscream/inventory-management.git)
cd inventory-management
