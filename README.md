# Shoe Inventory Program

A command-line inventory management application built in Python.  
The program allows users to manage shoe stock data stored in a persistent text file, using a structured, object-oriented approach.

## Overview

This project demonstrates practical use of:

- Object-Oriented Programming (OOP)
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

- Clean class-based design (`Shoe` class)
- Type hints for clarity
- Input validation for numeric fields
- Graceful handling of missing or malformed files
- Structured, readable output formatting

## How to Run

```bash
python main.py
