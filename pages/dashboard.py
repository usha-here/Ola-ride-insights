import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("dataset.xlsx")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔎 Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Date"].min(), df["Date"].max()]
)

vehicle_filter = st.sidebar.multiselect(
    "Vehicle Type",
    df["Vehicle_Type"].unique(),
    default=df["Vehicle_Type"].unique()
)
status_filter = st.sidebar.multiselect(
    "Booking Status",
    options=df["Booking_Status"].unique(),
    default=df["Booking_Status"].unique()
)
payment=st.sidebar.multiselect(
    "Payment Method",   
    options=df["Payment_Method"].unique(),
    default=df["Payment_Method"].unique()
)


filtered_df = df[
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1])) &
    (df["Vehicle_Type"].isin(vehicle_filter))&
        (df["Booking_Status"].isin(status_filter))&
        (df["Payment_Method"].isin(payment))

]

st.title("🚖 OLA Ride Analytics Dashboard")

# =============================
# KPI ROW
# =============================
total_rides = len(filtered_df)
successful_rides = len(filtered_df[filtered_df["Booking_Status"] == "Success"])
cancelled_rides = total_rides - successful_rides
revenue = filtered_df[filtered_df["Booking_Status"] == "Success"]["Booking_Value"].sum()
avg_rating = filtered_df["Driver_Ratings"].mean()

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Total Rides", f"{total_rides:,}")
k2.metric("Revenue", f"₹ {revenue:,.0f}")
k3.metric("Successful", f"{successful_rides:,}")
k4.metric("Cancelled", f"{cancelled_rides:,}")
k5.metric("Avg Driver Rating", f"{avg_rating:.2f}")

st.markdown("---")

# =============================
# ROW 1
# =============================
col1, col2 = st.columns(2)

with col1:
    ride_trend = filtered_df.groupby("Date").size().reset_index(name="Ride_Count")
    fig1 = px.line(ride_trend, x="Date", y="Ride_Count",
                   title="1️⃣ Ride Volume Over Time")
    fig1.update_layout(height=330)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(filtered_df, names="Booking_Status",
                  title="2️⃣ Booking Status Breakdown")
    fig2.update_layout(height=330)
    st.plotly_chart(fig2, use_container_width=True)

# =============================
# ROW 2
# =============================
col3, col4, col5 = st.columns(3)

with col3:
    vehicle_distance = (
        filtered_df.groupby("Vehicle_Type")["Ride_Distance"]
        .sum().sort_values(ascending=False).head(5).reset_index()
    )
    fig3 = px.bar(vehicle_distance, x="Vehicle_Type", y="Ride_Distance",
                  title="3️⃣ Top 5 Vehicle Types by Ride Distance")
    fig3.update_layout(height=300)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    avg_customer_rating = (
        filtered_df.groupby("Vehicle_Type")["Customer_Rating"]
        .mean().reset_index()
    )
    fig4 = px.bar(avg_customer_rating, x="Vehicle_Type", y="Customer_Rating",
                  title="4️⃣ Avg Customer Ratings by Vehicle")
    fig4.update_layout(height=300)
    st.plotly_chart(fig4, use_container_width=True)

with col5:

    # Extract driver cancellations (USE filtered_df)
    driver_cancel = filtered_df[["Canceled_Rides_by_Driver"]].dropna()
    driver_cancel = driver_cancel.rename(columns={"Canceled_Rides_by_Driver": "Reason"})
    driver_cancel["Cancellation_Type"] = "Driver"

    # Extract customer cancellations
    customer_cancel = filtered_df[["Canceled_Rides_by_Customer"]].dropna()
    customer_cancel = customer_cancel.rename(columns={"Canceled_Rides_by_Customer": "Reason"})
    customer_cancel["Cancellation_Type"] = "Customer"

    # Combine both
    cancel_data = pd.concat([driver_cancel, customer_cancel], ignore_index=True)

    # Group by type
    cancel_summary = (
        cancel_data.groupby("Cancellation_Type")
        .size()
        .reset_index(name="Count")
    )

    # Plot
    fig5 = px.bar(
        cancel_summary,
        x="Cancellation_Type",
        y="Count",
        title="5️⃣ Cancellation Distribution"
    )

    fig5.update_layout(height=300)
    st.plotly_chart(fig5, use_container_width=True)
# =============================
# ROW 3
# =============================
col6, col7, col8 = st.columns(3)

with col6:
    revenue_payment = (
        filtered_df[filtered_df["Booking_Status"] == "Success"]
        .groupby("Payment_Method")["Booking_Value"]
        .sum().reset_index()
    )
    fig6 = px.bar(revenue_payment, x="Payment_Method", y="Booking_Value",
                  title="6️⃣ Revenue by Payment Method")
    fig6.update_layout(height=300)
    st.plotly_chart(fig6, use_container_width=True)

with col7:
    top_customers = (
        filtered_df.groupby("Customer_ID")["Booking_Value"]
        .sum().sort_values(ascending=False).head(5).reset_index()
    )
    fig7 = px.bar(top_customers, x="Customer_ID", y="Booking_Value",
                  title="7️⃣ Top 5 Customers")
    fig7.update_layout(height=300)
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    distance_day = (
        filtered_df.groupby("Date")["Ride_Distance"]
        .sum().reset_index()
    )
    fig8 = px.line(distance_day, x="Date", y="Ride_Distance",
                   title="8️⃣ Ride Distance Per Day")
    fig8.update_layout(height=300)
    st.plotly_chart(fig8, use_container_width=True)

# =============================
# ROW 4
# =============================
col9, col10 = st.columns(2)

with col9:
    fig9 = px.histogram(filtered_df, x="Driver_Ratings",
                        title="9️⃣ Driver Ratings Distribution")
    fig9.update_layout(height=300)
    st.plotly_chart(fig9, use_container_width=True)

with col10:
    fig10 = px.scatter(filtered_df,
                       x="Customer_Rating",
                       y="Driver_Ratings",
                       title="🔟 Customer vs Driver Ratings")
    fig10.update_layout(height=300)
    st.plotly_chart(fig10, use_container_width=True)