
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
  - [x] Update any existing path references in documentation
  - [x] Verify all 7 kitten images are accessible in new location

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

#### Phase 2: Intelligent Processing
- [ ] **Computer vision pipeline**
  - [ ] Integrate OpenCV for edge detection
  - [ ] Implement Canny edge detection for contour analysis
  - [ ] Add Gaussian blur for noise reduction
  - [ ] Create contour identification algorithms

- [ ] **Smart cropping engine**
  - [ ] Implement rule-of-thirds composition calculation
  - [ ] Add subject detection using largest contour
  - [ ] Create optimal positioning algorithms for 16:9 format
  - [ ] Add boundary safety validation

- [ ] **Step visualization system**
  - [ ] Implement 9-step processing visualization
  - [ ] Add debug output for each processing stage
  - [ ] Create educational step-by-step image generation
  - [ ] Add optional visualization toggling

#### Phase 3: Advanced Features
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

#### Phase 4: MCP Integration
- [ ] **Deck builder integration**
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
  - [ ] Create comprehensive unit tests
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

- [ ] **Fix remaining flake8 E501 line length violations (56 total)**
  - [ ] Break long docstrings and function calls in `src/deckbuilder/cli_tools.py` (6 violations)
  - [ ] Fix line length in `src/deckbuilder/naming_conventions.py` (1 violation) 
  - [ ] Clean up `src/mcp_server/content_optimization.py` (1 violation)
  - [ ] Refactor `src/mcp_server/tools.py` (3 violations)
  - [ ] Break long strings in `tests/utils/content_generator.py` (45 violations)
  - [ ] Update CI to remove E501 from ignore list once fixed

- [ ] **Code formatting consistency**
  - [ ] Run `black --line-length 100 src/ tests/` after line length fixes
  - [ ] Ensure all new code follows 100-character limit
  - [ ] Add pre-commit hooks for automatic formatting

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

**Current Sprint**: PlaceKitten Library Development (Phase 1)
**Next Priority**: Core library implementation with basic placeholder generation and dimension handling
**Completed**: ✅ Template Management System - CLI tools, documentation, and validation systems
**Blockers**: None identified
**Target Completion**: Phase 1 - Core PlaceKitten library with basic image processing - End of current sprint
**Last Updated**: 2025-06-27