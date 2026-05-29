"""
pytest configuration for Constitutional Engine tests.
Provides markers, fixtures setup, and test execution options.
"""

def pytest_configure(config):
    """Configure custom pytest markers."""
    # Register custom markers
    config.addinivalue_line(
        "markers", 
        "law(number): mark test as testing a specific constitutional law"
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow-running (for CI exclusion)"
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test requiring external services"
    )
    config.addinivalue_line(
        "markers",
        "enterprise: mark test as enterprise-grade validation"
    )
