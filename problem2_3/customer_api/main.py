from fastapi import FastAPI
from router import router as customer_router
from logger import logger

# Create FastAPI application
app = FastAPI(
    title="Customer API",
    description="A RESTful API for managing customer data with related orders and payments",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc UI
)

# Include the customer router
app.include_router(customer_router)

# Root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint - returns API information
    """
    logger.info("GET / - Root endpoint accessed")
    return {
        "message": "Customer API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "customers": "/customers",
            "dashboard": "/overall_counts",
            "individual_counts": [
                "/customers/count",
                "/orders/count",
                "/products/count",
                "/employees/count",
                "/offices/count",
                "/payments/count",
                "/orderdetails/count",
                "/productlines/count"
            ]
        }
    }

# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Customer API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)