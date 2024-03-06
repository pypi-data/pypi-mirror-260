import pytest
import functools
import sys 
import os 

import warnings
from pdeprecator import deprecated_params

# Define a function to be decorated
@deprecated_params({"old_param": "new_param"})
def test_function(**kwargs):
    return kwargs.get("new_param")

def test_deprecated_params():
    # Call the decorated function with deprecated parameter
    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered
        warnings.simplefilter("always")

        # Call the decorated function with deprecated parameter
        result = test_function(old_param="value")

        # Verify that the deprecated parameter warning is issued
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "Parameter 'old_param' is deprecated. Use 'new_param' instead." in str(w[-1].message)

        # Verify that the function still works and returns the expected result
        assert result == "value"