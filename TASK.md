
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

### 🖼️ PlaceKitten Library Development (Current Focus)

#### Phase 0: Asset Cleanup (Immediate Priority)
- [x] **Clean up image directory structure**
  - [x] Move kitten images from `assets/images/Images/` to `assets/images/`
  - [x] Remove empty nested `Images/` folder  
  - [x] Move kitten images from `assets/images/` to `src/placekitten/images/`
  - [x] Update PlaceKitten core to use module-local image storage
  - [x] Verify all 6 kitten images are accessible in new location

#### Phase 1: Core Library Implementation
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

#### Phase 3: Deckbuilder Integration (Current Focus)
- [ ] **PlaceKitten Documentation**
  - [ ] Create comprehensive src/placekitten/README.md with API docs and examples
  - [ ] Update main README.md to include PlaceKitten as core feature
  - [ ] Create docs/Features/Image_Support.md design specification
  - [ ] Document integration patterns and use cases

- [ ] **Smart Image Fallback System**
  - [ ] Design fallback logic for missing/invalid image_path in Picture with Caption layouts
  - [ ] Implement automatic PlaceKitten generation with grayscale + smart crop
  - [ ] Add professional presentation styling (grayscale for business context)
  - [ ] Create cached generation system to avoid regenerating identical images

- [ ] **Enhanced Structured Frontmatter**
  - [ ] Add image_path field to Picture with Caption YAML structure
  - [ ] Add alt_text field for accessibility support
  - [ ] Update structured frontmatter parser to handle image fields
  - [ ] Maintain backward compatibility with existing presentations

- [ ] **PowerPoint Image Integration**
  - [ ] Create ImageHandler class for image file validation and processing
  - [ ] Implement PlaceKittenIntegration bridge between libraries
  - [ ] Add PICTURE placeholder detection and image insertion logic
  - [ ] Enhance engine.py with image placement capabilities using python-pptx

- [ ] **Image Processing Workflow**
  - [ ] Validate image files (existence, format, accessibility)
  - [ ] Smart resize to match PowerPoint placeholder dimensions
  - [ ] Implement graceful fallback to PlaceKitten for any image issues
  - [ ] Add error handling and user feedback for image problems

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

**Current Sprint**: PlaceKitten-Deckbuilder Integration (Phase 3 - IN PROGRESS)
**Next Priority**: Image Support Implementation & Smart Fallback System
**Completed**: 
- ✅ Template Management System - CLI tools, documentation, and validation systems
- ✅ PlaceKitten Phase 1 - Core library with image processing and filters
- ✅ PlaceKitten Phase 2 - Computer vision, smart cropping, step visualization
- ✅ Code Quality Fixes - All flake8 violations resolved, proper test file management

**Current Focus (2025-06-28)**:
- 🎯 PlaceKitten comprehensive documentation (README, integration guides)
- 🎯 Design smart image fallback system (grayscale + smart crop for professional look)
- 🎯 Enhanced YAML structure with image_path support for Picture with Caption
- 🎯 PowerPoint image integration using python-pptx PICTURE placeholders

**Integration Design Goals**:
- **Smart Fallbacks**: Automatic PlaceKitten generation when image_path missing/invalid
- **Professional Styling**: Grayscale + smart crop for business presentation context
- **Seamless Experience**: Enhanced YAML with image_path, backward compatible
- **Robust Processing**: Validation, error handling, cached generation

**Blockers**: None identified
**Target Completion**: Phase 3 - Full PlaceKitten-Deckbuilder integration with image support
**Last Updated**: 2025-06-28
