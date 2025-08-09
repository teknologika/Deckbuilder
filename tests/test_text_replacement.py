"""
Unit tests for text replacement functionality in FormattingSupport class.

Tests the enhanced language remap functionality that replaces text content
in addition to changing language IDs.
"""

from unittest.mock import patch, mock_open

from deckbuilder.content.formatting_support import FormattingSupport


class TestTextReplacement:
    """Test text replacement functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.formatter = FormattingSupport()

    def test_preserve_case_all_upper(self):
        """Test case preservation for all uppercase words"""
        result = self.formatter.preserve_case("OPTIMIZE", "optimise")
        assert result == "OPTIMISE"

    def test_preserve_case_all_lower(self):
        """Test case preservation for all lowercase words"""
        result = self.formatter.preserve_case("optimize", "optimise")
        assert result == "optimise"

    def test_preserve_case_title_case(self):
        """Test case preservation for title case words"""
        result = self.formatter.preserve_case("Optimize", "optimise")
        assert result == "Optimise"

    def test_preserve_case_mixed_case(self):
        """Test case preservation for mixed case words"""
        result = self.formatter.preserve_case("OpTiMiZe", "optimise")
        assert result == "OpTiMiSe"

    def test_preserve_case_different_length(self):
        """Test case preservation when replacement is different length"""
        result = self.formatter.preserve_case("Color", "colour")
        assert result == "Colour"

    def test_is_context_exception_no_contexts(self):
        """Test context exception with empty context list"""
        result = self.formatter.is_context_exception("This is a test program", 15, "program", [])
        assert result is False

    def test_is_context_exception_with_match(self):
        """Test context exception when exception context is found"""
        text = "This is a computer program for analysis"
        result = self.formatter.is_context_exception(text, 19, "program", ["computer", "software"])
        assert result is True

    def test_is_context_exception_no_match(self):
        """Test context exception when exception context is not found"""
        text = "This is a TV program about nature"
        result = self.formatter.is_context_exception(text, 13, "program", ["computer", "software"])
        assert result is False

    def test_is_context_exception_case_insensitive(self):
        """Test context exception is case insensitive"""
        text = "This is a COMPUTER program for analysis"
        result = self.formatter.is_context_exception(text, 19, "program", ["computer", "software"])
        assert result is True

    @patch("builtins.open", new_callable=mock_open, read_data='{"spelling_patterns": {"optimize": "optimise", "color": "colour"}}')
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_language_mapping_success(self, mock_exists, mock_file):
        """Test successful language mapping loading"""
        result = self.formatter.load_language_mapping("en-AU")
        assert result is not None
        assert result["spelling_patterns"]["optimize"] == "optimise"
        assert result["spelling_patterns"]["color"] == "colour"

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_language_mapping_file_not_found(self, mock_exists):
        """Test language mapping loading when file doesn't exist"""
        result = self.formatter.load_language_mapping("en-XX")
        assert result is None

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_language_mapping_invalid_json(self, mock_exists, mock_file):
        """Test language mapping loading with invalid JSON"""
        result = self.formatter.load_language_mapping("en-AU")
        assert result is None

    def test_apply_text_replacements_empty_text(self):
        """Test text replacement with empty text"""
        result = self.formatter.apply_text_replacements("", "en-AU")
        assert result == ""

    def test_apply_text_replacements_none_text(self):
        """Test text replacement with None text"""
        result = self.formatter.apply_text_replacements(None, "en-AU")
        assert result is None

    @patch.object(FormattingSupport, "load_language_mapping")
    def test_apply_text_replacements_no_mapping(self, mock_load):
        """Test text replacement when no language mapping is available"""
        mock_load.return_value = None
        result = self.formatter.apply_text_replacements("optimize this", "en-XX")
        assert result == "optimize this"

    @patch.object(FormattingSupport, "load_language_mapping")
    def test_apply_text_replacements_spelling_patterns(self, mock_load):
        """Test text replacement with spelling patterns"""
        mock_load.return_value = {"spelling_patterns": {"optimize": "optimise", "color": "colour"}}

        result = self.formatter.apply_text_replacements("Please optimize the color scheme", "en-AU")
        assert result == "Please optimise the colour scheme"

    @patch.object(FormattingSupport, "load_language_mapping")
    def test_apply_text_replacements_case_preservation(self, mock_load):
        """Test text replacement preserves case"""
        mock_load.return_value = {"spelling_patterns": {"optimize": "optimise", "color": "colour"}}

        result = self.formatter.apply_text_replacements("OPTIMIZE the Color scheme", "en-AU")
        assert result == "OPTIMISE the Colour scheme"

    @patch.object(FormattingSupport, "load_language_mapping")
    def test_apply_text_replacements_word_boundaries(self, mock_load):
        """Test text replacement respects word boundaries"""
        mock_load.return_value = {"spelling_patterns": {"color": "colour"}}

        # Should not replace "color" in "colorful" or "discolor"
        result = self.formatter.apply_text_replacements("The color is colorful and discolored", "en-AU")
        assert result == "The colour is colorful and discolored"

    @patch.object(FormattingSupport, "load_language_mapping")
    def test_apply_text_replacements_conditional_mapping(self, mock_load):
        """Test text replacement with conditional mappings"""
        mock_load.return_value = {"conditional_mappings": {"program": {"to": "programme", "except_contexts": ["computer", "software"]}}}

        # Should replace "program" in TV context
        result1 = self.formatter.apply_text_replacements("Watch this TV program tonight", "en-AU")
        assert result1 == "Watch this TV programme tonight"

        # Should NOT replace "program" in computer context
        result2 = self.formatter.apply_text_replacements("Run this computer program", "en-AU")
        assert result2 == "Run this computer program"

    @patch.object(FormattingSupport, "load_language_mapping")
    def test_apply_text_replacements_vocabulary(self, mock_load):
        """Test text replacement with vocabulary mappings"""
        mock_load.return_value = {"vocabulary": {"cell phone": "mobile phone", "resume": "cv"}}

        result = self.formatter.apply_text_replacements("Submit your resume and cell phone number", "en-AU")
        assert result == "Submit your cv and mobile phone number"

    @patch.object(FormattingSupport, "load_language_mapping")
    def test_apply_text_replacements_vocabulary_case_preservation(self, mock_load):
        """Test text replacement with vocabulary preserves case"""
        mock_load.return_value = {"vocabulary": {"cell phone": "mobile phone"}}

        result = self.formatter.apply_text_replacements("CELL PHONE and Cell Phone", "en-AU")
        assert result == "MOBILE PHONE and Mobile Phone"

    @patch.object(FormattingSupport, "load_language_mapping")
    def test_apply_text_replacements_multiple_patterns(self, mock_load):
        """Test text replacement with multiple pattern types"""
        mock_load.return_value = {
            "spelling_patterns": {"optimize": "optimise", "color": "colour"},
            "conditional_mappings": {"program": {"to": "programme", "except_contexts": ["computer"]}},
            "vocabulary": {"cell phone": "mobile phone"},
        }

        text = "Please optimize the color in this TV program on your cell phone"
        result = self.formatter.apply_text_replacements(text, "en-AU")
        expected = "Please optimise the colour in this TV programme on your mobile phone"
        assert result == expected

    def test_apply_text_replacements_no_changes(self):
        """Test text replacement when no changes are needed"""
        # Use a text that won't trigger any replacements
        with patch.object(self.formatter, "load_language_mapping") as mock_load:
            mock_load.return_value = {"spelling_patterns": {"optimize": "optimise"}}
            result = self.formatter.apply_text_replacements("This text has no target words", "en-AU")
            assert result == "This text has no target words"


class TestTextReplacementEdgeCases:
    """Test edge cases for text replacement functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.formatter = FormattingSupport()

    @patch.object(FormattingSupport, "load_language_mapping")
    def test_multiple_occurrences_same_word(self, mock_load):
        """Test replacement of multiple occurrences of the same word"""
        mock_load.return_value = {"spelling_patterns": {"color": "colour"}}

        result = self.formatter.apply_text_replacements("The color and color scheme", "en-AU")
        assert result == "The colour and colour scheme"

    @patch.object(FormattingSupport, "load_language_mapping")
    def test_overlapping_patterns(self, mock_load):
        """Test that patterns are applied in correct order"""
        mock_load.return_value = {"spelling_patterns": {"analyze": "analyse", "analyzer": "analyser"}}

        # Should replace "analyzer" with "analyser", not "analyser"
        result = self.formatter.apply_text_replacements("Use this analyzer to analyze", "en-AU")
        assert result == "Use this analyser to analyse"

    @patch.object(FormattingSupport, "load_language_mapping")
    def test_punctuation_handling(self, mock_load):
        """Test replacement with punctuation"""
        mock_load.return_value = {"spelling_patterns": {"optimize": "optimise"}}

        result = self.formatter.apply_text_replacements("Please optimize, analyze, and finalize.", "en-AU")
        assert result == "Please optimise, analyze, and finalize."

    @patch.object(FormattingSupport, "load_language_mapping")
    def test_newline_handling(self, mock_load):
        """Test replacement across newlines"""
        mock_load.return_value = {"spelling_patterns": {"optimize": "optimise", "color": "colour"}}

        text = "Please optimize\nthe color scheme"
        result = self.formatter.apply_text_replacements(text, "en-AU")
        assert result == "Please optimise\nthe colour scheme"

    def test_preserve_case_empty_replacement(self):
        """Test case preservation with empty replacement"""
        result = self.formatter.preserve_case("TEST", "")
        assert result == ""

    def test_preserve_case_empty_original(self):
        """Test case preservation with empty original"""
        result = self.formatter.preserve_case("", "test")
        assert result == "test"
