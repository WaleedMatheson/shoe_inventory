# Shoe Inventory Program

A command-line inventory management application built in Python.  
The program allows users to manage shoe stock data stored in a persistent text file, using a highly structured, object-oriented approach.

## Overview

This project demonstrates practical use of:

- Object-Oriented Programming (OOP) principles (Encapsulation and Composition)
- File handling with `pathlib`
- Exception handling
- Data validation
- CLI menu design
- Use of built-in functions such as `min()` and `max()`

Inventory data is stored in a CSV-formatted `inventory.txt` file and updated dynamically as users interact with the system.

## Core Functionality

- View full inventory
- Search for a product by SKU
- Add new products
- Restock the lowest-quantity item
- Calculate total value per product (cost × quantity)
- Identify highest-quantity stock item

All updates persist to file storage.

## Technical Highlights

- **Clean class-based design:** Utilises a `Shoe` class for individual items and an `Inventory` class to manage the collection and file operations.
- **Dynamic attributes:** Uses the Python `@property` decorator to dynamically calculate shoe values on the fly.
- **Data Encapsulation:** Centralizes file reading, writing, and error handling entirely within the `Inventory` object.
- **Type hints:** Ensures code clarity and developer readability.
- **Input validation:** Safely handles numeric fields and prevents crashes from bad user input.
- **Graceful error handling:** Detects missing or malformed files and provides clean terminal exits.

## How to Run

```bash
python main.py
