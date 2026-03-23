from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities_state():
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))


@pytest.fixture
def client():
    return TestClient(app)
