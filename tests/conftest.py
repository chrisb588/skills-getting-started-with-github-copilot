import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Reset the activities database before and after each test.
    This ensures test isolation—each test starts with a clean state.
    """
    # Store the original state
    original_activities = copy.deepcopy(activities)
    
    # Clear and restore original activities
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup: restore to original state after test
    activities.clear()
    activities.update(original_activities)
