import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(page_title="OLA Ride Dashboard", layout="wide")

# ----------------------------------------------------
# 🎨 CUSTOM STYLING (POWER BI LOOK)
# ----------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.main-title {
    background: linear-gradient(90deg, #1f77b4, #00c6ff);
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-size: 38px;
    font-weight: bold;
    margin-bottom: 25px;
}

.kpi-card {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

.kpi-title {
    font-size: 16px;
    color: #9CA3AF;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 32px;
    font-weight: bold;
    color: #00C6FF;
}

.section-title {
    font-size: 22px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 🌈 COLORED HEADER
# ----------------------------------------------------
st.markdown('<div class="main-title">🚖 OLA Ride-Sharing Analytics Dashboard</div>', unsafe_allow_html=True)

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("dataset.xlsx", engine="openpyxl")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ----------------------------------------------------
# CREATE SQLITE DATABASE
# ----------------------------------------------------
@st.cache_resource
def create_connection(df):
    conn = sqlite3.connect("ola.db", check_same_thread=False)
    df.to_sql("bookings", conn, index=False, if_exists="replace")
    return conn

conn = create_connection(df)

# ----------------------------------------------------
# 🔥 KPI CALCULATIONS
# ----------------------------------------------------
total_rides = len(df)
successful_rides = len(df[df["Booking_Status"] == "Success"])
cancelled_rides = len(df[df["Booking_Status"] != "Success"])
total_revenue = df[df["Booking_Status"] == "Success"]["Booking_Value"].sum()

# ----------------------------------------------------
# 📊 KPI CARDS
# ----------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Rides</div>
        <div class="kpi-value">{total_rides:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Successful Rides</div>
        <div class="kpi-value">{successful_rides:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Cancelled Rides</div>
        <div class="kpi-value">{cancelled_rides:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Revenue</div>
        <div class="kpi-value">₹ {total_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------
# SIDEBAR QUERY SELECT
# ----------------------------------------------------
st.sidebar.header("📌 Select SQL Query")

query_option = st.sidebar.selectbox(
    "Choose Query",
    [
        "Retrieve all successful bookings",
        "Find the average ride distance for each vehicle type",
        "Total Cancelled Rides by Customers",
        "Top 5 Customers",
        "Driver Cancellations due to Personal and Car Issues",
        "Maximum and Minimum Driver Ratings for Prime Sedan Bookings",
        "Rides Paid Using UPI",
        "Average Customer Rating per Vehicle Type",
        "Total Booking Value of Successfully Completed Rides",
        "Incomplete Rides with Cancellation Reason"
    ]
)

# ----------------------------------------------------
# SQL QUERIES
# ----------------------------------------------------
queries = {

    "Retrieve all successful bookings": """
        SELECT * FROM bookings
        WHERE Booking_Status = 'Success'
    """,

    "Find the average ride distance for each vehicle type": """
        SELECT Vehicle_Type,
               AVG(Ride_Distance) AS Avg_Distance
        FROM bookings
        GROUP BY Vehicle_Type
    """,

    "Total Cancelled Rides by Customers": """
        SELECT COUNT(*) AS Total_Cancelled_By_Customer
        FROM bookings
        WHERE Booking_Status = 'Canceled by Customer'
    """,

    "Top 5 Customers": """
        SELECT Customer_ID,
               COUNT(*) AS Total_Rides
        FROM bookings
        GROUP BY Customer_ID
        ORDER BY Total_Rides DESC
        LIMIT 5
    """,

    "Driver Cancellations due to Personal and Car Issues": """
        SELECT COUNT(*) AS Canceled_Rides_by_Driver
        FROM bookings
        WHERE Booking_Status = 'Canceled by Driver'
        AND (Canceled_Rides_by_Driver LIKE '%Personal%'
             OR Canceled_Rides_by_Driver LIKE '%Car%')
    """,

    "Maximum and Minimum Driver Ratings for Prime Sedan Bookings": """
        SELECT MAX(Driver_Ratings) AS Max_Rating,
               MIN(Driver_Ratings) AS Min_Rating
        FROM bookings
        WHERE Vehicle_Type = 'Prime Sedan'
    """,

    "Rides Paid Using UPI": """
        SELECT * FROM bookings
        WHERE Payment_Method = 'UPI'
    """,

    "Average Customer Rating per Vehicle Type": """
        SELECT Vehicle_Type,
               AVG(Customer_Rating) AS Avg_Customer_Rating
        FROM bookings
        GROUP BY Vehicle_Type
    """,

    "Total Booking Value of Successfully Completed Rides": """
        SELECT SUM(Booking_Value) AS Total_Revenue
        FROM bookings
        WHERE Booking_Status = 'Success'
    """,

    "Incomplete Rides with Cancellation Reason": """
    SELECT 
        Booking_ID,
        Booking_Status,
        COALESCE(Canceled_Rides_by_Customer, Canceled_Rides_by_Driver) AS Cancellation_Reason
    FROM bookings
    WHERE Booking_Status != 'Success'
"""
}

selected_query = queries[query_option]
result = pd.read_sql_query(selected_query, conn)

# ----------------------------------------------------
# DATA + VISUAL SECTION
# ----------------------------------------------------
st.markdown('<div class="section-title">📊 Data & Insights</div>', unsafe_allow_html=True)

col_table, col_chart = st.columns([1, 2])

with col_table:
    st.dataframe(result, use_container_width=True)

with col_chart:

    # Set dark theme for all charts
    template_style = "plotly_dark"

    if query_option == "Retrieve all successful bookings":
        fig = px.pie(df, names="Booking_Status", hole=0.6)
        fig.update_layout(template=template_style)
        st.plotly_chart(fig, use_container_width=True)

    elif query_option == "Find the average ride distance for each vehicle type":
        fig = px.bar(result, x="Avg_Distance", y="Vehicle_Type",
                     orientation="h", color="Avg_Distance")
        fig.update_layout(template=template_style)
        st.plotly_chart(fig, use_container_width=True)

    elif query_option == "Total Cancelled Rides by Customers":
        fig = go.Figure(go.Indicator(mode="number",
                                     value=result.iloc[0, 0],
                                     title={"text": "Cancelled by Customers"}))
        fig.update_layout(template=template_style)
        st.plotly_chart(fig, use_container_width=True)

    elif query_option == "Top 5 Customers":
        fig = px.bar(result, x="Total_Rides", y="Customer_ID",
                     orientation="h", color="Total_Rides")
        fig.update_layout(template=template_style)
        st.plotly_chart(fig, use_container_width=True)

    elif query_option == "Driver Cancellations due to Personal and Car Issues":
        fig = go.Figure(go.Indicator(mode="number",
                                     value=result.iloc[0, 0],
                                     title={"text": "Driver Cancellations due to Personal/Car Issues"}))
        fig.update_layout(template=template_style)
        st.plotly_chart(fig, use_container_width=True)

    elif query_option == "Maximum and Minimum Driver Ratings for Prime Sedan Bookings":
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Max", x=["Prime Sedan"], y=[result["Max_Rating"][0]]))
        fig.add_trace(go.Bar(name="Min", x=["Prime Sedan"], y=[result["Min_Rating"][0]]))
        fig.update_layout(template=template_style, barmode='group')
        st.plotly_chart(fig, use_container_width=True)

    elif query_option == "Rides Paid Using UPI":
        payment_counts = df["Payment_Method"].value_counts().reset_index()
        payment_counts.columns = ["Payment_Method", "Count"]
        fig = px.pie(payment_counts, names="Payment_Method", values="Count", hole=0.5)
        fig.update_layout(template=template_style)
        st.plotly_chart(fig, use_container_width=True)

    elif query_option == "Average Customer Rating per Vehicle Type":
        fig = px.bar(result, x="Vehicle_Type",
                     y="Avg_Customer_Rating",
                     color="Avg_Customer_Rating")
        fig.update_layout(template=template_style)
        st.plotly_chart(fig, use_container_width=True)

    elif query_option == "Total Booking Value of Successfully Completed Rides":
        fig = go.Figure(go.Indicator(mode="number",
                                     value=result.iloc[0, 0],
                                     number={'prefix': "₹ "},
                                     title={"text": "Total Revenue"}))
        fig.update_layout(template=template_style)
        st.plotly_chart(fig, use_container_width=True)

    elif query_option == "Incomplete Rides with Cancellation Reason":
        fig = px.histogram(result, x="Cancellation_Reason", color="Booking_Status")
        fig.update_layout(template=template_style)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("📍 Built with SQL + Streamlit | Power BI Style Dashboard")