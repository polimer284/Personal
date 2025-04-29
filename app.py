import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="Whatfix - Digital Adoption Platform",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
:root {
    --primary-color: #f47e35;
    --secondary-color: #31204a;
    --accent-color: #f47e35;
    --background-color: #f8f9fa;
    --text-color: #212529;
}

.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

.stButton>button {
    background-color: var(--primary-color);
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    transition: all 0.3s;
}

.stButton>button:hover {
    background-color: var(--secondary-color);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transform: translateY(-2px);
}

h1, h2, h3 {
    color: var(--secondary-color);
}

.highlight-card {
    border: 1px solid #e9ecef;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    background-color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: all 0.3s;
}

.highlight-card:hover {
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    transform: translateY(-5px);
}

.whatfix-option {
    border: 2px solid #e9ecef;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
    cursor: pointer;
    transition: all 0.2s;
}

.whatfix-option:hover {
    border-color: var(--accent-color);
    background-color: #f8f9fa;
}

.whatfix-option.selected {
    border-color: var(--primary-color);
    background-color: rgba(244, 126, 53, 0.1);
}

.feature-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    border-radius: 10px;
    background-color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    margin-bottom: 1rem;
}

.feature-icon {
    font-size: 2rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.feature-title {
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.award-container {
    padding: 0.5rem;
    border-radius: 5px;
    margin-bottom: 0.5rem;
    background-color: rgba(244, 126, 53, 0.1);
}

.customer-logo {
    height: 60px;
    margin: 10px;
    filter: grayscale(100%);
    transition: all 0.3s;
}

.customer-logo:hover {
    filter: grayscale(0%);
    transform: scale(1.1);
}

.category-button {
    padding: 15px;
    border-radius: 10px;
    margin: 5px;
    text-align: center;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
}

.category-button:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h1 style="font-size: 3rem; margin-bottom: 0.5rem; color: #31204a;">
        <span style="color: #f47e35;">W</span>hatfix
    </h1>
    <p style="font-size: 1.2rem; color: #6c757d;">A Leading Digital Adoption Platform (by Yoon)</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Overview"

# Define content for different sections
overview_content = {
    "title": "Company Overview",
    "description": """
    Founded in 2014, Whatfix is a global B2B SaaS organization that has been recognized as a leader in the digital adoption platforms (DAP) category for the past 4+ years by leading analyst firms like Gartner, Forrester, IDC, and Everest Group.
    
    Over the past 3 years, Whatfix has accelerated its pace of innovation and forayed into analytics and application simulation categories to become a multi-product organization.
    
    Whatfix has 1000+ employees present across the US, India, UK, Germany, Singapore, Philippines, France, Netherlands, Poland, Ukraine, South Korea, and Australia and is currently used by 700+ customers across the globe, including 80+ Fortune 500 companies.
    """,
    "stats": [
        {"label": "Founded", "value": "2014"},
        {"label": "Employees", "value": "1000+"},
        {"label": "Customers", "value": "700+"},
        {"label": "Fortune 500 Clients", "value": "80+"},
        {"label": "Global Presence", "value": "12 Countries"}
    ]
}

products_content = {
    "description": """
    Whatfix empowers enterprises to enhance user productivity and experience, driving accelerated ROI from digital investments. Its comprehensive product suite includes:
    """,
    "products": [
        {
            "name": "Product Analytics and Enterprise Insights",
            "description": "Monitor user behavior and digital friction, facilitating data-driven decision-making.",
            "icon": "📊"
        },
        {
            "name": "Mirror",
            "description": "Application simulation software for immersive training and product demonstrations, significantly reducing IT infrastructure and manpower costs.",
            "icon": "🔍"
        },
        {
            "name": "Hub and DAP for Web, Mobile, and Desktop",
            "description": "Application enablement and adoption, change management, and learning in the flow of work.",
            "icon": "🖥️"
        }
    ],
    "value_props": """
    This suite leverages the concept of userization (making technology user-savvy) and GenAI. It enables enterprises to improve cost efficiency and stimulate user productivity and engagement across their application portfolio. As a result, it maximizes the value of their digital investments.
    """
}

customers_content = {
    "description": "Whatfix serves 700+ customers (70% Americas, 20% Europe, 10% RoW) across various industries:",
    "logos": [
        "UPS", "Schneider Electric", "Compass Group", "Microsoft", "Aramark", "M&S",
        "ICICI Bank", "Experian", "ManpowerGroup", "Decathlon", "Cisco", "Beacon",
        "Caterpillar", "Omron", "Brown & Brown Insurance", "BD", "Avnet"
    ],
    "testimonials": [
        {
            "text": "Whatfix helped us accelerate our Bullhorn ATS transformation and maximize ROI by providing support in the flow of work for our recruiters.",
            "company": "ManpowerGroup"
        },
        {
            "text": "With Whatfix's in-app guidance and automation on Guidewire, we reduced errors and accelerated claims processing, leading to higher employee productivity.",
            "company": "A Leading US Insurance Provider"
        },
        {
            "text": "We connected Smart Tips with our learning management system so that each new user could engage with videos and other useful materials, replacing the unwieldy in-person training.",
            "company": "Ferring Pharmaceuticals"
        }
    ]
}

achievements_content = {
    "funding": {
        "title": "Investors & Funding",
        "description": "Whatfix has raised a total of ~$140M. Most recently, Whatfix raised a Series D round of $90M led by SoftBank and Sequoia Capital. Other investors include Cisco Investments (also a customer), Eight Roads Ventures (a division of Fidelity Investments), Sequoia Capital India, Dragoneer Investments, F-Prime Capital, Helion Venture Partners, and Stellaris Venture Partners."
    },
    "recognition": {
        "title": "Analyst Recognitions",
        "items": [
            "Sole Vendor Named as Customers' Choice: 2024 Gartner® Voice of the Customer for Digital Adoption Platform Report",
            "Leader in Inaugural IDC MarketScape: Worldwide DAP 2024 Vendor Assessment",
            "Leader in the inaugural Forrester New Wave™: Digital Adoption Platforms",
            "Leader (fourth consecutive year) and a Star Performer: Everest Group Digital Adoption Platform (DAP) PEAK Matrix® Assessment 2023",
            "Recognized DAP vendor: 2023 Gartner® Market Guide for Digital Adoption Platforms",
            "Leader in Everest Group's first: Workplace Employee Experience Management (WEEM) Platforms PEAK Matrix®"
        ]
    },
    "awards": {
        "title": "Key Industry Awards",
        "items": [
            "Highest-Ranking DAP on 2023 Deloitte Technology Fast 500™ North America for Third Consecutive Year",
            "Customer Service Department of the Year, Computer Services, Gold Stevie®",
            "Disruptor Company, Information Technology Software, Gold Globee® Winner Khadim Batti",
            "Scale-up SaaS Startup of the Year, SaasBoomi Annual 2023",
            "CEO of the Year, IT Software, Gold Globee® Winner (Khadim Batti)",
            "CTO of the Year, IT Software, Gold Globee® Winner (Vara kumar)",
            "Best Innovative or Emerging Tech Solution, Employee Experience by HR Tech Awards",
            "Hurun India Future Unicorn Award 2023",
            "Certified as a \"Great Place to Work\" for the year 2022-2023",
            "Featured on the Nasdaq Tower for ranking as 20th Highest-Rated Private Cloud Computing for Companies To Work For by Battery Ventures, in association with Glassdoor",
            "Among the highest-rated DAPs in the market - G2 (4.6/5), Gartner Peer Insights (4.5/5), TrustRadius (9.3/10) and CSAT 99.6%"
        ]
    }
}

use_cases_content = {
    "description": "Whatfix serves several use cases, collectively enhancing users' time to proficiency and application adoption. Some of the key use cases where Whatfix has proven value include:",
    "categories": [
        {
            "name": "Digital Adoption Platform",
            "items": [
                "Employee Onboarding & Training",
                "Application Change Management",
                "Process Compliance & Governance",
                "User Support & Self-Help",
                "Feature Adoption & User Engagement"
            ]
        },
        {
            "name": "Product Analytics",
            "items": [
                "User Behavior Analysis",
                "Process Optimization",
                "Friction Point Identification",
                "Process Compliance Monitoring",
                "ROI Measurement"
            ]
        },
        {
            "name": "Mirror",
            "items": [
                "Risk-Free Sandbox Environment",
                "Hands-On Training",
                "Process Simulation",
                "User Acceptance Testing",
                "New Feature Demonstrations"
            ]
        }
    ],
    "industries": [
        "Banking & Financial Services",
        "Insurance",
        "Healthcare",
        "Pharmaceuticals",
        "Retail",
        "Manufacturing",
        "Technology",
        "Telecommunications",
        "Public Sector",
        "Staffing & Recruiting"
    ]
}

culture_content = {
    "description": "Whatfix's company culture is built on strong values that drive its success:",
    "values": [
        {
            "name": "Treat people with empathy",
            "description": "A debate/discussion/discourse is worthless if you are not thinking about the customer. We go above and beyond to add value to customers.",
            "icon": "❤️"
        },
        {
            "name": "Hustle Mode ON",
            "description": "We want every interaction to be quick, be it customer queries, legal inquiries, feature releases, or our application performance. Most decisions are reversible. We want to make such decisions faster so that our execution is equally fast.",
            "icon": "🚀"
        },
        {
            "name": "Ethics and Integrity above all else",
            "description": "We do not lie, steal, or represent false details to anyone whom we interact with. We portray the correct picture and our customers and partners appreciate us for our honesty.",
            "icon": "🛡️"
        },
        {
            "name": "Transparent communication",
            "description": "We mandate direct, open, and honest communication & feedback. Any other way dilutes our focus on customers and our ability to collaborate and compete.",
            "icon": "💬"
        },
        {
            "name": "Fail fast, Scale fast",
            "description": "We experiment, fail fast, learn from it, and re-experiment. We are not afraid of failures, We use them as stepping stones. We scale fast once we see the success of the experiment.",
            "icon": "📈"
        },
        {
            "name": "Do it as you own it",
            "description": "We do it as we own it, There is nothing outside the job scope. We are accountable for results, not for plan/execution/activities.",
            "icon": "🏆"
        }
    ]
}

future_content = {
    "title": "Why Whatfix is the Next Big Thing?",
    "items": [
        {
            "title": "Large Market size",
            "description": "$25-30 billion is the current addressable market size for Whatfix. The digital revolution demands agility and maximizing the value of every software investment. Employees typically use 12 to 13 applications daily, leading to digital friction as they are expected to be proficient in each one."
        },
        {
            "title": "Validation",
            "description": "Whatfix has several global 2000 customers, including over 80+ Fortune 500 companies. This includes companies such as Experian, AbleTo, Sophos, Sentry, ICICI Bank, and more."
        },
        {
            "title": "Continuous Growth",
            "description": "Whatfix has been recognized as one of the fastest-growing SaaS companies worldwide. The company is investing heavily in R&D and has acquired three companies so far to catalyze its product innovation, including Airim in 2019, Nittio Learn in 2021, and Leap in 2022."
        },
        {
            "title": "Innovation with AI",
            "description": "As a leader in the DAP market, Whatfix is driving innovation by leveraging Generative AI to shape the future of DAPs. The AI integration enhances DAP functionalities, revolutionizing user interactions with technology."
        }
    ]
}

# Define main categories with colors
categories = [
    {"name": "Overview", "color": "#f47e35", "icon": "ℹ️"},
    {"name": "Products", "color": "#4361ee", "icon": "🛠️"},
    {"name": "Customers", "color": "#3a0ca3", "icon": "👥"},
    {"name": "Achievements", "color": "#7209b7", "icon": "🏆"},
    {"name": "Use Cases", "color": "#f72585", "icon": "💼"},
    {"name": "Culture", "color": "#4cc9f0", "icon": "🌟"},
    {"name": "Future Vision", "color": "#560bad", "icon": "🔮"},
    {"name": "Self Introduction", "color": "#1f77b4", "icon": "👋"}
]

# Create top navigation with colored buttons in a grid
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
cols = st.columns(len(categories))
for i, cat in enumerate(categories):
    with cols[i]:
        st.markdown(
            f"""
            <div 
                class="category-button" 
                style="background-color: {cat['color']}; color: white;"
                onclick="this.classList.toggle('selected'); window.parent.postMessage({{command: 'streamlitMessage', type: 'buttonClicked', value: '{cat['name']}'}}, '*');"
            >
                {cat['icon']} {cat['name']}
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button(cat['name'], key=f"btn_{cat['name']}", help=f"View {cat['name']} information"):
            st.session_state.current_page = cat['name']
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Display the selected page content
st.markdown("---")

if st.session_state.current_page == "Overview":
    st.header(f"📌 {overview_content['title']}")
    
    # Overview layout with two columns
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div class="highlight-card">
            {overview_content['description']}
        </div>
        """, unsafe_allow_html=True)
        
        # Global presence map (simple visualization)
        st.subheader("Global Presence")
        df_locations = pd.DataFrame({
            'Country': ['USA', 'India', 'UK', 'Germany', 'Singapore', 'Australia', 'France', 'Netherlands', 'Poland', 'Ukraine', 'South Korea', 'Philippines'],
            'Employees': [200, 600, 30, 25, 20, 15, 10, 10, 10, 10, 10, 10],
            'Latitude': [37.0902, 20.5937, 51.5074, 51.1657, 1.3521, -25.2744, 46.2276, 52.3676, 51.9194, 48.3794, 35.9078, 14.5995],
            'Longitude': [-95.7129, 78.9629, -0.1278, 10.4515, 103.8198, 133.7751, 2.2137, 4.9041, 19.1451, 31.1656, 127.7669, 120.9842]
        })
        
        fig = px.scatter_geo(
            df_locations, 
            lat='Latitude',
            lon='Longitude',
            size='Employees',
            hover_name='Country',
            color_discrete_sequence=['#f47e35'],
            title="Whatfix Global Presence",
            projection="natural earth"
        )
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Quick Facts")
        for stat in overview_content['stats']:
            st.markdown(f"""
            <div style="padding: 10px; margin-bottom: 10px; border-radius: 5px; background-color: rgba(244, 126, 53, 0.1); text-align: center;">
                <h3 style="color: #f47e35; margin: 0;">{stat['value']}</h3>
                <p style="margin: 0;">{stat['label']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Company timeline
    st.subheader("Company Timeline")
    timeline_data = [
        {"year": "2014", "event": "Whatfix founded"},
        {"year": "2015", "event": "Raised seed funding"},
        {"year": "2016", "event": "First enterprise customers"},
        {"year": "2017", "event": "Expanded to US market"},
        {"year": "2019", "event": "Series B funding & Acquired Airim"},
        {"year": "2021", "event": "Series C funding & Acquired Nittio Learn"},
        {"year": "2022", "event": "Series D funding & Acquired Leap"},
        {"year": "2023", "event": "Recognized as Leader by major analysts"},
        {"year": "2024", "event": "Expanded GenAI capabilities"}
    ]
    
    cols = st.columns(len(timeline_data))
    for i, item in enumerate(timeline_data):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; border-top: 3px solid #f47e35;">
                <p style="font-weight: bold; margin: 0;">{item['year']}</p>
                <p style="font-size: 0.8rem;">{item['event']}</p>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.current_page == "Products":
    st.header("🛠️ Product Suite")
    
    st.markdown(f"""
    <div class="highlight-card">
        {products_content['description']}
    </div>
    """, unsafe_allow_html=True)
    
    # Product cards in a grid
    product_cols = st.columns(len(products_content['products']))
    
    for i, product in enumerate(products_content['products']):
        with product_cols[i]:
            st.markdown(f"""
            <div class="highlight-card" style="height: 250px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 2.5rem; text-align: center; color: #f47e35; margin-bottom: 10px;">{product['icon']}</div>
                    <h3 style="text-align: center;">{product['name']}</h3>
                    <p>{product['description']}</p>
                </div>
                <div style="text-align: center;">
                    <button style="background-color: #f47e35; color: white; border: none; padding: 5px 15px; border-radius: 5px; cursor: pointer;">Learn More</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="highlight-card">
        <h3>The Whatfix Advantage</h3>
        {products_content['value_props']}
    </div>
    """, unsafe_allow_html=True)
    
    # Product benefits
    st.subheader("Key Benefits")
    benefit_cols = st.columns(3)
    
    benefits = [
        {"title": "Reduce Support Efforts & Training Time", "icon": "⏱️", "description": "Cut down on training time by up to 60% and reduce support tickets by providing in-context guidance."},
        {"title": "Accelerate Product Adoption", "icon": "📈", "description": "Drive feature usage and adoption with contextual walkthroughs and in-app guidance."},
        {"title": "Save Costs & Resources", "icon": "💰", "description": "Maximize ROI on software investments by ensuring users can effectively utilize all features."}
    ]
    
    for i, benefit in enumerate(benefits):
        with benefit_cols[i]:
            st.markdown(f"""
            <div class="highlight-card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px; color: #f47e35;">{benefit['icon']}</div>
                <h3>{benefit['title']}</h3>
                <p>{benefit['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Comparison with competitors
    st.subheader("Competitive Advantage")
    
    comparison_data = {
        'Feature': ['No-Code Editor', 'Self-Help Widget', 'Desktop App Support', 'Mobile App Support', 'Multi-Format Content', 'Auto Translation', 'Analytics', 'Sandbox Environment'],
        'Whatfix': ['✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅'],
        'Competitor A': ['✅', '❌', '❌', '✅', '❌', '❌', '✅', '❌'],
        'Competitor B': ['✅', '✅', '❌', '❌', '❌', '✅', '✅', '❌'],
        'Competitor C': ['✅', '❌', '❌', '✅', '❌', '❌', '❌', '❌']
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    
    fig = go.Figure(data=[
        go.Table(
            header=dict(
                values=list(df_comparison.columns),
                fill_color='#f47e35',
                align='center',
                font=dict(color='white', size=12)
            ),
            cells=dict(
                values=[df_comparison[col] for col in df_comparison.columns],
                fill_color=[['#f8f9fa', '#f8f9fa', '#f8f9fa', '#f8f9fa']] * len(df_comparison),
                align='center'
            )
        )
    ])
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.current_page == "Customers":
    st.header("👥 Our Customers")
    
    st.markdown(f"""
    <div class="highlight-card">
        {customers_content['description']}
    </div>
    """, unsafe_allow_html=True)
    
    # Customer distribution by region
    st.subheader("Customer Distribution")
    
    region_data = {
        'Region': ['Americas', 'Europe', 'Rest of World'],
        'Percentage': [70, 20, 10]
    }
    
    df_regions = pd.DataFrame(region_data)
    
    fig = px.pie(
        df_regions, 
        names='Region', 
        values='Percentage',
        color_discrete_sequence=['#f47e35', '#4361ee', '#31204a'],
        hole=0.4
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,
        legend=dict(orientation='h', y=-0.1)
    )
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        ### Industry Breakdown
        
        Whatfix serves customers across various industries:
        
        - **Financial Services & Insurance**: 25%
        - **Technology & Software**: 20%
        - **Healthcare & Pharma**: 15%
        - **Manufacturing**: 10%
        - **Retail & Consumer Goods**: 10%
        - **Telecommunications**: 5%
        - **Others**: 15%
        """)
    
    # Customer logos
    st.subheader("Some of Our Notable Customers")
    
    # Display logos in rows
    rows = 3
    logos_per_row = len(customers_content['logos']) // rows + (1 if len(customers_content['logos']) % rows else 0)
    
    for r in range(rows):
        cols = st.columns(logos_per_row)
        for i in range(logos_per_row):
            idx = r * logos_per_row + i
            if idx < len(customers_content['logos']):
                with cols[i]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 10px; background-color: white; border-radius: 5px; margin: 5px; height: 100px; display: flex; align-items: center; justify-content: center;">
                        <p style="font-weight: bold; color: #31204a;">{customers_content['logos'][idx]}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Customer testimonials
    st.subheader("Customer Success Stories")
    
    for i, testimonial in enumerate(customers_content['testimonials']):
        st.markdown(f"""
        <div class="highlight-card" style="border-left: 5px solid #f47e35;">
            <p style="font-style: italic;">"{testimonial['text']}"</p>
            <p style="text-align: right; font-weight: bold;">— {testimonial['company']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Success metrics
    st.subheader("Customer Success Metrics")
    
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        st.metric(label="Average Support Ticket Reduction", value="60%", delta="↓")
    
    with metric_cols[1]:
        st.metric(label="Average Training Time Reduction", value="50%", delta="↓")
    
    with metric_cols[2]:
        st.metric(label="Average Productivity Increase", value="37%", delta="↑")
    
    with metric_cols[3]:
        st.metric(label="Customer Satisfaction (CSAT)", value="99.6%", delta="↑")

elif st.session_state.current_page == "Achievements":
    st.header("🏆 Achievements & Recognition")
    
    # Funding information
    st.subheader(achievements_content["funding"]["title"])
    
    st.markdown(f"""
    <div class="highlight-card">
        {achievements_content["funding"]["description"]}
    </div>
    """, unsafe_allow_html=True)
    
    # Funding rounds visualization
    funding_data = {
        'Round': ['Seed', 'Series A', 'Series B', 'Series C', 'Series D'],
        'Amount (in millions $)': [3, 12, 35, 90, 140],
        'Year': ['2015', '2017', '2019', '2021', '2023'] 
    }
    
    df_funding = pd.DataFrame(funding_data)
    
    fig = px.bar(
        df_funding,
        x='Round',
        y='Amount (in millions $)',
        text='Amount (in millions $)',
        color='Amount (in millions $)',
        color_continuous_scale=px.colors.sequential.Oranges,
        labels={'Amount (in millions $)': 'Amount ($ millions)'},
        title="Whatfix Funding Journey"
    )
    
    fig.update_traces(
        texttemplate='$%{text}M',
        textposition='outside'
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Funding Round",
        yaxis_title="Amount ($ millions)",
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Analyst recognitions
    st.subheader(achievements_content["recognition"]["title"])
    
    for item in achievements_content["recognition"]["items"]:
        st.markdown(f"""
        <div class="award-container">
            <p>✓ {item}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Industry awards
    st.subheader(achievements_content["awards"]["title"])
    
    for i, item in enumerate(achievements_content["awards"]["items"]):
        st.markdown(f"""
        <div class="award-container" style="background-color: rgba({244 if i % 2 == 0 else 67}, {126 if i % 2 == 0 else 97}, {53 if i % 2 == 0 else 238}, 0.1);">
            <p>🏆 {item}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Patent information
    st.subheader("Patents & Innovation")
    
    st.markdown("""
    <div class="highlight-card">
        <p>Whatfix has been granted five technology patents by the U.S. Patent Office and has filed 15 applications. The company is continuously innovating in the digital adoption space, particularly with GenAI integration.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Acquisitions
    st.subheader("Strategic Acquisitions")
    
    acquisitions = [
        {"name": "Airim", "year": "2019", "description": "AI-powered personalization engine"},
        {"name": "Nittio Learn", "year": "2021", "description": "Learning management system"},
        {"name": "Leap", "year": "2022", "description": "Advanced analytics platform"}
    ]
    
    cols = st.columns(len(acquisitions))
    
    for i, acquisition in enumerate(acquisitions):
        with cols[i]:
            st.markdown(f"""
            <div class="highlight-card" style="text-align: center;">
                <h3>{acquisition["name"]}</h3>
                <p style="font-weight: bold; color: #f47e35;">Acquired in {acquisition["year"]}</p>
                <p>{acquisition["description"]}</p>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.current_page == "Use Cases":
    st.header("💼 Use Cases")
    
    st.markdown(f"""
    <div class="highlight-card">
        {use_cases_content["description"]}
    </div>
    """, unsafe_allow_html=True)
    
    # Use case categories
    for category in use_cases_content["categories"]:
        st.subheader(category["name"])
        
        items_per_row = 3
        rows = len(category["items"]) // items_per_row + (1 if len(category["items"]) % items_per_row else 0)
        
        for r in range(rows):
            cols = st.columns(items_per_row)
            for i in range(items_per_row):
                idx = r * items_per_row + i
                if idx < len(category["items"]):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="highlight-card" style="text-align: center; height: 100px; display: flex; align-items: center; justify-content: center;">
                            <p style="margin: 0;">{category["items"][idx]}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Industry applications
    st.subheader("Industry Applications")
    
    # Create columns for industry sections
    industry_cols = st.columns(2)
    
    # List of industries
    industries_left = use_cases_content["industries"][:len(use_cases_content["industries"])//2]
    industries_right = use_cases_content["industries"][len(use_cases_content["industries"])//2:]
    
    with industry_cols[0]:
        for industry in industries_left:
            st.markdown(f"""
            <div class="highlight-card" style="margin-bottom: 10px; cursor: pointer;">
                <h4>{industry}</h4>
                <p style="font-size: 0.8rem; color: #6c757d;">Click to expand</p>
            </div>
            """, unsafe_allow_html=True)
    
    with industry_cols[1]:
        for industry in industries_right:
            st.markdown(f"""
            <div class="highlight-card" style="margin-bottom: 10px; cursor: pointer;">
                <h4>{industry}</h4>
                <p style="font-size: 0.8rem; color: #6c757d;">Click to expand</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Featured case studies
    st.subheader("Featured Case Studies")
    
    case_studies = [
        {
            "title": "Manpower Group",
            "description": "Accelerated Bullhorn ATS transformation and maximized ROI by providing support in the flow of work for recruiters.",
            "results": ["Reduced user onboarding time by 50%", "Decreased ATS errors by 60%", "Integrated SOPs and best practices directly into the workflow"]
        },
        {
            "title": "Insurance Provider",
            "description": "Implemented in-app guidance and automation on Guidewire to reduce claims processing errors and accelerate processing times.",
            "results": ["Improved employee productivity by 40%", "Enhanced claims processing governance", "Created better policyholder experience"]
        },
        {
            "title": "Ferring Pharmaceuticals",
            "description": "Standardized CLM processes and reimagined how employees use the Icertis platform with in-app guidance.",
            "results": ["4,000 Smart Tips shown to users daily", "96% successful search rate in Self Help", "Reduced new user onboarding time"]
        }
    ]
    
    for case in case_studies:
        st.markdown(f"""
        <div class="highlight-card">
            <h3>{case["title"]}</h3>
            <p>{case["description"]}</p>
            <h4>Results:</h4>
            <ul>
                {"".join(f"<li>{result}</li>" for result in case["results"])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_page == "Culture":
    st.header("🌟 Company Culture")
    
    st.markdown(f"""
    <div class="highlight-card">
        {culture_content["description"]}
    </div>
    """, unsafe_allow_html=True)
    
    # Display values in a grid
    values_per_row = 3
    rows = len(culture_content["values"]) // values_per_row + (1 if len(culture_content["values"]) % values_per_row else 0)
    
    for r in range(rows):
        cols = st.columns(values_per_row)
        for i in range(values_per_row):
            idx = r * values_per_row + i
            if idx < len(culture_content["values"]):
                value = culture_content["values"][idx]
                with cols[i]:
                    st.markdown(f"""
                    <div class="highlight-card" style="height: 250px; display: flex; flex-direction: column;">
                        <div style="font-size: 2rem; text-align: center; color: #f47e35; margin-bottom: 10px;">{value["icon"]}</div>
                        <h3 style="text-align: center;">{value["name"]}</h3>
                        <p>{value["description"]}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Company work culture and environment
    st.subheader("Work Culture & Environment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Great Place to Work
        
        Whatfix has been certified as a "Great Place to Work" for the year 2022-2023 and was featured on the Nasdaq Tower for ranking as 20th Highest-Rated Private Cloud Computing Companies To Work For by Battery Ventures, in association with Glassdoor.
        
        ### Key Culture Highlights
        
        - **Global Team**: Diverse workforce across 12 countries
        - **Continuous Learning**: Regular upskilling and growth opportunities
        - **Work-Life Balance**: Flexible work arrangements and wellness programs
        - **Innovation Focus**: 10% of time dedicated to exploring new ideas
        - **Customer-Centric**: Every decision is made with the customer in mind
        """)
    
    with col2:
        st.markdown("""
        ### Employee Recognition
        
        - Gold Globee® Winners for CEO and CTO of the Year in IT Software
        - Featured in multiple "Best Places to Work" lists
        - Strong employee satisfaction ratings
        - Transparent communication culture
        - Regular hackathons and innovation challenges
        """)
    
    # Leadership team
    st.subheader("Leadership Team")
    
    leaders = [
        {"name": "Khadim Batti", "position": "Co-founder & CEO", "info": "Serial entrepreneur with expertise in product and GTM strategy"},
        {"name": "Vara Kumar Namburu", "position": "Co-founder & CTO", "info": "Technology visionary with deep expertise in enterprise software"},
        {"name": "Vispi Daver", "position": "Chief Revenue Officer", "info": "Experienced enterprise sales leader with expertise in global expansion"}
    ]
    
    leader_cols = st.columns(len(leaders))
    
    for i, leader in enumerate(leaders):
        with leader_cols[i]:
            st.markdown(f"""
            <div class="highlight-card" style="text-align: center;">
                <h3>{leader["name"]}</h3>
                <p style="font-weight: bold; color: #f47e35;">{leader["position"]}</p>
                <p>{leader["info"]}</p>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.current_page == "Future Vision":
    st.header("🔮 Future Vision")
    
    st.markdown(f"""
    <div class="highlight-card">
        <h2>Why Whatfix is the Next Big Thing?</h2>
    </div>
    """, unsafe_allow_html=True)
    
    for item in future_content["items"]:
        st.markdown(f"""
        <div class="highlight-card">
            <h3>{item["title"]}</h3>
            <p>{item["description"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # AI future
    st.subheader("The GenAI-Powered Future of DAPs")
    
    st.markdown("""
    Whatfix is driving innovation by leveraging Generative AI to shape the future of Digital Adoption Platforms. The AI integration enhances DAP functionalities in several ways:
    """)
    
    ai_features = [
        "AI Read: Quick extraction and summarization of knowledge repositories and user actions",
        "AI Write: In-app digital scribe for notes, emails, and content creation",
        "AI Do: Natural language instructions to perform in-app tasks automatically",
        "Personalized user experiences based on role, behavior, and needs",
        "Intelligent task recommendations and process optimization"
    ]
    
    for feature in ai_features:
        st.markdown(f"✓ {feature}")
    
    # Roadmap for the future
    st.subheader("Product Roadmap & Vision")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Near-Term Focus (6-12 months)
        
        - Enhanced AI integration across the platform
        - Expanded analytics capabilities for deeper insights
        - New industry-specific templates and solutions
        - Improved no-code creator experience
        - Enhanced mobile capabilities
        """)
    
    with col2:
        st.markdown("""
        ### Long-Term Vision (1-3 years)
        
        - Comprehensive technology adoption platform
        - AI-driven predictive user assistance
        - Expanded enterprise software ecosystem
        - Cross-application workflow optimization
        - True autonomous user experience management
        """)
    
    # Market trends
    st.subheader("Market Trends Supporting Whatfix's Growth")
    
    trends = [
        {
            "title": "Digital Transformation Acceleration",
            "description": "Enterprise digital transformation initiatives continue to accelerate, creating greater need for effective adoption solutions."
        },
        {
            "title": "Skills Gap Widening",
            "description": "As technology evolves faster than training, organizations need solutions to bridge the growing digital skills gap."
        },
        {
            "title": "AI Revolution",
            "description": "The AI revolution is transforming enterprise software, creating both opportunities and challenges for user adoption."
        },
        {
            "title": "Remote Work Permanence",
            "description": "Permanent hybrid/remote work models require better digital enablement and self-service support."
        }
    ]
    
    trend_cols = st.columns(2)
    
    for i, trend in enumerate(trends):
        with trend_cols[i % 2]:
            st.markdown(f"""
            <div class="highlight-card">
                <h4>{trend["title"]}</h4>
                <p>{trend["description"]}</p>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.current_page == "Self Introduction":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px; padding: 10px; background-color: #f8f9fa; border-radius: 10px;">
        <h2 style="color: #31204a;">Kyung Yoon Lee</h2>
        <p style="color: #6c757d;">MBA Candidate at Yale School of Management</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["1-Minute Self Introduction", "Why I'm Perfect for Whatfix", "My Resume"])

    with tab1:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px;">
            <h3 style="color: #f47e35; text-align: center;">Professional Experience Keywords</h3>
            <div style="display: flex;">
                <div style="flex:1; margin-right: 10px;">
                    <h4>Business Strategy Associate</h4>
                    <ul>
                        <li>Consulting</li>
                        <li>Strategy</li>
                        <li>Salesforce Implementation</li>
                        <li>US Sales</li>
                    </ul>
                </div>
                <div style="flex:1;">
                    <h4>Product Manager</h4>
                    <ul>
                        <li>US/EU Sales</li>
                        <li>$350M Project Win</li>
                        <li>Empathy</li>
                    </ul>
                </div>
            </div>
            <h4>Human Perspective</h4>
            <ul>
                <li>Empowering Dreams of Others</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px;">
            <h3 style="color: #f47e35; text-align: center;">Why I'm a Perfect Match for Whatfix</h3>
            <ul>
                <li><strong>B2B Enterprise Client Management Experience:</strong> Led large-scale projects for Fortune 500 global clients at LG Display (e.g., $350M deal with an automotive OEM), aligning perfectly with Whatfix's enterprise-focused sales model.</li>
                <li><strong>Cross-functional Collaboration & Solution Selling:</strong> Worked closely with Engineering, Product, and Strategy teams to understand client needs and deliver customized solutions, matching Whatfix's collaborative sales approach.</li>
                <li><strong>Data-driven Strategic Thinking:</strong> Developed systems for demand forecasting and bid success rate prediction based on internal and external data analysis, directly supporting Whatfix's market research needs.</li>
                <li><strong>Global and Multicultural Business Experience:</strong> Worked with stakeholders across North America, Europe, and Asia, developing a strong global mindset and cross-cultural communication skills, perfect for Whatfix's international client base.</li>
                <li><strong>Empathy and Customer-First Mindset:</strong> Proactively relocated to a client's site to support an urgent project timeline, showcasing true customer obsession and dedication to delivering value that matches Whatfix's core values.</li>
                <li><strong>Learning Agility and Technical Curiosity:</strong> Transitioned from a business strategy background to a client-facing Product Manager role by quickly mastering technical concepts, demonstrating the learning agility needed for Whatfix's SaaS platform.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px;">
            <h3 style="color: #f47e35; text-align: center;">My Resume</h3>
            <p><strong>YALE SCHOOL OF MANAGEMENT</strong>, New Haven, CT</p>
            <p>Master of Business Administration (MBA), Management Science Concentration (STEM), 2025</p>
            <ul>
                <li>Leader of Yale Korean Business Club; active member of Data Analytics Club and Technology Club</li>
                <li>Recognized for academic excellence in behavioral science, fintech innovation, and team management</li>
            </ul>
            <p><strong>CHUNG-ANG UNIVERSITY</strong>, Seoul, Korea</p>
            <p>Bachelor of Business Administration (BBA), 2018</p>
            <ul>
                <li>Leader of volunteer tutoring organization for underprivileged youth and of university paragliding club</li>
                <li>Graduated with Honors, GPA 3.94/4.5; merit-based scholarship recipient</li>
            </ul>
            <p><strong>ANALYSIS GROUP</strong>, Boston, MA - Associate Consultant, 2024</p>
            <ul>
                <li>Developed competitive response strategies, conducted research, designed analytical models using SQL and R</li>
            </ul>
            <p><strong>LG DISPLAY</strong>, Seoul, Korea - Product Manager, 2019-2023</p>
            <ul>
                <li>Drove $60M profit increase by cost analysis</li>
                <li>Orchestrated cross-functional $350M contract securing</li>
                <li>Established strategic product roadmap and internal processes</li>
            </ul>
            <p>Business Strategy Associate Role</p>
            <ul>
                <li>Built demand forecasting models achieving 97% accuracy</li>
                <li>Created bid-winning probability models boosting success rates</li>
            </ul>
            <p><strong>Skills:</strong> Excel, Python, R, Public Speaking, Stakeholder Management</p>
            <p><strong>Interests:</strong> AI automation, snowboarding, party hosting, tropical travel</p>
            <p><strong>Military service:</strong> Operations Specialist, Republic of Korea Army (2012–2013)</p>
            <p><strong>Big Data Analytics Training:</strong> Seoul National University 6-month program</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p>© 2024 Whatfix. All rights reserved.</p>
    <p style="font-size: 0.8rem; color: #6c757d;">
        <a href="#" style="color: #f47e35; text-decoration: none; margin: 0 10px;">About</a> •
        <a href="#" style="color: #f47e35; text-decoration: none; margin: 0 10px;">Contact</a> •
        <a href="#" style="color: #f47e35; text-decoration: none; margin: 0 10px;">Privacy Policy</a> •
        <a href="#" style="color: #f47e35; text-decoration: none; margin: 0 10px;">Terms of Service</a>
    </p>
</div>
""", unsafe_allow_html=True)