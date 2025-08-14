"""
JSON Schema for Pattern File Validation

This module provides JSON schema validation for pattern files to ensure
they follow the correct structure and contain required fields.
"""

import json
import jsonschema
from typing import Dict, Any, List
from pathlib import Path


class PatternSchemaValidator:
    """Validates pattern files against JSON schema."""

    def __init__(self):
        self.schema = self._get_pattern_schema()

    def _get_pattern_schema(self) -> Dict[str, Any]:
        """Define the JSON schema for pattern files."""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Pattern File Schema",
            "description": "Schema for structured frontmatter pattern files",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Human-readable description of the layout",
                    "minLength": 10,
                    "maxLength": 500,
                },
                "yaml_pattern": {
                    "type": "object",
                    "description": "YAML pattern defining the layout structure",
                    "properties": {
                        "layout": {
                            "type": "string",
                            "description": "Layout name matching PowerPoint template",
                            "minLength": 1,
                            "maxLength": 100,
                        }
                    },
                    "required": ["layout"],
                    "additionalProperties": {
                        "type": "string",
                        "enum": ["str", "int", "bool", "list"],
                    },
                },
                "validation": {
                    "type": "object",
                    "description": "Validation rules for pattern fields",
                    "properties": {
                        "required_fields": {
                            "type": "array",
                            "description": "List of required field names",
                            "items": {"type": "string", "minLength": 1},
                            "uniqueItems": True,
                        },
                        "optional_fields": {
                            "type": "array",
                            "description": "List of optional field names",
                            "items": {"type": "string", "minLength": 1},
                            "uniqueItems": True,
                        },
                        "field_types": {
                            "type": "object",
                            "description": "Field type definitions",
                            "additionalProperties": {
                                "type": "string",
                                "enum": ["string", "integer", "number", "boolean", "array", "object"],
                            },
                        },
                    },
                    "required": ["required_fields"],
                    "additionalProperties": False,
                },
                "example": {
                    "type": "string",
                    "description": "Example markdown with frontmatter",
                    "minLength": 10,
                },
            },
            "required": ["description", "yaml_pattern", "validation", "example"],
            "additionalProperties": False,
        }

    def validate_pattern(self, pattern_data: Dict[str, Any]) -> List[str]:
        """
        Validate a pattern against the schema.

        Args:
            pattern_data: Pattern data to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        try:
            # Basic schema validation
            jsonschema.validate(pattern_data, self.schema)

            # Additional semantic validation
            semantic_errors = self._validate_semantic_rules(pattern_data)
            errors.extend(semantic_errors)

        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")

        return errors

    def _validate_semantic_rules(self, pattern_data: Dict[str, Any]) -> List[str]:
        """Validate semantic rules beyond basic schema."""
        errors = []

        yaml_pattern = pattern_data.get("yaml_pattern", {})
        validation = pattern_data.get("validation", {})

        # Check that all required fields are in yaml_pattern
        required_fields = validation.get("required_fields", [])
        yaml_fields = set(yaml_pattern.keys()) - {"layout"}

        for field in required_fields:
            if field not in yaml_fields:
                errors.append(f"Required field '{field}' not found in yaml_pattern")

        # Check that optional fields are in yaml_pattern
        optional_fields = validation.get("optional_fields", [])
        for field in optional_fields:
            if field not in yaml_fields:
                errors.append(f"Optional field '{field}' not found in yaml_pattern")

        # Check for duplicate fields between required and optional
        required_set = set(required_fields)
        optional_set = set(optional_fields)
        duplicates = required_set & optional_set
        if duplicates:
            errors.append(f"Fields appear in both required and optional: {list(duplicates)}")

        # Validate field types consistency
        field_types = validation.get("field_types", {})
        for field, field_type in field_types.items():
            if field in yaml_pattern:
                yaml_type = yaml_pattern[field]
                if not self._types_compatible(yaml_type, field_type):
                    errors.append(f"Field '{field}' type mismatch: yaml_pattern='{yaml_type}', field_types='{field_type}'")

        # Validate example contains layout
        example = pattern_data.get("example", "")
        layout_name = yaml_pattern.get("layout", "")
        if layout_name and f"layout: {layout_name}" not in example:
            errors.append(f"Example does not contain 'layout: {layout_name}'")

        return errors

    def _types_compatible(self, yaml_type: str, field_type: str) -> bool:
        """Check if yaml_pattern type is compatible with field_types type."""
        type_mapping = {"str": "string", "int": "integer", "number": "number", "bool": "boolean", "list": "array", "dict": "object"}
        return type_mapping.get(yaml_type) == field_type

    def validate_pattern_file(self, file_path: Path) -> List[str]:
        """
        Validate a pattern file.

        Args:
            file_path: Path to pattern file

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        try:
            if not file_path.exists():
                return [f"Pattern file not found: {file_path}"]

            if not file_path.is_file():
                return [f"Path is not a file: {file_path}"]

            if file_path.suffix != ".json":
                return [f"Pattern file must have .json extension: {file_path}"]

            with open(file_path, "r", encoding="utf-8") as f:
                pattern_data = json.load(f)

            # Validate the pattern data
            validation_errors = self.validate_pattern(pattern_data)
            errors.extend(validation_errors)

        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in {file_path}: {str(e)}")
        except PermissionError:
            errors.append(f"Permission denied accessing {file_path}")
        except Exception as e:
            errors.append(f"Error validating {file_path}: {str(e)}")

        return errors

    def validate_all_patterns(self, patterns_dir: Path) -> Dict[str, List[str]]:
        """
        Validate all pattern files in a directory.

        Args:
            patterns_dir: Directory containing pattern files

        Returns:
            Dictionary mapping file names to validation errors
        """
        results = {}

        if not patterns_dir.exists():
            return {"directory": [f"Patterns directory not found: {patterns_dir}"]}

        if not patterns_dir.is_dir():
            return {"directory": [f"Path is not a directory: {patterns_dir}"]}

        pattern_files = list(patterns_dir.glob("*.json"))

        if not pattern_files:
            return {"directory": [f"No pattern files found in {patterns_dir}"]}

        for pattern_file in pattern_files:
            errors = self.validate_pattern_file(pattern_file)
            if errors:
                results[pattern_file.name] = errors

        return results
