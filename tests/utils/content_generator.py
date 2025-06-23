"""
Content Generation System for Testing

Provides hardcoded sample content libraries and dynamic content builders
for comprehensive testing of the deck-builder system.
"""

import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ContentType(Enum):
    """Content type categories."""
    BUSINESS = "business"
    TECHNICAL = "technical"
    MARKETING = "marketing"
    EDUCATIONAL = "educational"


class ContentLength(Enum):
    """Content length variations."""
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


@dataclass
class ContentVariation:
    """Content variation with length and formatting options."""
    text: str
    length: ContentLength
    has_formatting: bool = False


# Hardcoded Sample Content Libraries
BUSINESS_CONTENT = {
    ContentLength.SHORT: {
        'titles': [
            'Q4 Results',
            'Market Update', 
            'Strategic Vision',
            'Revenue Growth',
            'Cost Optimization',
            'Team Performance'
        ],
        'content': [
            'Revenue up 15%',
            'Strong market position',
            'Growth initiatives launched',
            'Operational efficiency improved',
            'Customer satisfaction high',
            'Team productivity increased'
        ],
        'bullets': [
            'Strong quarterly performance',
            'Market share expansion',
            'Cost reduction achieved',
            'Customer retention improved'
        ]
    },
    ContentLength.MEDIUM: {
        'titles': [
            'Quarterly Performance Review',
            'Market Analysis & Trends',
            'Strategic Planning Session',
            'Operational Excellence Initiative'
        ],
        'content': [
            'Revenue increased 15% year-over-year with strong performance across all business units.',
            'Market conditions show positive trends with emerging opportunities in key segments.',
            'Strategic initiatives are delivering measurable results and driving sustainable growth.',
            'Operational improvements have reduced costs by 12% while maintaining quality standards.'
        ],
        'bullets': [
            'Quarterly revenue exceeded targets by 8% with consistent growth patterns',
            'Market expansion into three new geographic regions completed successfully',
            'Customer satisfaction scores improved to 94% from 89% previous quarter',
            'Operational efficiency gains reduced processing time by 25%'
        ]
    },
    ContentLength.LONG: {
        'titles': [
            'Comprehensive Quarterly Performance Analysis and Strategic Outlook'
        ],
        'content': [
            'Our comprehensive analysis of Q4 performance demonstrates exceptional results across all key performance indicators, with revenue growth of 15% year-over-year, market share expansion in core segments, and operational excellence initiatives delivering substantial cost savings while maintaining our commitment to quality and customer satisfaction.',
            'The strategic market analysis reveals emerging opportunities in digital transformation services, sustainable technology solutions, and international expansion, positioning our organization to capitalize on industry trends and maintain competitive advantage through innovative product development and strategic partnerships.'
        ],
        'bullets': [
            'Financial performance exceeded all quarterly targets with revenue growth of 15%, EBITDA margin improvement of 3.2 percentage points, and cash flow generation 22% above previous year comparisons',
            'Market positioning strengthened through successful product launches, customer acquisition campaigns, and strategic partnerships that expanded our addressable market by 18% and enhanced competitive differentiation',
            'Operational excellence initiatives delivered $2.3M in cost savings through process automation, supply chain optimization, and workforce productivity improvements while maintaining 99.2% quality standards',
            'Customer satisfaction metrics reached all-time highs with NPS score of 67, retention rate of 96%, and average contract value increasing 14% through enhanced service delivery and value proposition alignment'
        ]
    }
}

TECHNICAL_CONTENT = {
    ContentLength.SHORT: {
        'titles': [
            'System Architecture',
            'API Performance',
            'Security Updates',
            'Database Optimization',
            'Cloud Migration',
            'DevOps Pipeline'
        ],
        'content': [
            'Microservices architecture',
            '99.9% uptime achieved',
            'Security patches applied',
            'Query performance improved',
            'Cloud infrastructure ready',
            'CI/CD pipeline automated'
        ],
        'bullets': [
            'REST API endpoints optimized',
            'Database indexing improved',
            'Security audit completed',
            'Load testing passed'
        ]
    },
    ContentLength.MEDIUM: {
        'titles': [
            'Microservices Architecture Implementation',
            'API Gateway Performance Optimization',
            'Security Framework Enhancement',
            'Database Performance Tuning'
        ],
        'content': [
            'Microservices architecture successfully migrated from monolithic structure with 40% performance improvement.',
            'API Gateway implementation reduced response times by 60% and improved system scalability.',
            'Enhanced security framework with multi-factor authentication and encryption at rest.',
            'Database optimization reduced query execution time by 75% through strategic indexing.'
        ],
        'bullets': [
            'Container orchestration with Kubernetes deployed across three environments',
            'API response times improved from 200ms to 80ms average with 99.9% uptime',
            'Zero-trust security model implemented with role-based access controls',
            'Database performance monitoring shows 75% reduction in slow query frequency'
        ]
    },
    ContentLength.LONG: {
        'titles': [
            'Comprehensive Technical Architecture Modernization and Performance Enhancement Initiative'
        ],
        'content': [
            'The comprehensive technical modernization initiative has successfully transformed our legacy monolithic architecture into a cloud-native microservices ecosystem, leveraging containerization, service mesh technology, and advanced orchestration platforms to achieve unprecedented scalability, reliability, and performance metrics while maintaining strict security protocols and regulatory compliance standards.',
            'Advanced API gateway implementation with intelligent load balancing, rate limiting, and circuit breaker patterns has revolutionized system performance, reducing average response times from 200ms to 50ms while supporting 10x traffic increases and maintaining 99.99% uptime through automated failover mechanisms and distributed caching strategies.'
        ],
        'bullets': [
            'Microservices architecture migration completed with 15 independent services, each optimized for specific business functions, resulting in 40% performance improvement, 60% reduction in deployment times, and enhanced fault isolation capabilities',
            'Cloud-native infrastructure deployment on Kubernetes with auto-scaling, service discovery, and advanced monitoring provides 99.99% uptime, supports traffic spikes up to 1000% normal load, and reduces infrastructure costs by 35%',
            'Comprehensive security framework implementation includes zero-trust architecture, end-to-end encryption, automated vulnerability scanning, and compliance monitoring for SOC2, GDPR, and industry-specific regulatory requirements',
            'DevOps pipeline automation with GitOps workflows, automated testing suites, and deployment strategies has reduced release cycle time from 2 weeks to 2 hours while maintaining code quality standards and zero-downtime deployments'
        ]
    }
}

MARKETING_CONTENT = {
    ContentLength.SHORT: {
        'titles': [
            'Brand Awareness',
            'Lead Generation',
            'Customer Retention',
            'Campaign Results',
            'Market Reach',
            'Conversion Rates'
        ],
        'content': [
            'Brand recognition up 25%',
            'Lead volume increased 40%',
            'Customer retention 94%',
            'Campaign ROI 300%',
            'Market penetration 18%',
            'Conversion rate 12%'
        ],
        'bullets': [
            'Social media engagement doubled',
            'Email campaign CTR improved',
            'Website traffic increased 50%',
            'Customer acquisition cost reduced'
        ]
    },
    ContentLength.MEDIUM: {
        'titles': [
            'Integrated Marketing Campaign Performance',
            'Digital Marketing Strategy Results',
            'Customer Acquisition Analytics',
            'Brand Positioning Enhancement'
        ],
        'content': [
            'Integrated marketing campaign delivered 300% ROI with significant improvements in brand awareness.',
            'Digital marketing strategy increased qualified leads by 40% through targeted content marketing.',
            'Customer acquisition costs reduced by 25% while improving lead quality and conversion rates.',
            'Brand positioning initiative resulted in 35% increase in market recognition and preference.'
        ],
        'bullets': [
            'Multi-channel campaign reached 2.5M prospects with 12% engagement rate',
            'Content marketing strategy generated 1,200 qualified leads per month',
            'Social media presence grew by 150% with 85% positive sentiment analysis',
            'Email marketing automation achieved 28% open rate and 6% click-through rate'
        ]
    },
    ContentLength.LONG: {
        'titles': [
            'Comprehensive Integrated Marketing Campaign Strategy and Performance Analysis with Multi-Channel Attribution'
        ],
        'content': [
            'The comprehensive integrated marketing campaign strategy has delivered exceptional results across all key performance metrics, achieving 300% return on investment through sophisticated multi-channel attribution, advanced audience segmentation, personalized content delivery, and data-driven optimization that has fundamentally transformed our market positioning and customer acquisition capabilities.',
            'Advanced digital marketing ecosystem implementation leveraging artificial intelligence, machine learning algorithms, and predictive analytics has revolutionized customer journey optimization, reducing acquisition costs by 35% while improving lead quality scores by 45% and accelerating sales cycle velocity through personalized engagement strategies and automated nurturing workflows.'
        ],
        'bullets': [
            'Integrated marketing campaign performance exceeded all KPIs with 300% ROI, 2.5M prospect reach, 12% engagement rate, and 40% increase in qualified lead generation through sophisticated multi-channel attribution and advanced audience segmentation strategies',
            'Digital marketing transformation utilizing AI-powered personalization, predictive analytics, and marketing automation achieved 35% reduction in customer acquisition costs, 150% increase in social media engagement, and 45% improvement in lead quality scores',
            'Brand positioning and awareness initiatives resulted in 35% increase in unaided brand recognition, 28% improvement in brand preference metrics, and 94% customer retention rate through consistent messaging, thought leadership content, and customer experience optimization',
            'Content marketing strategy and distribution across 8 channels generated 14,400 qualified leads annually, achieved 28% email open rates, 6% click-through rates, and established market leadership position in 3 key industry segments through valuable, relevant content delivery'
        ]
    }
}

EDUCATIONAL_CONTENT = {
    ContentLength.SHORT: {
        'titles': [
            'Learning Objectives',
            'Course Overview',
            'Key Concepts',
            'Assessment Methods',
            'Student Progress',
            'Learning Outcomes'
        ],
        'content': [
            'Core competencies defined',
            'Curriculum structure established',
            'Foundational concepts covered',
            'Evaluation criteria set',
            'Progress tracking implemented',
            'Learning goals achieved'
        ],
        'bullets': [
            'Interactive learning modules',
            'Real-world case studies',
            'Hands-on practice sessions',
            'Peer collaboration activities'
        ]
    },
    ContentLength.MEDIUM: {
        'titles': [
            'Comprehensive Learning Framework Design',
            'Student Engagement Strategy Implementation',
            'Assessment and Evaluation Methodology',
            'Learning Outcome Measurement'
        ],
        'content': [
            'Comprehensive learning framework designed to address diverse learning styles and competency levels.',
            'Student engagement strategy implementation increased participation by 75% and knowledge retention.',
            'Assessment methodology combines formative and summative evaluations for comprehensive skill measurement.',
            'Learning outcome measurement demonstrates 90% achievement of defined competency standards.'
        ],
        'bullets': [
            'Multi-modal learning approach accommodates visual, auditory, and kinesthetic learners',
            'Gamification elements increased student engagement and motivation by 75%',
            'Competency-based assessment ensures mastery before progression to advanced topics',
            'Continuous feedback loops provide real-time learning adjustments and personalization'
        ]
    },
    ContentLength.LONG: {
        'titles': [
            'Advanced Pedagogical Framework Implementation with Adaptive Learning Technologies and Comprehensive Assessment Strategies'
        ],
        'content': [
            'The advanced pedagogical framework implementation leverages cutting-edge adaptive learning technologies, artificial intelligence-driven personalization, and comprehensive assessment strategies to create an immersive, engaging, and highly effective educational experience that addresses individual learning preferences, accommodates diverse competency levels, and ensures measurable skill development through evidence-based instructional design principles.',
            'Innovative student engagement and retention strategy incorporating gamification elements, peer-to-peer learning networks, real-world project applications, and continuous feedback mechanisms has revolutionized the learning experience, achieving 90% course completion rates, 85% knowledge retention after 6 months, and 95% student satisfaction scores while preparing learners for immediate practical application in professional environments.'
        ],
        'bullets': [
            'Adaptive learning technology implementation with AI-powered personalization algorithms provides individualized learning paths, real-time difficulty adjustment, and predictive analytics to optimize knowledge acquisition and retention for each student based on learning patterns and performance data',
            'Comprehensive assessment strategy combining formative, summative, and authentic evaluations ensures mastery-based progression, provides detailed competency mapping, and generates actionable insights for continuous curriculum improvement and individualized learning support',
            'Student engagement and motivation enhancement through gamification, interactive simulations, collaborative projects, and peer learning networks resulted in 75% increase in participation, 90% course completion rate, and 95% student satisfaction scores',
            'Learning outcome measurement and analytics demonstrate 90% achievement of defined competency standards, 85% knowledge retention after 6 months, and 92% successful practical application in professional contexts through comprehensive tracking and evaluation systems'
        ]
    }
}

# Formatting patterns for content variation
FORMATTING_PATTERNS = {
    'bold': ['**{}**', 'Bold emphasis'],
    'italic': ['*{}*', 'Italic emphasis'], 
    'underline': ['___{}___', 'Underlined text'],
    'bold_italic': ['***{}***', 'Bold and italic'],
    'bold_underline': ['**___{}___**', 'Bold and underlined'],
    'italic_underline': ['*___{}___*', 'Italic and underlined'],
    'all_formatting': ['***___{}___***', 'All formatting combined']
}


class ContentGenerator:
    """Dynamic content generation system for testing."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize content generator with optional random seed."""
        if seed is not None:
            random.seed(seed)
    
    def get_content_library(self, content_type: ContentType) -> Dict[ContentLength, Dict[str, List[str]]]:
        """Get content library for specified type."""
        libraries = {
            ContentType.BUSINESS: BUSINESS_CONTENT,
            ContentType.TECHNICAL: TECHNICAL_CONTENT,
            ContentType.MARKETING: MARKETING_CONTENT,
            ContentType.EDUCATIONAL: EDUCATIONAL_CONTENT
        }
        return libraries.get(content_type, BUSINESS_CONTENT)
    
    def build_column_content(self, num_columns: int, content_type: ContentType = ContentType.BUSINESS, 
                           content_length: ContentLength = ContentLength.MEDIUM) -> List[Dict[str, str]]:
        """Generate content for multi-column layouts."""
        library = self.get_content_library(content_type)[content_length]
        
        columns = []
        for i in range(num_columns):
            title_idx = i % len(library['titles'])
            content_idx = i % len(library['content'])
            
            columns.append({
                'title': library['titles'][title_idx],
                'content': library['content'][content_idx]
            })
        
        return columns
    
    def build_comparison_content(self, comparison_type: str = 'features', 
                               content_type: ContentType = ContentType.BUSINESS) -> Dict[str, Dict[str, str]]:
        """Generate left/right comparison content."""
        library = self.get_content_library(content_type)[ContentLength.MEDIUM]
        
        comparison_templates = {
            'features': {
                'left': {'title': 'Current Solution', 'content': library['content'][0]},
                'right': {'title': 'Proposed Solution', 'content': library['content'][1]}
            },
            'before_after': {
                'left': {'title': 'Before', 'content': library['content'][2]},
                'right': {'title': 'After', 'content': library['content'][3]}
            },
            'pros_cons': {
                'left': {'title': 'Advantages', 'content': library['bullets'][0]},
                'right': {'title': 'Considerations', 'content': library['bullets'][1]}
            }
        }
        
        return comparison_templates.get(comparison_type, comparison_templates['features'])
    
    def build_table_content(self, rows: int, cols: int, include_formatting: bool = True) -> Dict[str, Any]:
        """Generate table data with optional formatting."""
        headers = ['Feature', 'Status', 'Priority', 'Owner', 'Timeline'][:cols]
        
        if include_formatting:
            headers = [self.apply_random_formatting(header) for header in headers]
        
        data = [headers]
        
        # Sample row data
        row_samples = [
            ['Authentication', 'Complete', 'High', 'Security Team', 'Q1'],
            ['User Management', 'In Progress', 'Medium', 'Platform Team', 'Q2'],
            ['Reporting', 'Planned', 'Low', 'Analytics Team', 'Q3'],
            ['API Integration', 'Blocked', 'Critical', 'Integration Team', 'Q1'],
            ['Performance Monitoring', 'Testing', 'High', 'DevOps Team', 'Q2']
        ]
        
        for i in range(rows - 1):  # -1 for header row
            row_idx = i % len(row_samples)
            row = row_samples[row_idx][:cols]
            
            if include_formatting:
                row = [self.apply_random_formatting(cell) for cell in row]
            
            data.append(row)
        
        return {
            'data': data,
            'header_style': 'dark_blue_white_text',
            'row_style': 'alternating_light_gray',
            'border_style': 'thin_gray'
        }
    
    def apply_formatting_variations(self, content: str) -> Dict[str, str]:
        """Add bold/italic/underline variations to content."""
        variations = {}
        
        for format_name, (pattern, description) in FORMATTING_PATTERNS.items():
            variations[format_name] = pattern.format(content)
        
        return variations
    
    def apply_random_formatting(self, text: str) -> str:
        """Apply random formatting to text."""
        format_options = list(FORMATTING_PATTERNS.keys())
        format_choice = random.choice(format_options + ['none'])
        
        if format_choice == 'none':
            return text
        
        pattern, _ = FORMATTING_PATTERNS[format_choice]
        return pattern.format(text)
    
    def generate_agenda_content(self, num_items: int = 6) -> List[Dict[str, str]]:
        """Generate agenda items for agenda layouts."""
        agenda_templates = [
            'Opening remarks and introductions',
            'Market analysis and trends review', 
            'Product roadmap updates',
            'Financial performance review',
            'Strategic initiatives overview',
            'Q&A session and next steps',
            'Risk assessment and mitigation',
            'Customer feedback analysis',
            'Competitive landscape review',
            'Technology platform updates'
        ]
        
        agenda_items = []
        for i in range(num_items):
            item_idx = i % len(agenda_templates)
            agenda_items.append({
                'number': f"{i+1:02d}",
                'item': agenda_templates[item_idx]
            })
        
        return agenda_items
    
    def generate_swot_content(self) -> Dict[str, str]:
        """Generate SWOT analysis content."""
        return {
            'strengths': 'Strong market position with proven technology and dedicated team',
            'weaknesses': 'Limited geographic presence and high operational costs',
            'opportunities': 'Emerging markets and digital transformation trends',
            'threats': 'Increased competition and regulatory changes'
        }
    
    def generate_content_variation(self, base_content: str, length: ContentLength, 
                                 add_formatting: bool = False) -> ContentVariation:
        """Generate content variation with specified length and formatting."""
        # Adjust content length
        if length == ContentLength.SHORT:
            # Take first sentence or truncate
            sentences = base_content.split('.')
            content = sentences[0] + '.' if sentences else base_content[:50] + '...'
        elif length == ContentLength.LONG:
            # Expand content with additional details
            content = f"{base_content} Additional details and comprehensive analysis provide deeper insights into the implementation strategy, expected outcomes, and long-term benefits for stakeholders."
        else:
            content = base_content
        
        # Apply formatting if requested
        if add_formatting:
            content = self.apply_random_formatting(content)
        
        return ContentVariation(
            text=content,
            length=length,
            has_formatting=add_formatting
        )


# Convenience functions for easy testing
def get_sample_business_content(length: ContentLength = ContentLength.MEDIUM) -> Dict[str, List[str]]:
    """Get sample business content for specified length."""
    return BUSINESS_CONTENT[length]


def get_sample_technical_content(length: ContentLength = ContentLength.MEDIUM) -> Dict[str, List[str]]:
    """Get sample technical content for specified length."""
    return TECHNICAL_CONTENT[length]


def get_formatted_content_samples() -> Dict[str, str]:
    """Get sample content with various formatting applied."""
    base_text = "Important information"
    samples = {}
    
    for format_name, (pattern, description) in FORMATTING_PATTERNS.items():
        samples[format_name] = pattern.format(base_text)
    
    return samples


# Factory function for quick content generation
def create_content_generator(content_type: ContentType = ContentType.BUSINESS, 
                           seed: Optional[int] = None) -> ContentGenerator:
    """Factory function to create configured content generator."""
    return ContentGenerator(seed=seed)