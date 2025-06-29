
# Deckbuilder - Task List

## Overview
This document tracks all tasks for building Deckbuilder, a Python library and accompanying MCP (Model Context Protocol) Server for intelligent PowerPoint presentation generation.
Tasks are organized by phase and component.

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

#### HIGH PRIORITY: CLI UX Enhancement
- [ ] **CLI Reorganization: Clean Hierarchical Command Structure** - 2025-06-29
  - [ ] Transform messy flat CLI with 13 top-level commands to professional hierarchical structure  
  - [ ] Implement `deckbuilder [options] <command> <subcommand> [parameters]` format
  - [ ] Create comprehensive bash completion with multi-level tab completion
  - [ ] Group related commands: `template`, `image`, `config` subcommands
  - [ ] Design Document: [CLI_Reorganization.md](docs/Features/CLI_Reorganization.md)
  - [ ] GitHub Issue: #10
  - **Priority**: High - Significant UX improvement for professional CLI interface

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

**Current Sprint**: Documentation Cleanup & CLI Tools Development (Phase A & B)
**Next Priority**: Standalone CLI tools and PyPI package preparation
**Completed**: 
- ✅ Template Management System - CLI tools, documentation, and validation systems
- ✅ PlaceKitten Library - Complete image processing with filters and smart cropping
- ✅ PlaceKitten-Deckbuilder Integration - Smart fallback system with professional styling
- ✅ Comprehensive Testing - 108 tests including image integration and fallback validation
- ✅ MCP Server Integration - Full image support documentation and USER CONTENT POLICY
- ✅ Code Quality & CI/CD - All formatting and linting issues resolved

**Current Focus (2025-06-28)**:
- 🎯 Documentation cleanup: Update planning documents and create comprehensive guides
- 🎯 PlaceKitten API documentation with examples and integration patterns
- 🎯 Standalone CLI development separate from MCP server for local usage
- 🎯 Package preparation for PyPI distribution and publication

**Development Goals**:
- **Complete Documentation**: Comprehensive guides for all features and capabilities
- **Standalone CLI**: Independent command-line tools for local development and testing
- **PyPI Package**: Professional distribution with `pip install deckbuilder` support
- **User Experience**: Simplified workflows for both CLI and MCP server usage

**Architecture Status**: 
- ✅ **MCP Server**: Fully functional with image support and enhanced tools
- ✅ **PlaceKitten Library**: Complete computer vision pipeline with intelligent cropping
- ✅ **Image Integration**: Smart fallback system with professional styling
- 🚧 **CLI Tools**: Template analysis exists, needs standalone presentation generation
- 🚧 **Package Distribution**: Needs PyPI optimization and publication

**Blockers**: None identified
**Target Completion**: Phases A, B, C - Complete CLI tools and PyPI package
**Last Updated**: 2025-06-28
