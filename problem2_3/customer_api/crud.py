from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from models import Customer, Order, Payment
from schema import CustomerCreate, CustomerUpdate
from logger import logger
from models import Product, Employee, Office, ProductLine, OrderDetail

# ============= CREATE OPERATIONS =============

def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    """
    Create a new customer in the database.
    
    Args:
        db: Database session
        customer: CustomerCreate schema with validated data
    
    Returns:
        Created Customer object
    """
    logger.info(f"Creating new customer: {customer.customerName}")
    
    try:
        # Convert Pydantic model to dict and create SQLAlchemy model
        db_customer = Customer(**customer.model_dump())
        
        # Add to session and commit
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)  # Refresh to get auto-generated customerNumber
        
        logger.info(f"Customer created successfully with ID: {db_customer.customerNumber}")
        return db_customer
    
    except Exception as e:
        logger.error(f"Failed to create customer: {e}")
        db.rollback()
        raise


# ============= READ OPERATIONS =============

def get_customer(db: Session, customer_number: int) -> Optional[Customer]:
    """
    Retrieve a single customer by their customer number.
    Includes related orders and payments using eager loading.
    
    Args:
        db: Database session
        customer_number: Customer's unique ID
    
    Returns:
        Customer object if found, None otherwise
    """
    logger.info(f"Fetching customer with ID: {customer_number}")
    
    try:
        # Use joinedload to eagerly load relationships (prevents N+1 queries)
        customer = db.query(Customer).options(
            joinedload(Customer.orders),
            joinedload(Customer.payments)
        ).filter(Customer.customerNumber == customer_number).first()
        
        if customer:
            logger.info(f"Customer {customer_number} found: {customer.customerName}")
        else:
            logger.warning(f"Customer {customer_number} not found")
        
        return customer
    
    except Exception as e:
        logger.error(f"Error fetching customer {customer_number}: {e}")
        raise


def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
    """
    Retrieve a list of customers with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
    
    Returns:
        List of Customer objects
    """
    logger.info(f"Fetching customers with skip={skip}, limit={limit}")
    
    try:
        customers = db.query(Customer).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(customers)} customers")
        return customers
    
    except Exception as e:
        logger.error(f"Error fetching customers: {e}")
        raise


def get_customers_count(db: Session) -> int:
    """
    Get total count of customers in database.
    Useful for pagination metadata.
    
    Returns:
        Total number of customers
    """
    try:
        count = db.query(func.count(Customer.customerNumber)).scalar()
        logger.info(f"Total customers in database: {count}")
        return count
    
    except Exception as e:
        logger.error(f"Error counting customers: {e}")
        raise


# ============= UPDATE OPERATIONS =============

def update_customer(
    db: Session, 
    customer_number: int, 
    customer_update: CustomerUpdate
) -> Optional[Customer]:
    """
    Update an existing customer's information.
    Only updates fields that are provided (not None).
    
    Args:
        db: Database session
        customer_number: Customer's unique ID
        customer_update: CustomerUpdate schema with new values
    
    Returns:
        Updated Customer object if found, None otherwise
    """
    logger.info(f"Updating customer {customer_number}")
    
    try:
        # First, fetch the customer
        db_customer = db.query(Customer).filter(
            Customer.customerNumber == customer_number
        ).first()
        
        if not db_customer:
            logger.warning(f"Customer {customer_number} not found for update")
            return None
        
        # Update only the fields that were provided (not None)
        update_data = customer_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        
        db.commit()
        db.refresh(db_customer)
        
        logger.info(f"Customer {customer_number} updated successfully")
        return db_customer
    
    except Exception as e:
        logger.error(f"Failed to update customer {customer_number}: {e}")
        db.rollback()
        raise


# ============= DELETE OPERATIONS =============

def delete_customer(db: Session, customer_number: int) -> bool:
    """
    Delete a customer from the database.
    
    Args:
        db: Database session
        customer_number: Customer's unique ID
    
    Returns:
        True if deleted, False if customer not found
    """
    logger.info(f"Attempting to delete customer {customer_number}")
    
    try:
        db_customer = db.query(Customer).filter(
            Customer.customerNumber == customer_number
        ).first()
        
        if not db_customer:
            logger.warning(f"Customer {customer_number} not found for deletion")
            return False
        
        db.delete(db_customer)
        db.commit()
        
        logger.info(f"Customer {customer_number} deleted successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to delete customer {customer_number}: {e}")
        db.rollback()
        raise
# ============= COUNT OPERATIONS FOR DASHBOARD =============


def get_customers_count(db: Session) -> int:
    """Get total count of customers"""
    logger.info("Querying customers count")
    try:
        count = db.query(func.count(Customer.customerNumber)).scalar()
        logger.info(f"Customers count: {count}")
        return count or 0
    except Exception as e:
        logger.error(f"Error counting customers: {e}")
        raise


def get_orders_count(db: Session) -> int:
    """Get total count of orders"""
    logger.info("Querying orders count")
    try:
        count = db.query(func.count(Order.orderNumber)).scalar()
        logger.info(f"Orders count: {count}")
        return count or 0
    except Exception as e:
        logger.error(f"Error counting orders: {e}")
        raise


def get_products_count(db: Session) -> int:
    """Get total count of products"""
    logger.info("Querying products count")
    try:
        count = db.query(func.count(Product.productCode)).scalar()
        logger.info(f"Products count: {count}")
        return count or 0
    except Exception as e:
        logger.error(f"Error counting products: {e}")
        raise


def get_employees_count(db: Session) -> int:
    """Get total count of employees"""
    logger.info("Querying employees count")
    try:
        count = db.query(func.count(Employee.employeeNumber)).scalar()
        logger.info(f"Employees count: {count}")
        return count or 0
    except Exception as e:
        logger.error(f"Error counting employees: {e}")
        raise


def get_offices_count(db: Session) -> int:
    """Get total count of offices"""
    logger.info("Querying offices count")
    try:
        count = db.query(func.count(Office.officeCode)).scalar()
        logger.info(f"Offices count: {count}")
        return count or 0
    except Exception as e:
        logger.error(f"Error counting offices: {e}")
        raise


def get_payments_count(db: Session) -> int:
    """Get total count of payments"""
    logger.info("Querying payments count")
    try:
        count = db.query(func.count(Payment.checkNumber)).scalar()
        logger.info(f"Payments count: {count}")
        return count or 0
    except Exception as e:
        logger.error(f"Error counting payments: {e}")
        raise


def get_orderdetails_count(db: Session) -> int:
    """Get total count of order details"""
    logger.info("Querying orderdetails count")
    try:
        count = db.query(func.count(OrderDetail.orderNumber)).scalar()
        logger.info(f"Order details count: {count}")
        return count or 0
    except Exception as e:
        logger.error(f"Error counting order details: {e}")
        raise


def get_productlines_count(db: Session) -> int:
    """Get total count of product lines"""
    logger.info("Querying productlines count")
    try:
        count = db.query(func.count(ProductLine.productLine)).scalar()
        logger.info(f"Product lines count: {count}")
        return count or 0
    except Exception as e:
        logger.error(f"Error counting product lines: {e}")
        raise