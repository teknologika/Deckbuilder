#!/usr/bin/env python3
"""
Presentation Result Classes for Deckbuilder

Provides structured result objects for all presentation operations,
eliminating the need for exceptions on user input validation errors.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class PresentationResult:
    """
    Result object for presentation creation operations.

    Provides structured success/error information without throwing exceptions.
    """

    success: bool
    filename: Optional[str] = None
    slide_count: Optional[int] = None
    error_message: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = None

    @classmethod
    def success_result(cls, filename: str, slide_count: int) -> "PresentationResult":
        """Create a successful result."""
        return cls(success=True, filename=filename, slide_count=slide_count)

    @classmethod
    def error_result(cls, message: str, details: Optional[Dict[str, Any]] = None) -> "PresentationResult":
        """Create an error result."""
        return cls(success=False, error_message=message, error_details=details or {})

    @classmethod
    def yaml_error_result(cls, yaml_error: str, line_info: Optional[str] = None) -> "PresentationResult":
        """Create a YAML parsing error result with helpful context."""
        details = {"error_type": "yaml_parsing", "yaml_error": yaml_error}
        if line_info:
            details["line_info"] = line_info

        message = f"YAML syntax error in frontmatter: {yaml_error}"
        if line_info:
            message += f"\nLocation: {line_info}"
        message += "\n\nFix: Check YAML syntax - ensure proper indentation and formatting"

        return cls.error_result(message, details)

    @classmethod
    def validation_error_result(cls, validation_message: str, context: Optional[str] = None) -> "PresentationResult":
        """Create a validation error result."""
        details = {"error_type": "validation", "validation_message": validation_message}
        if context:
            details["context"] = context

        message = f"Content validation error: {validation_message}"
        if context:
            message += f"\nContext: {context}"

        return cls.error_result(message, details)

    @classmethod
    def content_error_result(cls, content_message: str, suggestion: Optional[str] = None) -> "PresentationResult":
        """Create a content processing error result."""
        details = {"error_type": "content_processing", "content_message": content_message}
        if suggestion:
            details["suggestion"] = suggestion

        message = f"Content processing error: {content_message}"
        if suggestion:
            message += f"\nSuggestion: {suggestion}"

        return cls.error_result(message, details)


@dataclass
class ValidationResult:
    """
    Result object for validation operations.

    Used internally for validation steps before presentation creation.
    """

    valid: bool
    errors: List[str]
    warnings: List[str]
    context: Optional[Dict[str, Any]] = None

    @classmethod
    def success_result(cls) -> "ValidationResult":
        """Create a successful validation result."""
        return cls(valid=True, errors=[], warnings=[])

    @classmethod
    def error_result(cls, errors: List[str], warnings: Optional[List[str]] = None) -> "ValidationResult":
        """Create a failed validation result."""
        return cls(valid=False, errors=errors, warnings=warnings or [])

    def add_error(self, error: str):
        """Add an error to the validation result."""
        self.errors.append(error)
        self.valid = False

    def add_warning(self, warning: str):
        """Add a warning to the validation result."""
        self.warnings.append(warning)
