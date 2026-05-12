from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schema import CustomerOut, CustomerCreate, CustomerUpdate, CustomerListOut
import crud
from logger import logger

# Create router instance
router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)


@router.get("/", response_model=List[CustomerListOut])
def list_customers(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    List all customers with pagination.
    
    **Query Parameters:**
    - skip: Starting point (default: 0)
    - limit: Number of results (default: 100, max: 500)
    
    **Returns:** List of customers without related data
    """
    logger.info(f"GET /customers - skip={skip}, limit={limit}")
    
    try:
        customers = crud.get_customers(db, skip=skip, limit=limit)
        total = crud.get_customers_count(db)
        
        logger.info(f"Returning {len(customers)} customers out of {total} total")
        return customers
    
    except Exception as e:
        logger.error(f"Error in list_customers endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{customer_number}", response_model=CustomerOut)
def get_customer(
    customer_number: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific customer.
    
    **Path Parameters:**
    - customer_number: Unique customer ID
    
    **Returns:** Customer data including orders and payments
    **Raises:** 404 if customer not found
    """
    logger.info(f"GET /customers/{customer_number}")
    
    try:
        customer = crud.get_customer(db, customer_number=customer_number)
        
        if customer is None:
            logger.warning(f"Customer {customer_number} not found - returning 404")
            raise HTTPException(
                status_code=404,
                detail=f"Customer with number {customer_number} not found"
            )
        
        logger.info(f"Successfully retrieved customer {customer_number}")
        return customer
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        logger.error(f"Error in get_customer endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/", response_model=CustomerOut, status_code=201)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new customer.
    
    **Request Body:** Customer data (customerNumber is auto-generated)
    **Returns:** Created customer with generated ID
    **Status Code:** 201 Created
    """
    logger.info(f"POST /customers - Creating customer: {customer.customerName}")
    
    try:
        new_customer = crud.create_customer(db, customer=customer)
        logger.info(f"Customer created with ID: {new_customer.customerNumber}")
        return new_customer
    
    except Exception as e:
        logger.error(f"Error in create_customer endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to create customer")


@router.put("/{customer_number}", response_model=CustomerOut)
def update_customer(
    customer_number: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing customer's information.
    
    **Path Parameters:**
    - customer_number: Unique customer ID
    
    **Request Body:** Fields to update (all optional)
    **Returns:** Updated customer data
    **Raises:** 404 if customer not found
    """
    logger.info(f"PUT /customers/{customer_number}")
    
    try:
        updated_customer = crud.update_customer(
            db, 
            customer_number=customer_number, 
            customer_update=customer
        )
        
        if updated_customer is None:
            logger.warning(f"Customer {customer_number} not found for update - returning 404")
            raise HTTPException(
                status_code=404,
                detail=f"Customer with number {customer_number} not found"
            )
        
        logger.info(f"Customer {customer_number} updated successfully")
        return updated_customer
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_customer endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to update customer")


@router.delete("/{customer_number}", status_code=204)
def delete_customer(
    customer_number: int,
    db: Session = Depends(get_db)
):
    """
    Delete a customer.
    
    **Path Parameters:**
    - customer_number: Unique customer ID
    
    **Returns:** No content on success
    **Status Code:** 204 No Content
    **Raises:** 404 if customer not found
    """
    logger.info(f"DELETE /customers/{customer_number}")
    
    try:
        success = crud.delete_customer(db, customer_number=customer_number)
        
        if not success:
            logger.warning(f"Customer {customer_number} not found for deletion - returning 404")
            raise HTTPException(
                status_code=404,
                detail=f"Customer with number {customer_number} not found"
            )
        
        logger.info(f"Customer {customer_number} deleted successfully")
        return None  # 204 No Content
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_customer endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete customer")