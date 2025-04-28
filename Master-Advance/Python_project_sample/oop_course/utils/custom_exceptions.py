"""
Custom exceptions for the Python OOP course.

This module defines custom exception classes used across the course examples.
"""


class ValidationError(Exception):
    """
    Exception raised for validation errors.
    
    Attributes:
        field (str): Field with the validation error
        message (str): Explanation of the error
    """
    
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"Validation error in field '{field}': {message}")


class ResourceNotFoundError(Exception):
    """
    Exception raised when a requested resource is not found.
    
    Attributes:
        resource_type (str): Type of resource (e.g., 'file', 'database record')
        resource_id (str): Identifier of the resource
        message (str): Optional additional message
    """
    
    def __init__(self, resource_type, resource_id, message=None):
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.message = message
        
        error_msg = f"{resource_type} with id '{resource_id}' not found"
        if message:
            error_msg += f": {message}"
        
        super().__init__(error_msg)


class AuthorizationError(Exception):
    """
    Exception raised when an operation is not authorized.
    
    Attributes:
        user (str): User identifier
        operation (str): Operation attempted
        resource (str): Resource on which operation was attempted
    """
    
    def __init__(self, user, operation, resource):
        self.user = user
        self.operation = operation
        self.resource = resource
        
        error_msg = f"User '{user}' not authorized to {operation} on {resource}"
        super().__init__(error_msg)


class ConfigurationError(Exception):
    """
    Exception raised for configuration errors.
    
    Attributes:
        component (str): Component with configuration issue
        message (str): Description of the configuration problem
    """
    
    def __init__(self, component, message):
        self.component = component
        self.message = message
        super().__init__(f"Configuration error in {component}: {message}")


class DataProcessingError(Exception):
    """
    Exception raised during data processing.
    
    Attributes:
        source (str): Source of the data
        stage (str): Processing stage where error occurred
        message (str): Description of the error
        original_error (Exception, optional): Original exception that caused this error
    """
    
    def __init__(self, source, stage, message, original_error=None):
        self.source = source
        self.stage = stage
        self.message = message
        self.original_error = original_error
        
        error_msg = f"Error processing data from '{source}' at stage '{stage}': {message}"
        if original_error:
            error_msg += f" (Original error: {str(original_error)})"
        
        super().__init__(error_msg)


if __name__ == "__main__":
    # Example usage
    try:
        raise ValidationError("age", "must be a positive integer")
    except ValidationError as e:
        print(f"Caught exception: {e}")
    
    try:
        raise ResourceNotFoundError("User", "12345", "User account has been deleted")
    except ResourceNotFoundError as e:
        print(f"Caught exception: {e}") 