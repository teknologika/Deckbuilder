# Deckbuilder Python Library Documentation

**Choose your path based on what you want to accomplish:**

## 🚀 Quick Start (Most Users)

**Goal**: Create presentations fast from JSON or Markdown

### [📖 Quick Start Guide](Deckbuilder_Quick_Start.md)
- One-shot presentation creation
- JSON and Markdown examples
- Essential formatting guide
- Zero complex setup required

**Perfect for**: Business users, quick prototyping, simple automation

---

## 🔧 Core Development (Developers)

**Goal**: Programmatic control and integration

### [📖 Core API Reference](Deckbuilder_Core_API.md)
- Complete function reference
- Parameter details and return values
- Error handling strategies
- Integration examples

**Perfect for**: Developers, custom applications, precise control

---

## 🎨 Advanced Customization (Power Users)

**Goal**: Custom templates and enhanced functionality

### [📖 Template Management Guide](Deckbuilder_Template_Management.md)
- PowerPoint template customization
- CLI tools for template analysis
- Custom mapping creation
- Template validation and enhancement

**Perfect for**: Designers, enterprise users, custom branding

---

## 🤖 AI-Powered Features (Optional)

**Goal**: Intelligent layout recommendations

### [📖 Content Intelligence Guide](Deckbuilder_Content_Intelligence.md)
- AI-powered layout recommendations
- Content analysis and optimization
- Semantic content understanding
- Advanced workflow automation

**Perfect for**: AI applications, content optimization, smart automation

---

## Architecture Overview

Deckbuilder uses a **content-first design philosophy** that transforms LLMs from layout pickers into intelligent presentation consultants:

1. **Understand user content and communication goals first**
2. **Recommend presentation structure based on message intent**
3. **Suggest optimal layouts with audience consideration**
4. **Optimize content for chosen layouts**

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                 Python Library Core                     │
│  ┌─────────────────┐        ┌────────────────────┐     │
│  │  Deckbuilder    │        │  Structured        │     │
│  │  Engine         │◄──────►│  Frontmatter       │     │
│  └────────┬────────┘        └────────────────────┘     │
│           │                                              │
├───────────┴──────────────────────────────────────────────┤
│               Supporting Systems                         │
│  ┌─────────────────┐        ┌────────────────────┐     │
│  │  Template       │        │  Content           │     │
│  │  Management     │◄──────►│  Intelligence      │     │
│  └─────────────────┘        └────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd deckbuilder

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Basic usage
from deckbuilder import get_deckbuilder_client
deck = get_deckbuilder_client()
```

## Key Features

### 🎯 Content-First Intelligence
Instead of asking "what layouts exist?", Deckbuilder asks "what does the user want to communicate?" This transforms the system from a layout picker into an intelligent presentation consultant.

### 📝 Multiple Input Formats
- **JSON**: Precise programmatic control with comprehensive structure
- **Markdown + YAML**: Intuitive authoring with frontmatter definitions

### 🎨 Rich Content Support
- **Inline Formatting**: `**bold**`, `*italic*`, `___underline___`, `***bold italic***`
- **Mixed Content**: Headings, paragraphs, and bullet points in single slides
- **Advanced Tables**: Professional styling with custom colors and themes
- **50+ Layout Library**: Progressive implementation of business presentation layouts

### 🔧 Template Management
- **CLI Tools**: Analyze, validate, and enhance PowerPoint templates
- **Semantic Detection**: Automatic placeholder identification
- **Hybrid Mapping**: Semantic detection + JSON configuration for reliability

## Quick Example

```python
from deckbuilder import get_deckbuilder_client

# Get client instance
deck = get_deckbuilder_client()

# Create presentation data
data = {
    "presentation": {
        "slides": [
            {
                "type": "Title Slide",
                "title": "**My Presentation**",
                "subtitle": "Created with Deckbuilder"
            },
            {
                "type": "Title and Content",
                "title": "Key Benefits",
                "content": [
                    "**Fast** - One-shot creation",
                    "*Flexible* - JSON or Markdown input",
                    "***Intelligent*** - Content-first design"
                ]
            }
        ]
    }
}

# Create presentation in one command
result = deck.create_presentation_from_json(data, "MyPresentation")
print(result)  # "Successfully created presentation: MyPresentation.2025-01-26_1430.g.pptx"
```

## Documentation Structure

Each guide is designed for specific use cases:

- **[Quick Start](Deckbuilder_Quick_Start.md)** - Get up and running in 5 minutes
- **[Core API](Deckbuilder_Core_API.md)** - Complete function reference for developers
- **[Template Management](Deckbuilder_Template_Management.md)** - Custom templates and advanced configuration
- **[Content Intelligence](Deckbuilder_Content_Intelligence.md)** - AI-powered features and optimization

Choose the guide that matches your goals and experience level. Most users should start with the Quick Start guide.

## Additional Technical Documentation

For deeper understanding of the system architecture and design decisions:

- **[Supported Templates](Supported_Templates.md)** - Complete roadmap of 50+ business presentation layouts
- **[Placeholder Matching](Placeholder_Matching.md)** - Hybrid template system architecture and design
- **[Template Discovery](Template_Discovery.md)** - Content-first design evolution and structured frontmatter
- **[Convention Based Naming](Convention_Based_Naming.md)** - Multi-tier placeholder naming system
- **[Default Template](Default_Template.md)** - Built-in template specifications
- **[Testing Framework](Testing_Framework.md)** - Comprehensive testing approach and validation
- **[Template Management](Template_Management.md)** - Original template management system design
- **[PlaceKitten](Place_Kitten.md)** - Image processing library design (future enhancement)
