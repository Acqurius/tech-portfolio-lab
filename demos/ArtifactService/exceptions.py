"""
Custom exceptions for Artifact Service
"""


class ArtifactServiceError(Exception):
    """Base exception for Artifact Service"""
    pass


class ArtifactNotFoundError(ArtifactServiceError):
    """Raised when artifact is not found"""
    pass


class StorageError(ArtifactServiceError):
    """Raised when storage operation fails"""
    pass


class ValidationError(ArtifactServiceError):
    """Raised when input validation fails"""
    pass


class ConfigurationError(ArtifactServiceError):
    """Raised when configuration is invalid"""
    pass
