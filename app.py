import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import random

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

.location-badge {
    background-color: var(--primary-color);
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 15px;
    font-size: 0.8rem;
    margin-right: 0.5rem;
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

# Updated sample data with location, id, time structure
def generate_sample_data():
    locations = ["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"]
    sample_times = [
        "18:00", "15:00", "07:00", "12:00", "12:00", "17:00", "10:00", "10:00", 
        "14:00", "12:00", "10:30", "15:00", "18:30", "12:00", "14:00", "08:00",
        "07:00", "15:00", "16:30", "10:00", "06:30", "14:31", "09:50", "21:30",
        "21:00", "22:00", "20:30", "19:00", "16:00", "11:00", "13:30", "09:00",
        "20:00", "22:30", "11:30", "13:00", "16:45", "08:30", "19:30", "17:45"
    ]
    
    data = []
    for i in range(40):  # Generate 40 sample records
        data.append({
            'location': random.choice(locations),
            'id': int(4.2e8 + random.randint(0, int(2e9))),  # Similar to your ID range
            'time': sample_times[i % len(sample_times)]
        })
    
    return data

DEFAULT_DATA = generate_sample_data()

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

def sort_reservations_by_time(data):
    """Sort reservations by time"""
    return sorted(data, key=lambda x: time_to_minutes(x['time']))

def calculate_time_slots(data, start_hour=8, end_hour=18, selected_location=None):
    """Calculate reservation status by time slots"""
    # Filter by location if selected
    if selected_location and selected_location != "All Locations":
        data = [item for item in data if item['location'] == selected_location]
    
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
    
    # Filter reservations that have any overlap with the time range
    start_minutes = start_hour * 60
    end_minutes = end_hour * 60
    
    filtered_data = []
    for item in data:
        reservation_minutes = time_to_minutes(item['time'])
        reservation_start = reservation_minutes - 30  # 30분 전부터
        reservation_end = reservation_minutes + 30    # 30분 후까지
        
        # 예약 시간대가 설정된 시간 범위와 겹치는지 확인
        if reservation_end > start_minutes and reservation_start < end_minutes:
            filtered_data.append(item)
    
    # Calculate slot occupancy for filtered reservations
    for item in filtered_data:
        original_minutes = time_to_minutes(item['time'])
        start_minutes_res = original_minutes - 30
        end_minutes_res = original_minutes + 30
        
        for slot in time_slots:
            slot_minutes = slot['minutes']
            if start_minutes_res <= slot_minutes < end_minutes_res:
                slot['count'] += 1
                slot['reservations'].append({
                    'id': item['id'],
                    'location': item['location'],
                    'time': item['time']
                })
    
    return time_slots, filtered_data

def calculate_max_overlap_per_location(data, start_hour=8, end_hour=18):
    """Calculate maximum overlap for each location separately"""
    # Group data by location
    location_groups = {}
    for item in data:
        location = item['location']
        if location not in location_groups:
            location_groups[location] = []
        location_groups[location].append(item)
    
    max_overlaps = {}
    
    # Calculate max overlap for each location
    for location, location_data in location_groups.items():
        # Create time slots for this location only
        time_slots, _ = calculate_time_slots(location_data, start_hour, end_hour)
        
        # Find maximum overlap for this location
        max_overlap = max([slot['count'] for slot in time_slots]) if time_slots else 0
        max_overlaps[location] = max_overlap
    
    # Return the overall maximum across all locations
    return max(max_overlaps.values()) if max_overlaps else 0

def create_heatmap(time_slots, data, selected_location=None):
    """Create heatmap chart grouped by location with expandable details"""
    # Prepare time-based data
    times = [slot['time'] for slot in time_slots]
    
    # Group data by location
    location_groups = {}
    for item in data:
        location = item['location']
        if location not in location_groups:
            location_groups[location] = []
        location_groups[location].append(item)
    
    # Sort locations by number of reservations (descending)
    sorted_locations = sorted(location_groups.keys(), 
                            key=lambda loc: len(location_groups[loc]), 
                            reverse=True)
    
    # Create summary heatmap (only totals)
    z_data_summary = []
    y_labels_summary = []
    
    # Process each location - only totals
    for location in sorted_locations:
        location_items = location_groups[location]
        
        # Calculate location total row
        location_total_row = [0] * len(time_slots)
        for item in location_items:
            original_minutes = time_to_minutes(item['time'])
            start_minutes = original_minutes - 30
            end_minutes = original_minutes + 30
            
            for i, slot in enumerate(time_slots):
                slot_minutes = slot['minutes']
                if start_minutes <= slot_minutes < end_minutes:
                    location_total_row[i] += 1
        
        # Add location total row
        z_data_summary.append(location_total_row)
        y_labels_summary.append(f"🏢 {location} ({len(location_items)} reservations)")
    
    # Create summary heatmap (reverse y-axis order to show highest count first)
    fig_summary = go.Figure(data=go.Heatmap(
        z=z_data_summary,
        x=times,
        y=y_labels_summary,
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
        text=[[str(val) if val > 0 else '' for val in row] for row in z_data_summary],
        texttemplate="%{text}",
        textfont={"size": 12, "color": "white"},
        hoverongaps=False,
        hovertemplate="<b>%{y}</b><br>Time: %{x}<br>Reservations: %{z}<extra></extra>"
    ))
    
    # Add vertical dotted lines at 30-minute intervals
    for i in range(0, len(times), 3):  # Every 3rd time slot (30 minutes)
        x_pos = i
        
        # Add vertical line using shape
        fig_summary.add_shape(
            type="line",
            x0=x_pos,
            x1=x_pos,
            y0=-0.5,
            y1=len(y_labels_summary) - 0.5,
            line=dict(color="rgba(128,128,128,0.3)", width=0.5, dash="dash"),
            xref="x",
            yref="y"
        )
    
    title = f"Time Reservation Summary by Location (±30 minutes applied)"
    if selected_location and selected_location != "All Locations":
        title += f" - {selected_location}"
    
    fig_summary.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Locations",
        height=max(400, len(sorted_locations) * 50 + 100),
        xaxis=dict(
            tickangle=45,
            tickmode='linear',
            dtick=3  # Display at 30-minute intervals
        ),
        yaxis=dict(
            tickfont=dict(size=11),
            autorange='reversed'  # Reverse y-axis to show highest count at top
        ),
        margin=dict(l=250, r=50, t=50, b=100),
        showlegend=False
    )
    
    # Return sorted location groups to maintain order
    sorted_location_groups = {loc: location_groups[loc] for loc in sorted_locations}
    
    return fig_summary, sorted_location_groups

def create_location_detail_heatmap(location, location_items, time_slots):
    """Create detailed heatmap for a specific location"""
    # Prepare time-based data
    times = [slot['time'] for slot in time_slots]
    
    # Sort items by time within location (earliest first)
    location_items_sorted = sort_reservations_by_time(location_items)
    
    # Create detailed heatmap data - TOTAL FIRST, then reversed individual items
    z_data_detail = []
    y_labels_detail = []
    
    # Calculate location total row (same as summary)
    location_total_row = [0] * len(time_slots)
    for item in location_items:
        original_minutes = time_to_minutes(item['time'])
        start_minutes = original_minutes - 30
        end_minutes = original_minutes + 30
        
        for i, slot in enumerate(time_slots):
            slot_minutes = slot['minutes']
            if start_minutes <= slot_minutes < end_minutes:
                location_total_row[i] += 1
    
    # Add individual reservation rows first (reversed so latest shows first)
    for item in reversed(location_items_sorted):
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
        
        z_data_detail.append(row)
        y_labels_detail.append(f"ID {item['id']} ({item['time']})")
    
    # Add TOTAL row at the END (so it appears at TOP of chart)
    z_data_detail.append(location_total_row)
    y_labels_detail.append(f"📊 TOTAL ({len(location_items)} reservations)")
    
    # Create detailed heatmap
    fig_detail = go.Figure(data=go.Heatmap(
        z=z_data_detail,
        x=times,
        y=y_labels_detail,
        colorscale=[
            [0, 'white'],
            [0.5, '#ff6b6b'],
            [1, '#e74c3c']
        ],
        showscale=False,  # Remove color bar (legend)
        text=[[''] * len(row) for row in z_data_detail[:-1]] + [  # No text for individual rows
            [str(val) if val > 0 else '' for val in z_data_detail[-1]]  # Numbers for TOTAL row
        ],
        texttemplate="%{text}",
        textfont={"size": 12, "color": "white"},
        hoverongaps=False,
        hovertemplate="<b>%{y}</b><br>Time: %{x}<br>Value: %{z}<extra></extra>"
    ))
    
    # Add vertical dotted lines at 30-minute intervals
    for i in range(0, len(times), 3):  # Every 3rd time slot (30 minutes)
        x_pos = i
        
        # Add vertical line using shape
        fig_detail.add_shape(
            type="line",
            x0=x_pos,
            x1=x_pos,
            y0=-0.5,
            y1=len(y_labels_detail) - 0.5,
            line=dict(color="rgba(128,128,128,0.3)", width=0.5, dash="dash"),
            xref="x",
            yref="y"
        )
    
    fig_detail.update_layout(
        title=f"Detailed View: {location}",
        xaxis_title="Time",
        yaxis_title="Reservation Details",
        height=max(300, (len(location_items_sorted) + 1) * 25 + 100),  # +1 for total row
        xaxis=dict(
            tickangle=45,
            tickmode='linear',
            dtick=3  # 30-minute intervals
        ),
        yaxis=dict(
            tickfont=dict(size=10)
        ),
        margin=dict(l=200, r=50, t=50, b=80),
        showlegend=False
    )
    
    return fig_detail

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

def create_location_summary(data):
    """Create location-wise summary"""
    location_counts = {}
    for item in data:
        location = item['location']
        location_counts[location] = location_counts.get(location, 0) + 1
    
    if location_counts:
        locations = list(location_counts.keys())
        counts = list(location_counts.values())
        
        fig = px.pie(
            values=counts,
            names=locations,
            title='Reservations by Location'
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
        ["Use Sample Data", "Upload CSV File", "Manual Input"]
    )
    
    data = DEFAULT_DATA.copy()
    
    if data_input_method == "Upload CSV File":
        uploaded_file = st.sidebar.file_uploader("Select CSV file", type="csv")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                required_columns = ['location', 'id', 'time']
                if all(col in df.columns for col in required_columns):
                    data = df.to_dict('records')
                    st.sidebar.success(f"Loaded {len(data)} reservation records.")
                else:
                    st.sidebar.error(f"CSV file must contain columns: {', '.join(required_columns)}")
            except Exception as e:
                st.sidebar.error(f"File reading error: {e}")
    
    elif data_input_method == "Manual Input":
        st.sidebar.subheader("Add Reservation")
        with st.sidebar.form("add_reservation"):
            new_location = st.text_input("Location", value="Sample 1")
            new_id = st.number_input("Reservation ID", min_value=1, value=int(4.2e8))
            new_time = st.time_input("Reservation Time")
            
            if st.form_submit_button("Add Reservation"):
                data.append({
                    'location': new_location,
                    'id': int(new_id),
                    'time': new_time.strftime("%H:%M")
                })
                st.sidebar.success("Reservation added.")
                st.experimental_rerun()
    
    # Location filter
    locations = sorted(list(set([item['location'] for item in data])))
    selected_location = st.sidebar.selectbox(
        "Filter by Location",
        ["All Locations"] + locations
    )
    
    # Data processing
    time_slots, reservation_data = calculate_time_slots(data, start_hour, end_hour, selected_location)
    
    # Show filtering info
    total_filtered = len(reservation_data)
    total_original = len([item for item in data if selected_location == "All Locations" or item['location'] == selected_location])
    
    if total_filtered < total_original:
        filtered_out = total_original - total_filtered
        st.info(f"ℹ️ {filtered_out} reservations are hidden (outside time range considering ±30min buffer)")
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #4a90e2; margin: 0;">Total Reservations</h3>
            <h2 style="margin: 0;">{len(reservation_data)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Calculate max overlap per location separately
        max_overlap = calculate_max_overlap_per_location(reservation_data, start_hour, end_hour)
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #f39c12; margin: 0;">Max Overlap</h3>
            <h2 style="margin: 0;">{max_overlap}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        unique_locations = len(set([item['location'] for item in reservation_data]))
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #27ae60; margin: 0;">Active Locations</h3>
            <h2 style="margin: 0;">{unique_locations}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Reservation Chart", "📈 Overlap Analysis", "🏢 Location Summary", "📋 Reservation List"])
    
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
        
        # Summary heatmap and location details
        if reservation_data:
            fig_summary, location_groups = create_heatmap(time_slots, reservation_data, selected_location)
            st.plotly_chart(fig_summary, use_container_width=True)
            
            # Location details with expanders (maintain same order as summary chart)
            for location in location_groups.keys():  # location_groups is already sorted
                location_items = location_groups[location]
                with st.expander(f"🏢 {location} ({len(location_items)} reservations)", expanded=False):
                    # Create detailed heatmap for this location
                    fig_detail = create_location_detail_heatmap(location, location_items, time_slots)
                    st.plotly_chart(fig_detail, use_container_width=True)
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
                    reservation_details = []
                    for res in slot['reservations']:
                        reservation_details.append(f"ID {res['id']} ({res['location']})")
                    
                    st.markdown(f"""
                    <div class="reservation-card">
                        <strong>{slot['time']}</strong>
                        <span class="overlap-badge">{slot['count']} Overlaps</span>
                        <br><small>Reservations: {', '.join(reservation_details)}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No overlapping reservations.")
    
    with tab3:
        st.subheader("Location Summary")
        
        location_fig = create_location_summary(reservation_data)
        if location_fig:
            st.plotly_chart(location_fig, use_container_width=True)
            
            # Location breakdown table - sorted by reservation count
            location_breakdown = {}
            for item in reservation_data:
                loc = item['location']
                if loc not in location_breakdown:
                    location_breakdown[loc] = []
                location_breakdown[loc].append(item)
            
            # Sort locations by reservation count (descending)
            sorted_locations_summary = sorted(location_breakdown.keys(), 
                                            key=lambda loc: len(location_breakdown[loc]), 
                                            reverse=True)
            
            for location in sorted_locations_summary:
                items = location_breakdown[location]
                with st.expander(f"🏢 {location} ({len(items)} reservations)"):
                    for item in sorted(items, key=lambda x: time_to_minutes(x['time'])):
                        st.write(f"• ID {item['id']} at {item['time']}")
        else:
            st.info("No location data to display.")
    
    with tab4:
        st.subheader("All Reservations")
        
        if reservation_data:
            # Sort reservations by location, then by time
            sorted_reservations = sorted(reservation_data, 
                                       key=lambda x: (x['location'], time_to_minutes(x['time'])))
            
            for item in sorted_reservations:
                original_minutes = time_to_minutes(item['time'])
                start_time = minutes_to_time(original_minutes - 30)
                end_time = minutes_to_time(original_minutes + 30)
                
                st.markdown(f"""
                <div class="reservation-card">
                    <span class="location-badge">{item['location']}</span>
                    <strong>ID #{item['id']}</strong>
                    <span class="available-badge">Active</span>
                    <br>
                    <small>Reservation Time: {item['time']}</small>
                    <br>
                    <small>Actual Occupancy: {start_time} ~ {end_time}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No reservations.")

if __name__ == "__main__":
    main()