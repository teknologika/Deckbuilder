
# Deckbuilder - Task List

## Overview
This document tracks all tasks for building Deckbuilder, a Python library and accompanying MCP (Model Context Protocol) Server for intelligent PowerPoint presentation generation.
Tasks are organized by phase and component.

---

## 🚨 CURRENT PRIORITY: Content Processing Unification

### **[GitHub Issue #35](https://github.com/teknologika/Deckbuilder/issues/35) - Unify content processing - eliminate artificial simple/rich distinction**
**Added**: 2025-07-06
**Priority**: HIGH - Affects 20+ test failures
**Status**: 🔧 Ready for Implementation

**Problem**: Content processing fails due to artificial "simple" vs "rich" content distinction that doesn't exist in python-pptx.

**Key Discoveries**:
- Python-pptx has **no concept of "simple" vs "rich" content** - all text uses same hierarchy
- Hardcoded `placeholder_format.idx == 1` fails for complex layouts (Two Content, Four Columns)
- JSON canonical pipeline achieved 64% test reduction (56 → 20 failures)
- Remaining 20 failures all related to content block processing

**Solution**: Unified content processing using semantic placeholder detection and single text_frame → paragraphs → runs path.

---

### ✅ Completed Features
- [x] Core presentation engine with structured frontmatter support
- [x] Template system with semantic detection and JSON mapping
- [x] Layout selection fix (prefer `layout` field over `type` field)
- [x] Enhanced placeholder naming (copy descriptive names from template mapping)
- [x] File-based MCP tool (`create_presentation_from_file`)
- [x] JSON object input fix (changed from string to dict parameter)

### ✅ PlaceKitten Library Development ✅ COMPLETED

#### Phase 0: Asset Cleanup ✅ COMPLETED
- [x] **Clean up image directory structure**
  - [x] Move kitten images from `assets/images/Images/` to `assets/images/`
  - [x] Remove empty nested `Images/` folder  
  - [x] Move kitten images from `assets/images/` to `src/placekitten/images/`
  - [x] Update PlaceKitten core to use module-local image storage
  - [x] Verify all 6 kitten images are accessible in new location

#### Phase 1: Core Library Implementation ✅ COMPLETED
- [x] **Add dependencies and setup**
  - [x] Add OpenCV (cv2) to requirements.txt for computer vision
  - [x] Add Pillow (PIL) to requirements.txt for image processing
  - [x] Add NumPy to requirements.txt for array operations
  - [x] Create demo image source folder structure

- [x] **Implement PlaceKitten class**
  - [x] Build main PlaceKitten class with basic image generation
  - [x] Add dimension handling (auto-height 16:9 and custom)
  - [x] Implement image selection from existing kitten images
  - [x] Add file path resolution and management

- [x] **Create ImageProcessor class**
  - [x] Build ImageProcessor for image manipulation
  - [x] Add basic resize and save functionality
  - [x] Implement method chaining support
  - [x] Add image loading from files or arrays

- [x] **Basic filter pipeline**
  - [x] Implement core filters (grayscale, blur, sepia, invert)
  - [x] Add advanced filters (brightness, contrast, pixelate, saturation, sharpness)
  - [x] Create filter registry with extensible architecture
  - [x] Add filter validation and error handling

#### Phase 2: Intelligent Processing ✅ COMPLETED
- [x] **Computer vision pipeline**
  - [x] Integrate OpenCV for edge detection
  - [x] Implement Canny edge detection for contour analysis
  - [x] Add Gaussian blur for noise reduction
  - [x] Create contour identification algorithms

- [x] **Smart cropping engine**
  - [x] Implement rule-of-thirds composition calculation
  - [x] Add subject detection using largest contour
  - [x] Create optimal positioning algorithms for 16:9 format
  - [x] Add boundary safety validation
  - [x] Add Haar cascade face detection for face-priority cropping

- [x] **Step visualization system**
  - [x] Implement 9-step processing visualization
  - [x] Add debug output for each processing stage
  - [x] Create educational step-by-step image generation
  - [x] Add optional visualization toggling
  - [x] Fix test file management - proper output directories

- [x] **Enhanced PlaceKitten Features**
  - [x] Optional width/height parameters with aspect ratio preservation
  - [x] 1-based indexing for user-friendly image selection
  - [x] Smart random image selection for invalid/missing image_id
  - [x] Full-size image support when no dimensions specified

#### Phase 3: Deckbuilder Integration ✅ COMPLETED
- [x] **Smart Image Fallback System**
  - [x] Design fallback logic for missing/invalid image_path in Picture with Caption layouts
  - [x] Implement automatic PlaceKitten generation with grayscale + smart crop
  - [x] Add professional presentation styling (grayscale for business context)
  - [x] Create cached generation system to avoid regenerating identical images

- [x] **Enhanced Structured Frontmatter**
  - [x] Add image_path field to Picture with Caption YAML structure
  - [x] Add alt_text field for accessibility support
  - [x] Update structured frontmatter parser to handle image fields
  - [x] Maintain backward compatibility with existing presentations

- [x] **PowerPoint Image Integration**
  - [x] Create ImageHandler class for image file validation and processing
  - [x] Implement PlaceKittenIntegration bridge between libraries
  - [x] Add PICTURE placeholder detection and image insertion logic
  - [x] Enhance engine.py with image placement capabilities using python-pptx

- [x] **Image Processing Workflow**
  - [x] Validate image files (existence, format, accessibility)
  - [x] Smart resize to match PowerPoint placeholder dimensions
  - [x] Implement graceful fallback to PlaceKitten for any image issues
  - [x] Add error handling and user feedback for image problems

- [x] **Testing & Validation**
  - [x] Comprehensive pytest test suites (18 PlaceKitten tests + 15 integration tests)
  - [x] Markdown and JSON input format testing with proper environment setup
  - [x] Image fallback functionality and PlaceKitten integration validation
  - [x] File size validation to ensure images actually appear in PowerPoint files
  - [x] Professional styling configuration testing

- [x] **MCP Tool Integration**
  - [x] Update MCP server tools to document comprehensive image support
  - [x] Enhanced tool descriptions showcasing PlaceKitten capabilities
  - [x] Complete media.image_path frontmatter examples
  - [x] USER CONTENT POLICY implementation (use JSON/markdown exactly as-is)

#### Phase 4: Advanced PlaceKitten Features  
- [ ] **Batch processing capabilities**
  - [ ] Implement multi-image processing workflows
  - [ ] Add progress tracking for batch operations
  - [ ] Create quality optimization algorithms
  - [ ] Add error handling for batch failures

- [ ] **Performance optimization**
  - [ ] Implement image caching system
  - [ ] Add memory usage optimization (<500MB per session)
  - [ ] Create parallel processing for batch operations
  - [ ] Add performance metrics and monitoring (<2s target)

- [ ] **Quality assurance and validation**
  - [ ] Add input format validation (JPG, PNG, WebP)
  - [ ] Implement output quality controls
  - [ ] Create comprehensive error handling
  - [ ] Add processing validation checks

#### Phase 5: MCP Integration
- [ ] **Enhanced MCP tools for image generation**
  - [ ] Create generate_placeholder_image MCP tool
  - [ ] Add process_image_for_presentation MCP tool
  - [ ] Implement batch_process_images MCP tool
  - [ ] Add automatic template sizing support

- [ ] **Presentation workflow optimization**
  - [ ] Integrate with existing slide template system
  - [ ] Add structured frontmatter support for images
  - [ ] Create seamless workflow with markdown generation
  - [ ] Add presentation format optimization (JPG/PNG)

- [ ] **Testing and validation**
  - [ ] Create comprehensive unit tests for image integration
  - [ ] Add integration tests with deck builder
  - [ ] Implement performance benchmarking
  - [ ] Add user acceptance testing scenarios

### 🚀 Next Development Phases (Current Focus)

#### JSON is King Refactoring
- [ ] **1. Implement Canonical JSON Model:** Define and document the final JSON schema. (Partially Completed)
- [x] **2. Create Converter Module:** Create `src/deckbuilder/converter.py`.
- [x] **3. Implement `markdown_to_json`:** Build the function in the new module to convert `.md` files to the canonical JSON format. (Partially Completed - Bullet and basic table parsing improved, multi-content layout strategy documented and partially implemented)
- [x] **4. Refactor `cli.py`:** Update the `create` command to use the new converter and pass only JSON to the engine. (Completed)
- [x] **5. Refactor `engine.py`:** Strip all Markdown and multi-format parsing logic, leaving only the logic that processes the canonical JSON model. (Completed)
- [x] **6. Refactor `structured_frontmatter.py`:** Integrate its conversion logic into the new `converter.py` module.
- [x] **7. Test Suite Update:** Update all relevant unit and integration tests to reflect the pipeline changes. (Completed - E2E golden file test and engine/converter unit tests updated)
- [x] **8. Documentation Update:** Update all user and developer documentation to reflect the new architecture. (Partially Completed - API.md updated, Multi_Content_Layouts.md created)

#### HIGH PRIORITY: CLI UX Enhancement
- [x] **CLI Reorganization: Clean Hierarchical Command Structure** - 2025-06-29 ✅ COMPLETED
  - [x] Transform messy flat CLI with 13 top-level commands to professional hierarchical structure  
  - [x] Implement `deckbuilder [options] <command> <subcommand> [parameters]` format
  - [x] Create comprehensive bash completion with multi-level tab completion
  - [x] Group related commands: `template`, `image`, `config` subcommands
  - [x] Design Document: [CLI_Reorganization.md](docs/Features/CLI_Reorganization.md)
  - [x] GitHub Issue: #10 - COMPLETED
  - **Status**: ✅ COMPLETED - Professional hierarchical CLI structure implemented

- [x] **Config Show Display Enhancement** - 2025-06-29 ✅ COMPLETED
  - [x] Fix config show to display proper default values instead of "Not set"
  - [x] Add source indicators: (Default), (Environment Variable), (CLI Argument)
  - [x] Fix font message text: "using template fonts" instead of "template default"
  - [x] GitHub Issue: #11 - COMPLETED
  - **Status**: ✅ COMPLETED - Config display now shows proper defaults and source indicators

#### 🚨 CRITICAL: Content Mapping Failures (v1.0.2 Discovery)

**Status**: Critical production issues discovered during v1.0.2 validation - Core functionality broken

- [x] **JSON Complex Field Mapping Broken** - [GitHub Issue #26](https://github.teknologika/Deckbuilder/issues/26) ✅ COMPLETED
  - [x] `content_left_1`, `content_right_1`, etc. not being placed in PowerPoint slides
  - [x] Template mapping works correctly, but content processing pipeline fails
  - [x] Multi-column layouts (Two Content, Four Columns, Comparison) affected
  - [x] **Root Cause**: Input processing pipeline broken, not template or core engine
  - **Priority**: Critical - Core functionality completely broken



#### 🚨 CRITICAL: Rich Content Rendering Bug - [GitHub Issue #33](https://github.com/teknologika/Deckbuilder/issues/33)

**Status**: Critical content rendering issue - Rich content displaying as JSON strings instead of formatted PowerPoint elements

#### 🧪 Testing Philosophy Revolution - [GitHub Issue #28](https://github.com/teknologika/Deckbuilder/issues/28)

**Critical Lesson**: 157/157 passing tests gave false confidence while core functionality was broken

- [x] **Document Content-First Testing Philosophy** - Added to PLANNING.md ✅ COMPLETED
  - [x] The False Confidence Problem: Tests passed while output was broken
  - [x] Traditional vs Content-First Testing comparison
  - [x] Root cause analysis and prevention strategies
  - [x] Architectural lessons learned and development guidelines

- [ ] **Implement Content-First Testing Framework**
  - [ ] **Content Validation Tests**: Read actual PowerPoint files to verify content placement
  - [ ] **Field Mapping Tests**: Validate complex layout placeholders (content_left_1, etc.)
  - [ ] **End-to-End Workflow Tests**: Complete input → output validation
  - [ ] **Regression Prevention Suite**: Automated validation of previously working features

- [ ] **Diagnostic Testing Implementation**
  - [x] Create `/tests/deckbuilder/e2e/test_pipeline_diagnostics.py` ✅ COMPLETED
  - [ ] Run diagnostic tests to isolate template vs content generation issues
  - [ ] Validate simple content mapping (titles, basic content)
  - [ ] Test complex field mappings (multi-column layouts)
  - [ ] Verify Markdown frontmatter processing pipeline

#### URGENT: PlaceKitten CLI Bug Fix
- [ ] **Fix PlaceKitten CLI Image Generation Bug**
  - [ ] PlaceKitten CLI commands creating directories instead of image files
  - [ ] Error: `[Errno 21] Is a directory: 'filename.jpg'` when using `deckbuilder image` command
  - [ ] Affects TestPyPI package validation and user experience
  - [ ] Test environment validation failing due to image generation issues
  - **Priority**: High - Blocking TestPyPI validation and user testing

#### Phase A: Documentation & Planning Cleanup
- [ ] **PlaceKitten Documentation**
  - [ ] Create comprehensive src/placekitten/README.md with API docs and examples
  - [ ] Update main README.md to include PlaceKitten as core feature
  - [ ] Create docs/Features/Image_Support.md design specification
  - [ ] Document integration patterns and use cases

#### Phase B: Command Line Tools Enhancement  
- [x] **Standalone CLI Development**
  - [x] Create standalone CLI entry point separate from MCP server
  - [x] Enhanced template analysis with better reporting and validation
  - [x] Presentation generation commands for direct CLI usage
  - [ ] Debug and troubleshooting tools for template validation and image testing

- [ ] **CLI Environment Logic Improvements** 🚧 IN PROGRESS
  - [ ] Improve environment variable resolution priority (CLI args > env vars > defaults)
  - [ ] Add `deckbuilder init [PATH]` command for template setup
  - [ ] Simplify global arguments (`-t/--templates`, `-o/--output`)
  - [ ] Enhanced error messages with actionable guidance
  - [ ] Environment variable setup guidance in init command
  - [ ] Tab completion support for commands and templates
  - **Design Document**: [Deckbuilder_CLI.md](docs/Features/Deckbuilder_CLI.md)

- [ ] **User Experience Improvements**
  - [x] Simplified workflow: `deckbuilder create presentation.md`
  - [ ] Progress indicators and clear feedback for operations
  - [ ] Better error handling with helpful error messages and suggestions
  - [ ] Configuration management for CLI-based settings and preferences

- [ ] **Local Development Tools**
  - [ ] Local testing utilities to test presentations without MCP server
  - [ ] CLI-based template management operations
  - [ ] PlaceKitten generation and testing tools
  - [ ] Performance profiling for generation speed and memory analysis

#### Phase C: PyPI Package Preparation & Publishing
- [ ] **Package Structure Optimization**
  - [ ] Setup.py configuration with proper dependencies and entry points
  - [ ] Manifest files including templates, examples, documentation
  - [ ] CLI command registration: `pip install deckbuilder` → `deckbuilder` command
  - [ ] Package documentation for PyPI-ready README and docs

- [ ] **Distribution Preparation**
  - [ ] Version management with semantic versioning strategy
  - [ ] Changelog generation for automated release notes
  - [ ] Package testing to validate installation and functionality
  - [ ] Security scanning to ensure no vulnerabilities in dependencies

- [ ] **PyPI Publishing**
  - [ ] Test PyPI upload to validate package structure
  - [ ] Production PyPI release for official package publication
  - [ ] Integration testing: install from PyPI and test functionality
  - [ ] Publication documentation with installation and usage guides

### 📋 Future Enhancements
- [ ] **Content-First MCP Tools**
  - [ ] `analyze_presentation_needs()` - Content and goal analysis
  - [ ] `recommend_slide_approach()` - Layout recommendations
  - [ ] `optimize_content_for_layout()` - Content optimization

- [ ] **Advanced Template Features**
  - [ ] Template comparison and migration tools
  - [ ] Custom template creation wizard
  - [ ] Template validation CI/CD integration
  - [ ] Multi-template support and switching


### 🧹 Code Quality Maintenance

**Priority: Medium - Ongoing cleanup items that don't block functionality**

- [x] **Fix PlaceKitten flake8 violations (ALL FIXED - 2025-06-27)**
  - [x] F401: Remove unused imports (typing.Any from filters.py)
  - [x] F841: Remove unused variables (step4_image from smart_crop.py)
  - [x] E226: Fix missing whitespace around operators (core.py)
  - [x] W293: Fix blank lines with whitespace (smart_crop.py)
  - [x] E402: Add noqa comments for necessary import placement (debug_scaling.py)
  - [x] F541: Fix f-strings without placeholders (debug_scaling.py)

- [x] **PlaceKitten test file management (FIXED - 2025-06-27)**
  - [x] Stop test files from dumping in root directory
  - [x] Add output_folder parameter to smart_crop methods
  - [x] Update .gitignore with proper patterns for test files
  - [x] All test output contained in tests/placekitten/test_output/

- [ ] **Fix remaining flake8 E501 line length violations (56 total)**
  - [ ] Break long docstrings and function calls in `src/deckbuilder/cli_tools.py` (6 violations)
  - [ ] Fix line length in `src/deckbuilder/naming_conventions.py` (1 violation)
  - [ ] Clean up `src/mcp_server/content_optimization.py` (1 violation)
  - [ ] Refactor `src/mcp_server/tools.py` (3 violations)
  - [ ] Break long strings in `tests/utils/content_generator.py` (45 violations)
  - [ ] Update CI to remove E501 from ignore list once fixed

- [x] **Code formatting consistency**
  - [x] Pre-commit hooks working with black, flake8, bandit, pytest
  - [x] All PlaceKitten code follows formatting standards
  - [ ] Ensure all new code follows 100-character limit

### 🔧 Technical Debt
- [ ] **Code Organization**
  - [ ] Consolidate template analysis code
  - [ ] Improve error handling across MCP tools
  - [ ] Add comprehensive logging
  - [ ] Create unit tests for template management

- [ ] **Documentation Updates**
  - [ ] Update README with new MCP tools
  - [ ] Add template creation user guide
  - [ ] Document naming conventions clearly
  - [ ] Create troubleshooting guide

## Progress Tracking

### 🚨 CRITICAL STATE: v1.0.2 Content Mapping Failures

**Current Priority**: EMERGENCY - Fix critical production issues discovered during v1.0.2 validation

**Critical Issues (Production Blocking)**:
- ❌ **JSON Complex Field Mapping**: content_left_1, content_right_1 not placed in slides
- ❌ **Markdown Frontmatter Titles**: YAML titles not appearing in PowerPoint
- ❌ **Image Insertion Regression**: Previously working PlaceKitten integration broken  
- ❌ **False Test Confidence**: 157/157 tests passed while core functionality failed

**Emergency Response Plan**:
1. 🚨 **Fix Content Mapping Pipeline**: Restore JSON and Markdown processing
2. 🚨 **Fix Image Insertion Regression**: Restore PlaceKitten PowerPoint integration  
3. 🧪 **Implement Content-First Testing**: Prevent future false confidence
4. 🔄 **Regression Testing Suite**: Validate all existing functionality

### Discovery & Documentation ✅ COMPLETED
- [x] **GitHub Issues Created**: All 5 critical issues documented (#26, #27, #28, #29, #30)
- [x] **PLANNING.md Updated**: Content-first testing philosophy and lessons learned documented
- [x] **TASK.md Updated**: Critical issues prioritized and aligned with GitHub issues
- [x] **Root Cause Analysis**: Template mapping works, core engine works, input processing broken

### Next Critical Tasks
1. **Fix JSON Complex Field Mapping** (Issue #26) - Restore multi-column layout functionality
2. **Fix Markdown Frontmatter Processing** (Issue #27) - Restore primary input format  
3. **Fix Image Insertion Regression** (Issue #29) - Restore PlaceKitten integration
4. **Implement Content-First Testing** (Issue #28) - Prevent future false confidence

**Previously Completed**: 
- ✅ Template Management System - CLI tools, documentation, and validation systems
- ✅ PlaceKitten Library - Complete image processing with filters and smart cropping
- ⚠️ PlaceKitten-Deckbuilder Integration - **REGRESSION: Integration broken**
- ⚠️ Comprehensive Testing - **FALSE CONFIDENCE: Tests don't validate content**
- ✅ MCP Server Integration - Full image support documentation and USER CONTENT POLICY
- ✅ Code Quality & CI/CD - All formatting and linting issues resolved

**Current Focus (2025-07-03)**:
- 🚨 **EMERGENCY**: Fix critical content mapping failures in production
- 🧪 **Testing Revolution**: Implement content-first testing to prevent future issues
- 🔄 **Regression Prevention**: Ensure previously working features stay working
- 📋 **Issue Tracking**: Systematic resolution of all GitHub issues

**Architecture Status**: 
- ✅ **Template Mapping**: Works perfectly - JSON structure correctly identifies layouts
- ✅ **Core PowerPoint Engine**: Works correctly - When data reaches it, slides generate properly  
- ❌ **Input Processing Pipelines**: BROKEN - JSON and Markdown preprocessing fails
- ❌ **Content Placement**: BROKEN - Complex field names not recognized
- ❌ **Image Integration**: REGRESSION - Previously working functionality lost

**Critical Blockers**: 
- **Content mapping completely broken** - Users cannot generate functional presentations
- **Primary input formats broken** - Both JSON and Markdown affected
- **Image functionality lost** - Regression in previously working features

**Emergency Timeline**: Fix critical issues before any new development
**Target Completion**: Restore v1.0.2 to functional state, then implement prevention measures
**Last Updated**: 2025-07-03

