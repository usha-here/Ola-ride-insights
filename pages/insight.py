import streamlit as st

st.set_page_config(layout="wide")

st.title("Business Strategy & Operational Insights")
st.caption("Usha Nitwal")

st.markdown("---")

# =====================================================
# SECTION 1
# =====================================================

st.subheader("Peak Demand Optimization")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
Ride demand analysis indicates consistent time-based concentration patterns.
Identifying peak demand windows enables better driver allocation and supply balancing.

Peak demand typically aligns with:

- Office commute hours  
- Weekend evenings  
- High traffic or weather disruptions  
""")

with col2:
    st.info("""
Business Impact

• Reduced customer wait times  
• Higher ride completion rates  
• Improved driver utilization  
• Revenue optimization during peak hours  
""")

st.markdown("---")

# =====================================================
# SECTION 2
# =====================================================

st.subheader("Customer Behavior Intelligence")

col3, col4 = st.columns([2, 1])

with col3:
    st.markdown("""
Customer behavior analysis highlights variation in ride frequency,
vehicle preference, and payment methods.

Key segments identified:

- High-frequency riders  
- Premium vehicle users  
- Price-sensitive customers  
""")

with col4:
    st.success("""
Strategic Applications

• Personalized promotions  
• Loyalty programs  
• Targeted notifications  
• Retention-focused campaigns  
""")

st.markdown("---")

# =====================================================
# SECTION 3
# =====================================================

st.subheader("Dynamic Pricing Effectiveness")

col5, col6 = st.columns([2, 1])

with col5:
    st.markdown("""
Revenue trends suggest varying levels of customer sensitivity to pricing changes.
Dynamic pricing strategies must maintain a balance between revenue maximization
and booking conversion rates.

Tracking booking value alongside ride volume
helps evaluate pricing elasticity.
""")

with col6:
    st.warning("""
Optimization Objectives

• Increase revenue per ride  
• Maintain booking conversion rates  
• Avoid demand suppression  
• Improve pricing transparency  
""")

st.markdown("---")

# =====================================================
# SECTION 4
# =====================================================

st.subheader("Operational Risk Monitoring")

col7, col8 = st.columns([2, 1])

with col7:
    st.markdown("""
Irregular ride patterns may indicate operational inefficiencies
or potential risk exposure.

Key indicators include:

- Cancellation spikes  
- Abnormal ride distances  
- Clusters of low ratings  
""")

with col8:
    st.error("""
Risk Mitigation Measures

• Automated anomaly detection  
• Fraud monitoring systems  
• Driver and customer risk scoring  
• Real-time operational dashboards  
""")

st.markdown("---")

# =====================================================
# SECTION 5 – KEY BUSINESS ISSUES
# =====================================================

st.subheader("Key Business Issues Identified")

st.markdown("""
• High cancellation rate (primary operational risk)  
• Driver availability constraints  
• Heavy reliance on cash transactions  
• Revenue leakage from cancelled bookings  
""")

st.markdown("---")

# =====================================================
# SECTION 6 – STRATEGIC ACTION PLAN
# =====================================================

st.subheader("Strategic Action Plan")

st.table({
    "Priority": ["High", "High", "Medium", "Low"],
    "Action": [
        "Reduce driver cancellations",
        "Improve driver supply matching",
        "Increase UPI/Card adoption",
        "Introduce loyalty program for high-value customers"
    ],
    "Expected Impact": [
        "Immediate revenue improvement",
        "Reduction in 'Driver Not Found' cases",
        "Higher digital transaction penetration",
        "Improved customer retention"
    ]
})

st.markdown("---")

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.subheader("Executive Summary")

st.markdown("""
Overall ride demand and revenue performance remain stable. 
However, approximately 38% of rides are cancelled, representing 
the most significant operational and financial challenge.

High cancellation levels impact revenue realization,
customer experience, and platform efficiency.

Reducing cancellations and strengthening driver supply alignment
can materially increase revenue without increasing customer acquisition costs.

Primary strategic priorities:

• Improve ride completion rates  
• Optimize driver allocation  
• Accelerate digital payment adoption  
• Strengthen customer retention initiatives  

Focused execution in these areas will enhance operational efficiency,
improve customer satisfaction, and drive sustainable revenue growth.
""")