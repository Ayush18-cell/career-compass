import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import numpy as np

# Job Portals & Companies Mapping
JOB_PORTALS = {
    "linkedin": {
        "name": "LinkedIn Jobs",
        "url": "https://www.linkedin.com/jobs",
        "icon": "🔗"
    },
    "indeed": {
        "name": "Indeed",
        "url": "https://www.indeed.com",
        "icon": "🔍"
    },
    "naukri": {
        "name": "Naukri",
        "url": "https://www.naukri.com",
        "icon": "💼"
    },
    "glassdoor": {
        "name": "Glassdoor",
        "url": "https://www.glassdoor.com",
        "icon": "⭐"
    },
    "monster": {
        "name": "Monster",
        "url": "https://www.monster.com",
        "icon": "👾"
    },
    "angel": {
        "name": "AngelList",
        "url": "https://angel.co/jobs",
        "icon": "😇"
    }
}

# Role to Company Mapping
ROLE_TO_COMPANIES = {
    "Software Engineer": ["Google", "Microsoft", "Amazon", "Apple", "Meta", "Tesla"],
    "Data Scientist": ["DataCamp", "Kaggle", "IBM", "McKinsey", "Deloitte"],
    "Data Analyst": ["Tableau", "Power BI", "Deloitte", "Ernst & Young", "PwC"],
    "Product Manager": ["Google", "Microsoft", "Amazon", "Apple", "Atlassian"],
    "DevOps Engineer": ["Google Cloud", "AWS", "DigitalOcean", "Heroku"],
    "ML Engineer": ["OpenAI", "DeepMind", "Tesla", "Nvidia", "Google AI"],
    "Project Manager": ["Accenture", "Deloitte", "TCS", "Infosys", "Wipro"],
    "Finance Manager": ["Goldman Sachs", "Morgan Stanley", "Citigroup", "ICICI Bank"],
    "Business Analyst": ["Accenture", "Capgemini", "Cognizant", "HCL Technologies"],
    "QA Engineer": ["Infosys", "TCS", "Wipro", "HCL", "Cognizant"],
    "Cloud Architect": ["AWS", "Azure", "Google Cloud", "Terraform", "Kubernetes"],
    "Agile Coach": ["ThoughtWorks", "Atlassian", "Scrum Alliance", "Scaled Agile"],
    "Operations Manager": ["Amazon", "DHL", "UPS", "Flipkart", "Amazon"],
    "Strategy Consultant": ["McKinsey", "BCG", "Bain & Company", "Deloitte", "EY"],
}

# Page config
st.set_page_config(
    page_title="🧭 CareerCompass",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_role_data():
    df = pd.read_csv('data/cleaned_jobs.csv')
    return df

@st.cache_data
def get_skill_stats(df):
    """Get overall skill statistics"""
    all_skills = []
    for skills_str in df['skills']:
        all_skills.extend([s.strip() for s in skills_str.split(",")])
    return Counter(all_skills)

@st.cache_data
def get_certification_stats(df):
    """Get overall certification statistics"""
    all_certs = []
    for cert_str in df[df['certifications'].str.len() > 0]['certifications']:
        all_certs.extend([c.strip() for c in cert_str.split(",")])
    return Counter(all_certs)

# Initialize session state
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None
if 'selected_exp' not in st.session_state:
    st.session_state.selected_exp = "All"

df = load_role_data()
unique_roles = sorted(df['title'].unique().tolist())

# Header
st.markdown("# 🧭 Career Compass")
st.markdown("**Explore career paths, salary ranges, required skills, and certifications**")
st.divider()

# Sidebar navigation
with st.sidebar:
    st.markdown("### 📊 Navigation")
    page = st.radio(
        "Select a section:",
        ["🔍 Role Lookup", "📈 Market Analysis", "🎓 Certification Guide", "💡 Career Insights"],
        label_visibility="collapsed"
    )

# ============================================================================
# PAGE 1: Role Lookup
# ============================================================================
if page == "🔍 Role Lookup":
    st.markdown("### Lookup Skills & Salary for Your Target Role")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        selected_role = st.selectbox(
            "🏢 Select Job Role:",
            unique_roles,
            placeholder="Choose a role...",
            key="role_select"
        )
    
    with col2:
        selected_exp = st.selectbox(
            "📅 Experience Level:",
            ["All"] + sorted(df['experience'].unique().tolist()),
            placeholder="All levels",
            key="exp_select"
        )
    
    with col3:
        search_btn = st.button("🔎 Search", use_container_width=True, type="primary")
    
    if search_btn or selected_role:
        if selected_role:
            # Filter data
            role_data = df[df['title'] == selected_role]
            if selected_exp != "All":
                role_data = role_data[role_data['experience'] == selected_exp]
            
            if not role_data.empty:
                # Calculate metrics
                avg_salary = role_data['salary_lpa'].mean()
                min_salary = role_data['salary_lpa'].min()
                max_salary = role_data['salary_lpa'].max()
                median_salary = role_data['salary_lpa'].median()
                total_records = len(role_data)
                
                # Extract skills
                all_skills = []
                for skills_str in role_data['skills']:
                    all_skills.extend([s.strip() for s in skills_str.split(",")])
                skill_counts = Counter(all_skills)
                top_skills = [skill for skill, count in skill_counts.most_common(8)]
                
                # Extract certifications
                certs = role_data[role_data['certifications'].str.len() > 0]['certifications'].unique()
                
                # Display role header
                st.success(f"### {selected_role}")
                
                # Salary metrics
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("💰 Average", f"₹{avg_salary:.2f}L", f"Median: ₹{median_salary:.2f}L")
                with col2:
                    st.metric("📊 Min Salary", f"₹{min_salary:.2f}L")
                with col3:
                    st.metric("📈 Max Salary", f"₹{max_salary:.2f}L")
                with col4:
                    salary_range = max_salary - min_salary
                    st.metric("📉 Range", f"₹{salary_range:.2f}L")
                with col5:
                    st.metric("📋 Records", total_records)
                
                st.divider()
                
                # Skills & Certifications
                col_skills, col_certs = st.columns(2)
                
                with col_skills:
                    st.subheader("🛠️ Required Skills")
                    skills_df = pd.DataFrame([
                        {"Skill": skill, "Frequency": skill_counts[skill]} 
                        for skill in top_skills
                    ])
                    
                    # Skill bar chart
                    fig_skills = px.bar(
                        skills_df,
                        x="Frequency",
                        y="Skill",
                        orientation="h",
                        color="Frequency",
                        color_continuous_scale="Blues",
                        title="Top Skills Required"
                    )
                    fig_skills.update_layout(height=300, showlegend=False)
                    st.plotly_chart(fig_skills, use_container_width=True)
                
                with col_certs:
                    st.subheader("🎓 Recommended Certifications")
                    if len(certs) > 0:
                        cert_list = list(certs)[:8]
                        st.info(f"**Certifications:**\n\n" + "\n".join([f"✅ {c}" for c in cert_list]))
                    else:
                        st.info("No specific certifications found for this role")
                
                st.divider()
                
                # Job Portals & Hiring Companies
                st.subheader("🎯 Where to Apply - Job Portals & Hiring Companies")
                
                job_col1, job_col2 = st.columns(2)
                
                with job_col1:
                    st.markdown("#### 🌐 Popular Job Portals")
                    for portal_key, portal_info in JOB_PORTALS.items():
                        st.markdown(
                            f"[{portal_info['icon']} {portal_info['name']}]({portal_info['url']})",
                            unsafe_allow_html=False
                        )
                
                with job_col2:
                    st.markdown("#### 🏢 Companies Hiring for This Role")
                    companies = ROLE_TO_COMPANIES.get(selected_role, ["Glassdoor", "LinkedIn", "Indeed"])
                    companies_text = ", ".join(companies[:6])
                    st.success(f"**{companies_text}** and many more!")
                    
                    # Direct search links for job portals
                    st.markdown("#### 🔎 Quick Search Links")
                    col_search1, col_search2, col_search3 = st.columns(3)
                    
                    with col_search1:
                        linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={selected_role.replace(' ', '%20')}"
                        st.markdown(f"[🔗 LinkedIn Jobs]({linkedin_url})")
                    
                    with col_search2:
                        indeed_url = f"https://www.indeed.com/jobs?q={selected_role.replace(' ', '+')}"
                        st.markdown(f"[🔍 Indeed Jobs]({indeed_url})")
                    
                    with col_search3:
                        naukri_url = f"https://www.naukri.com/jobs-{selected_role.replace(' ', '-').lower()}"
                        st.markdown(f"[💼 Naukri Jobs]({naukri_url})")
                
                st.divider()
                st.subheader("💼 Salary Distribution by Experience")
                exp_salary = role_data.groupby('experience')['salary_lpa'].agg(['mean', 'count']).reset_index()
                exp_salary = exp_salary[exp_salary['count'] > 0].sort_values('mean')
                
                fig_exp = px.bar(
                    exp_salary,
                    x='experience',
                    y='mean',
                    title="Average Salary by Experience Level",
                    labels={'experience': 'Experience Level', 'mean': 'Average Salary (LPA)'},
                    color='mean',
                    color_continuous_scale="Greens"
                )
                st.plotly_chart(fig_exp, use_container_width=True)
                
                st.divider()
                
                # Sample records table
                st.subheader("📋 Sample Job Records")
                display_cols = ['title', 'experience', 'salary_lpa', 'skills', 'certifications']
                st.dataframe(
                    role_data[display_cols].head(10),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.error("❌ No data found for this role and experience level")
        else:
            st.warning("⚠️ Please select a role to view details")

# ============================================================================
# PAGE 2: Market Analysis
# ============================================================================
elif page == "📈 Market Analysis":
    st.markdown("### Market Insights & Salary Trends")
    
    # Top paying roles
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Top Paying Roles")
        top_roles = df.groupby('title')['salary_lpa'].mean().sort_values(ascending=False).head(10)
        fig_top = px.bar(
            x=top_roles.values,
            y=top_roles.index,
            orientation='h',
            title="Top 10 Highest Paying Roles",
            labels={'x': 'Average Salary (LPA)', 'y': 'Job Role'},
            color=top_roles.values,
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        st.subheader("📊 Most In-Demand Skills")
        skill_stats = get_skill_stats(df)
        top_skills_market = skill_stats.most_common(10)
        skills_df = pd.DataFrame(top_skills_market, columns=['Skill', 'Demand'])
        
        fig_skills_market = px.bar(
            skills_df,
            x='Demand',
            y='Skill',
            orientation='h',
            title="Top 10 In-Demand Skills",
            color='Demand',
            color_continuous_scale="Purples"
        )
        st.plotly_chart(fig_skills_market, use_container_width=True)
    
    st.divider()
    
    # Salary distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📉 Overall Salary Distribution")
        fig_dist = px.histogram(
            df,
            x='salary_lpa',
            nbins=30,
            title="Salary Distribution Across All Roles",
            labels={'salary_lpa': 'Salary (LPA)', 'count': 'Number of Jobs'},
            color_discrete_sequence=['#636EFA']
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        st.subheader("📊 Experience vs Salary")
        exp_order = ["0-1 year", "1-3 years", "2-5 years", "3-7 years", "5+ years"]
        exp_salary = df.groupby('experience')['salary_lpa'].apply(list).reindex(exp_order)
        
        fig_box = go.Figure()
        for exp_level in exp_order:
            if exp_level in df['experience'].unique():
                data = df[df['experience'] == exp_level]['salary_lpa'].values
                fig_box.add_trace(go.Box(y=data, name=exp_level))
        
        fig_box.update_layout(
            title="Salary Range by Experience Level",
            yaxis_title="Salary (LPA)",
            xaxis_title="Experience",
            height=400
        )
        st.plotly_chart(fig_box, use_container_width=True)

# ============================================================================
# PAGE 3: Certification Guide
# ============================================================================
elif page == "🎓 Certification Guide":
    st.markdown("### Certification & Professional Development Guide")
    
    st.subheader("🏆 Most Recommended Certifications")
    cert_stats = get_certification_stats(df)
    top_certs = cert_stats.most_common(15)
    certs_df = pd.DataFrame(top_certs, columns=['Certification', 'Frequency'])
    
    fig_certs = px.bar(
        certs_df,
        x='Frequency',
        y='Certification',
        orientation='h',
        title="Top 15 Certifications Across All Roles",
        color='Frequency',
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_certs, use_container_width=True)
    
    st.divider()
    
    # Certification by role
    st.subheader("📋 Certifications by Role")
    role_selection = st.selectbox("Select a role to view certifications:", unique_roles)
    
    role_certs = df[df['title'] == role_selection]
    role_certs_list = role_certs[role_certs['certifications'].str.len() > 0]['certifications'].unique()
    
    if len(role_certs_list) > 0:
        st.info(f"**Recommended certifications for {role_selection}:**\n\n" + 
                "\n".join([f"✅ {cert}" for cert in role_certs_list]))
    else:
        st.info(f"No specific certifications found for {role_selection}")

# ============================================================================
# PAGE 4: Career Insights
# ============================================================================
elif page == "💡 Career Insights":
    st.markdown("### Career Path Recommendations & Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Skill Growth Potential")
        skill_stats = get_skill_stats(df)
        high_demand_skills = [skill for skill, count in skill_stats.most_common(15)]
        
        st.info(f"**High-Demand Skills (Top 15):**\n\n" + 
                ", ".join(high_demand_skills))
    
    with col2:
        st.subheader("💼 Role Categories")
        role_categories = {
            "Technical": ["Data Analyst", "Data Scientist", "Backend Developer", "Frontend Developer", 
                         "Full Stack Developer", "Data Engineer", "Cloud Engineer", "DevOps Engineer", 
                         "Machine Learning Engineer"],
            "Management": ["Project Manager", "Product Manager", "Business Manager", "Operations Manager", 
                         "Scrum Master", "Agile Coach"],
            "Consulting": ["Strategy Consultant", "Management Consultant", "Business Analyst", 
                          "Analytics Consultant"],
            "Finance": ["Finance Manager", "Business Analyst Manager"]
        }
        
        for category, roles in role_categories.items():
            avg_sal = df[df['title'].isin(roles)]['salary_lpa'].mean()
            count = len(df[df['title'].isin(roles)])
            st.metric(f"📌 {category}", f"₹{avg_sal:.2f}L ({count} jobs)")
    
    st.divider()
    
    # Career progression
    st.subheader("📈 Career Progression Path")
    career_paths = {
        "Data Analyst → Data Scientist → ML Engineer": 
            ["Data Analyst", "Data Scientist", "Machine Learning Engineer"],
        "Junior Developer → Senior Engineer → Tech Lead": 
            ["Junior Developer", "Senior Engineer", "Technical Lead"],
        "Business Analyst → Product Manager → Director": 
            ["Business Analyst", "Product Manager"],
        "Scrum Master → Agile Coach → Program Manager": 
            ["Scrum Master", "Agile Coach", "Program Manager"]
    }
    
    for path, roles_in_path in career_paths.items():
        with st.expander(f"📍 {path}", expanded=False):
            salaries = []
            for role in roles_in_path:
                role_salary = df[df['title'] == role]['salary_lpa'].mean()
                salaries.append(role_salary)
            
            path_df = pd.DataFrame({
                'Role': roles_in_path,
                'Average Salary (LPA)': salaries
            })
            
            fig_path = px.line(
                path_df,
                x='Role',
                y='Average Salary (LPA)',
                markers=True,
                title=f"Salary Progression: {path}"
            )
            fig_path.update_traces(marker=dict(size=12))
            st.plotly_chart(fig_path, use_container_width=True)
    
    st.divider()
    
    # Salary insights
    st.subheader("💰 Salary Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        overall_avg = df['salary_lpa'].mean()
        st.metric("📊 Overall Average Salary", f"₹{overall_avg:.2f}L")
    
    with col2:
        tech_avg = df[df['title'].str.contains('Developer|Engineer|Data|Cloud', regex=True)]['salary_lpa'].mean()
        st.metric("💻 Tech Roles Average", f"₹{tech_avg:.2f}L")
    
    with col3:
        mgmt_avg = df[df['title'].str.contains('Manager|Consultant|Product', regex=True)]['salary_lpa'].mean()
        st.metric("📈 Mgmt Roles Average", f"₹{mgmt_avg:.2f}L")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center'>
    <p>📊 AI Skill Gap & Salary Predictor | Built with Streamlit & ML | 700+ Job Records</p>
    <p>Updated: January 2026 | Total Roles: 30 | Skills Tracked: 40+</p>
    </div>
    """, unsafe_allow_html=True)
