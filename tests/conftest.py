"""Test configuration and fixtures for SaaS Analytics Platform."""

import pytest
from pathlib import Path
from typing import Dict, Any
import json


# Session-level fixtures
@pytest.fixture(scope="session")
def project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def test_data_dir(project_root: Path) -> Path:
    """Get test data directory."""
    return project_root / "tests" / "fixtures"


@pytest.fixture(scope="session")
def sample_customer() -> Dict[str, Any]:
    """Sample customer record for testing."""
    return {
        "customer_id": "CUST_001",
        "customer_name": "Acme Corporation",
        "email": "contact@acme.com",
        "country": "US",
        "segment": "Enterprise",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-11-01T00:00:00Z"
    }


@pytest.fixture(scope="session")
def sample_subscription() -> Dict[str, Any]:
    """Sample subscription record for testing."""
    return {
        "subscription_id": "SUB_001",
        "customer_id": "CUST_001",
        "product_id": "PROD_001",
        "monthly_amount": 999.99,
        "status": "active",
        "start_date": "2024-01-01",
        "end_date": None,
        "renewal_date": "2025-01-01"
    }


@pytest.fixture(scope="session")
def sample_invoice() -> Dict[str, Any]:
    """Sample invoice record for testing."""
    return {
        "invoice_id": "INV_001",
        "subscription_id": "SUB_001",
        "customer_id": "CUST_001",
        "invoice_amount": 999.99,
        "invoice_date": "2024-01-01",
        "due_date": "2024-01-31",
        "invoice_status": "paid"
    }


@pytest.fixture(scope="session")
def sample_payment() -> Dict[str, Any]:
    """Sample payment record for testing."""
    return {
        "payment_id": "PAY_001",
        "invoice_id": "INV_001",
        "payment_amount": 999.99,
        "payment_date": "2024-01-15",
        "payment_method": "credit_card",
        "payment_status": "completed"
    }


@pytest.fixture(scope="session")
def sample_usage() -> Dict[str, Any]:
    """Sample product usage record for testing."""
    return {
        "usage_id": "USG_001",
        "customer_id": "CUST_001",
        "product_id": "PROD_001",
        "event_type": "login",
        "event_date": "2024-11-01",
        "event_count": 5
    }


# Configuration and markers
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "requires_snowflake: mark test as requiring Snowflake connection"
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow to run"
    )
    config.addinivalue_line(
        "markers",
        "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test"
    )


# Hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection."""
    for item in items:
        # Mark all tests in tests/unit as unit tests
        if "tests/unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Mark all tests in tests/integration as integration tests
        if "tests/integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
