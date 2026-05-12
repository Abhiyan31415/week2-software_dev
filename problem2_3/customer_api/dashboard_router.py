from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from logger import logger
import asyncio
import time

# Create router for dashboard endpoints
router = APIRouter(
    prefix="",
    tags=["dashboard"]
)


# ============= INDIVIDUAL COUNT ENDPOINTS =============

@router.get("/customers/count")
def count_customers(db: Session = Depends(get_db)):
    """Get total count of customers"""
    logger.info("GET /customers/count - Request received")
    try:
        count = crud.get_customers_count(db)
        logger.info(f"GET /customers/count - Success: {count}")
        return {"table": "customers", "count": count}
    except Exception as e:
        logger.error(f"GET /customers/count - Error: {e}")
        raise


@router.get("/orders/count")
def count_orders(db: Session = Depends(get_db)):
    """Get total count of orders"""
    logger.info("GET /orders/count - Request received")
    try:
        count = crud.get_orders_count(db)
        logger.info(f"GET /orders/count - Success: {count}")
        return {"table": "orders", "count": count}
    except Exception as e:
        logger.error(f"GET /orders/count - Error: {e}")
        raise


@router.get("/products/count")
def count_products(db: Session = Depends(get_db)):
    """Get total count of products"""
    logger.info("GET /products/count - Request received")
    try:
        count = crud.get_products_count(db)
        logger.info(f"GET /products/count - Success: {count}")
        return {"table": "products", "count": count}
    except Exception as e:
        logger.error(f"GET /products/count - Error: {e}")
        raise


@router.get("/employees/count")
def count_employees(db: Session = Depends(get_db)):
    """Get total count of employees"""
    logger.info("GET /employees/count - Request received")
    try:
        count = crud.get_employees_count(db)
        logger.info(f"GET /employees/count - Success: {count}")
        return {"table": "employees", "count": count}
    except Exception as e:
        logger.error(f"GET /employees/count - Error: {e}")
        raise


@router.get("/offices/count")
def count_offices(db: Session = Depends(get_db)):
    """Get total count of offices"""
    logger.info("GET /offices/count - Request received")
    try:
        count = crud.get_offices_count(db)
        logger.info(f"GET /offices/count - Success: {count}")
        return {"table": "offices", "count": count}
    except Exception as e:
        logger.error(f"GET /offices/count - Error: {e}")
        raise


@router.get("/payments/count")
def count_payments(db: Session = Depends(get_db)):
    """Get total count of payments"""
    logger.info("GET /payments/count - Request received")
    try:
        count = crud.get_payments_count(db)
        logger.info(f"GET /payments/count - Success: {count}")
        return {"table": "payments", "count": count}
    except Exception as e:
        logger.error(f"GET /payments/count - Error: {e}")
        raise


@router.get("/orderdetails/count")
def count_orderdetails(db: Session = Depends(get_db)):
    """Get total count of order details"""
    logger.info("GET /orderdetails/count - Request received")
    try:
        count = crud.get_orderdetails_count(db)
        logger.info(f"GET /orderdetails/count - Success: {count}")
        return {"table": "orderdetails", "count": count}
    except Exception as e:
        logger.error(f"GET /orderdetails/count - Error: {e}")
        raise


@router.get("/productlines/count")
def count_productlines(db: Session = Depends(get_db)):
    """Get total count of product lines"""
    logger.info("GET /productlines/count - Request received")
    try:
        count = crud.get_productlines_count(db)
        logger.info(f"GET /productlines/count - Success: {count}")
        return {"table": "productlines", "count": count}
    except Exception as e:
        logger.error(f"GET /productlines/count - Error: {e}")
        raise


# ============= AGGREGATED CONCURRENT ENDPOINT =============

async def fetch_count(count_function, db: Session, table_name: str):
    """
    Async wrapper to fetch count from database.
    Runs synchronous database queries in thread pool.
    """
    logger.info(f"Starting concurrent query for {table_name}")
    # Run blocking database query in thread pool
    loop = asyncio.get_event_loop()
    count = await loop.run_in_executor(None, count_function, db)
    logger.info(f"Completed concurrent query for {table_name}: {count}")
    return count


@router.get("/overall_counts")
async def get_overall_counts(db: Session = Depends(get_db)):
    """
    Aggregated dashboard endpoint - fetches all table counts concurrently.
    
    This endpoint demonstrates Factor VIII: Concurrency
    - All 8 database queries run simultaneously
    - Uses asyncio.gather() to coordinate parallel execution
    - Much faster than sequential queries
    """
    logger.info("GET /overall_counts - Request received")
    start_time = time.time()
    
    logger.info("Starting all 8 concurrent count queries")
    
    try:
        # Launch all 8 queries simultaneously using asyncio.gather()
        customers, orders, products, employees, offices, payments, orderdetails, productlines = await asyncio.gather(
            fetch_count(crud.get_customers_count, db, "customers"),
            fetch_count(crud.get_orders_count, db, "orders"),
            fetch_count(crud.get_products_count, db, "products"),
            fetch_count(crud.get_employees_count, db, "employees"),
            fetch_count(crud.get_offices_count, db, "offices"),
            fetch_count(crud.get_payments_count, db, "payments"),
            fetch_count(crud.get_orderdetails_count, db, "orderdetails"),
            fetch_count(crud.get_productlines_count, db, "productlines"),
        )
        
        elapsed_time = time.time() - start_time
        logger.info(f"All concurrent queries completed in {elapsed_time:.3f} seconds")
        
        response = {
            "customers": customers,
            "orders": orders,
            "products": products,
            "employees": employees,
            "offices": offices,
            "payments": payments,
            "orderdetails": orderdetails,
            "productlines": productlines
        }
        
        logger.info(f"GET /overall_counts - Success: {response}")
        return response
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.error(f"GET /overall_counts - Error after {elapsed_time:.3f}s: {e}")
        raise