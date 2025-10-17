# Northwind Database Query Tool - Agent Instructions

This workspace contains a read-only SQL query tool for the Northwind database. The tool is designed to safely execute SELECT queries without risk of modifying the database, and only returns 10 rows maximum.  Always use the provided tool rather than trying to access the database directly.  Always provide the sql query you used in the response in nice formatted fenced blocks so that I can verify the results myself easily.

```bash
uv run query_northwind.py "SELECT COUNT(*) FROM orders"
```

## Schema

- **Categories**: CategoryID, CategoryName, Description, Picture
- **Customers**: CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax
- **Employees**: EmployeeID, LastName, FirstName, Title, TitleOfCourtesy, BirthDate, HireDate, Address, City, Region, PostalCode, Country, HomePhone, Extension, Photo, Notes, ReportsTo, PhotoPath
- **Orders**: OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry
- **Order Details**: OrderID, ProductID, UnitPrice, Quantity, Discount
- **Products**: ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued
- **Suppliers**: SupplierID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax, HomePage
- **Shippers**: ShipperID, CompanyName, Phone
- **Regions**: RegionID, RegionDescription
- **Territories**: TerritoryID, TerritoryDescription, RegionID
- **EmployeeTerritories**: EmployeeID, TerritoryID
- **CustomerCustomerDemo**: CustomerID, CustomerTypeID
- **CustomerDemographics**: CustomerTypeID, CustomerDesc
