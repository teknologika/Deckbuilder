"""
Sample content fixtures for deckbuilder testing.
"""

import pytest
from tests.utils.content_generator import (
    ContentGenerator, ContentType, ContentLength,
    get_sample_business_content, get_sample_technical_content,
    get_formatted_content_samples
)


@pytest.fixture
def content_generator():
    """Content generator with fixed seed for reproducible tests."""
    return ContentGenerator(seed=42)


@pytest.fixture
def business_content_short():
    """Short business content samples."""
    return get_sample_business_content(ContentLength.SHORT)


@pytest.fixture
def business_content_medium():
    """Medium business content samples."""
    return get_sample_business_content(ContentLength.MEDIUM)


@pytest.fixture
def business_content_long():
    """Long business content samples."""
    return get_sample_business_content(ContentLength.LONG)


@pytest.fixture
def technical_content_medium():
    """Medium technical content samples."""
    return get_sample_technical_content(ContentLength.MEDIUM)


@pytest.fixture
def formatted_content():
    """Content with various formatting applied."""
    return get_formatted_content_samples()


@pytest.fixture
def four_column_content(content_generator):
    """Content for four-column layouts."""
    return content_generator.build_column_content(4, ContentType.BUSINESS, ContentLength.MEDIUM)


@pytest.fixture
def three_column_content(content_generator):
    """Content for three-column layouts."""
    return content_generator.build_column_content(3, ContentType.TECHNICAL, ContentLength.MEDIUM)


@pytest.fixture
def comparison_content(content_generator):
    """Content for comparison layouts."""
    return content_generator.build_comparison_content('features', ContentType.BUSINESS)


@pytest.fixture
def table_content(content_generator):
    """Content for table layouts."""
    return content_generator.build_table_content(5, 3, include_formatting=True)


@pytest.fixture
def agenda_content(content_generator):
    """Content for agenda layouts."""
    return content_generator.generate_agenda_content(6)


@pytest.fixture
def swot_content(content_generator):
    """Content for SWOT analysis layouts."""
    return content_generator.generate_swot_content()


@pytest.fixture(params=[ContentLength.SHORT, ContentLength.MEDIUM, ContentLength.LONG])
def content_length_variations(request):
    """Parameterized fixture for different content lengths."""
    return request.param


@pytest.fixture(params=[ContentType.BUSINESS, ContentType.TECHNICAL, ContentType.MARKETING])
def content_type_variations(request):
    """Parameterized fixture for different content types.""" 
    return request.param