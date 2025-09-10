import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Time Reservation Management System",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
:root {
    --primary-color: #4a90e2;
    --secondary-color: #2c3e50;
    --danger-color: #e74c3c;
    --success-color: #27ae60;
    --warning-color: #f39c12;
    --background-color: #f5f5f5;
}

.stApp {
    background-color: var(--background-color);
}

.metric-card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
    text-align: center;
}

.reservation-card {
    background-color: white;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid var(--primary-color);
    margin-bottom: 0.5rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.overlap-badge {
    background-color: var(--danger-color);
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: bold;
}

.available-badge {
    background-color: var(--success-color);
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 15px;
    font-size: 0.8rem;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 5px;
}

.legend-color {
    width: 20px;
    height: 20px;
    border-radius: 3px;
    border: 1px solid #ccc;
}

h1, h2, h3 {
    color: var(--secondary-color);
}
</style>
""", unsafe_allow_html=True)

# Original data
DEFAULT_DATA = [
    {'id': 1, 'time': '18:00'}, {'id': 2, 'time': '15:00'}, {'id': 3, 'time': '07:00'},
    {'id': 4, 'time': '12:00'}, {'id': 5, 'time': '12:00'}, {'id': 6, 'time': '17:00'},
    {'id': 7, 'time': '10:00'}, {'id': 8, 'time': '10:00'}, {'id': 9, 'time': '14:00'},
    {'id': 10, 'time': '12:00'}, {'id': 11, 'time': '10:30'}, {'id': 12, 'time': '15:00'},
    {'id': 13, 'time': '18:30'}, {'id': 14, 'time': '12:00'}, {'id': 15, 'time': '14:00'},
    {'id': 16, 'time': '08:00'}, {'id': 17, 'time': '07:00'}, {'id': 18, 'time': '15:00'},
    {'id': 19, 'time': '16:30'}, {'id': 20, 'time': '10:00'}, {'id': 21, 'time': '06:30'},
    {'id': 22, 'time': '14:31'}, {'id': 23, 'time': '09:50'}
]

def time_to_minutes(time_str):
    """Convert time string to minutes"""
    try:
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    except:
        return 0

def minutes_to_time(minutes):
    """Convert minutes to time string"""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"

def calculate_time_slots(data, start_hour=8, end_hour=18):
    """Calculate reservation status by time slots"""
    # Create 10-minute interval time slots
    time_slots = []
    for hour in range(start_hour, end_hour):
        for minute in range(0, 60, 10):
            slot_minutes = hour * 60 + minute
            time_slots.append({
                'time': minutes_to_time(slot_minutes),
                'minutes': slot_minutes,
                'count': 0,
                'reservations': []
            })
    
    # Calculate slot occupancy for each reservation
    for item in data:
        original_minutes = time_to_minutes(item['time'])
        start_minutes = original_minutes - 30
        end_minutes = original_minutes + 30
        
        for slot in time_slots:
            slot_minutes = slot['minutes']
            if start_minutes <= slot_minutes < end_minutes:
                slot['count'] += 1
                slot['reservations'].append(item['id'])
    
    return time_slots, data

def create_heatmap(time_slots, data):
    """Create heatmap chart"""
    # Prepare time-based data
    times = [slot['time'] for slot in time_slots]
    reservation_ids = [item['id'] for item in data]
    
    # Create 2D array (Reservation ID x Time)
    z_data = []
    y_labels = []
    
    for item in data:
        row = []
        original_minutes = time_to_minutes(item['time'])
        start_minutes = original_minutes - 30
        end_minutes = original_minutes + 30
        
        for slot in time_slots:
            slot_minutes = slot['minutes']
            if start_minutes <= slot_minutes < end_minutes:
                row.append(1)  # Reserved
            else:
                row.append(0)  # Available
        
        z_data.append(row)
        y_labels.append(f"ID {item['id']} ({item['time']})")
    
    # Add total row
    total_row = [slot['count'] for slot in time_slots]
    z_data.append(total_row)
    y_labels.append("Total")
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=times,
        y=y_labels,
        colorscale=[
            [0, 'white'],
            [0.5, '#ff6b6b'],
            [1, '#e74c3c']
        ],
        showscale=True,
        colorbar=dict(
            title="Reservations",
            tickmode="linear",
            tick0=0,
            dtick=1
        ),
        text=[[str(val) if val > 1 else '' for val in row] for row in z_data],
        texttemplate="%{text}",
        textfont={"size": 10, "color": "white"},
        hoverongaps=False,
        hovertemplate="<b>%{y}</b><br>Time: %{x}<br>Reservations: %{z}<extra></extra>"
    ))
    
    fig.update_layout(
        title="Time Reservation Status Chart (±30 minutes applied)",
        xaxis_title="Time",
        yaxis_title="Reservation ID",
        height=600,
        xaxis=dict(
            tickangle=45,
            tickmode='linear',
            dtick=6  # Display at 1-hour intervals
        ),
        margin=dict(l=100, r=50, t=50, b=100)
    )
    
    return fig

def create_overlap_chart(time_slots):
    """Overlap reservation distribution chart"""
    overlap_counts = {}
    for slot in time_slots:
        count = slot['count']
        if count > 0:
            overlap_counts[count] = overlap_counts.get(count, 0) + 1
    
    if overlap_counts:
        counts = list(overlap_counts.keys())
        frequencies = list(overlap_counts.values())
        
        fig = px.bar(
            x=counts,
            y=frequencies,
            labels={'x': 'Concurrent Reservations', 'y': 'Time Slot Count'},
            title='Concurrent Reservation Distribution',
            color=counts,
            color_continuous_scale='Reds'
        )
        
        fig.update_traces(
            text=frequencies,
            textposition='outside'
        )
        
        fig.update_layout(height=400)
        return fig
    
    return None

# Main application
def main():
    st.title("📅 Time Reservation Management System")
    st.markdown("**Visualizes reservation status with ±30 minute buffer time applied**")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Settings")
    
    # Operating hours configuration
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_hour = st.selectbox("Start Hour", range(0, 24), index=8)
    with col2:
        end_hour = st.selectbox("End Hour", range(1, 25), index=18)
    
    if start_hour >= end_hour:
        st.sidebar.error("End hour must be later than start hour.")
        return
    
    # Data input method selection
    data_input_method = st.sidebar.radio(
        "Data Input Method",
        ["Use Default Data", "Upload CSV File", "Manual Input"]
    )
    
    data = DEFAULT_DATA.copy()
    
    if data_input_method == "Upload CSV File":
        uploaded_file = st.sidebar.file_uploader("Select CSV file", type="csv")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if 'id' in df.columns and 'time' in df.columns:
                    data = df.to_dict('records')
                    st.sidebar.success(f"Loaded {len(data)} reservation records.")
                else:
                    st.sidebar.error("CSV file must contain 'id' and 'time' columns.")
            except Exception as e:
                st.sidebar.error(f"File reading error: {e}")
    
    elif data_input_method == "Manual Input":
        st.sidebar.subheader("Add Reservation")
        with st.sidebar.form("add_reservation"):
            new_id = st.number_input("Reservation ID", min_value=1, value=len(data)+1)
            new_time = st.time_input("Reservation Time")
            
            if st.form_submit_button("Add Reservation"):
                data.append({
                    'id': new_id,
                    'time': new_time.strftime("%H:%M")
                })
                st.sidebar.success("Reservation added.")
    
    # Data processing
    time_slots, reservation_data = calculate_time_slots(data, start_hour, end_hour)
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #4a90e2; margin: 0;">Total Reservations</h3>
            <h2 style="margin: 0;">{}</h2>
        </div>
        """.format(len(data)), unsafe_allow_html=True)
    
    with col2:
        max_overlap = max([slot['count'] for slot in time_slots]) if time_slots else 0
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #f39c12; margin: 0;">Max Overlap</h3>
            <h2 style="margin: 0;">{}</h2>
        </div>
        """.format(max_overlap), unsafe_allow_html=True)
    
    with col3:
        total_occupied_slots = sum(1 for slot in time_slots if slot['count'] > 0)
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #27ae60; margin: 0;">Occupied Time Slots</h3>
            <h2 style="margin: 0;">{}</h2>
        </div>
        """.format(total_occupied_slots), unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📊 Reservation Chart", "📈 Overlap Analysis", "📋 Reservation List"])
    
    with tab1:
        st.subheader("Reservation Status by Time Slot")
        
        # Legend
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;">
            <div class="legend-item">
                <div class="legend-color" style="background-color: white; border: 2px solid #ccc;"></div>
                <span>Available</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #ff6b6b;"></div>
                <span>Reserved</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #e74c3c;"></div>
                <span>Overlapping</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Heatmap chart
        if reservation_data:
            fig = create_heatmap(time_slots, reservation_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No reservations to display.")
    
    with tab2:
        st.subheader("Overlap Reservation Analysis")
        
        overlap_fig = create_overlap_chart(time_slots)
        if overlap_fig:
            st.plotly_chart(overlap_fig, use_container_width=True)
            
            # Display time slots with high overlap
            high_overlap_slots = [slot for slot in time_slots if slot['count'] >= 3]
            if high_overlap_slots:
                st.warning(f"⚠️ {len(high_overlap_slots)} time slots have 3 or more overlapping reservations.")
                
                for slot in high_overlap_slots[:5]:  # Display top 5 only
                    st.markdown(f"""
                    <div class="reservation-card">
                        <strong>{slot['time']}</strong>
                        <span class="overlap-badge">{slot['count']} Overlaps</span>
                        <br><small>Reservation IDs: {', '.join(map(str, slot['reservations']))}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No overlapping reservations.")
    
    with tab3:
        st.subheader("All Reservations")
        
        if reservation_data:
            for item in reservation_data:
                original_minutes = time_to_minutes(item['time'])
                start_time = minutes_to_time(original_minutes - 30)
                end_time = minutes_to_time(original_minutes + 30)
                
                st.markdown(f"""
                <div class="reservation-card">
                    <strong>Reservation #{item['id']}</strong>
                    <span class="available-badge">Active</span>
                    <br>
                    <small>Reservation Time: {item['time']}</small>
                    <br>
                    <small>Actual Occupancy: {start_time} ~ {end_time}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No reservations.")
    
    # Data download
    st.markdown("---")
    st.subheader("📥 Data Download")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Download Reservations (CSV)", type="primary"):
            df = pd.DataFrame(reservation_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV File",
                data=csv,
                file_name=f"reservations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Download Time Slot Analysis (CSV)"):
            slots_df = pd.DataFrame([
                {
                    'time': slot['time'],
                    'overlap_count': slot['count'],
                    'reservation_ids': ', '.join(map(str, slot['reservations'])) if slot['reservations'] else ''
                }
                for slot in time_slots if slot['count'] > 0
            ])
            csv = slots_df.to_csv(index=False)
            st.download_button(
                label="Download Analysis Results",
                data=csv,
                file_name=f"time_slot_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()