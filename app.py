import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="시간 예약 현황 관리 시스템",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
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

.excluded-card {
    background-color: #ffe6e6;
    border-left-color: var(--danger-color);
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

# 원본 데이터
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
    """시간 문자열을 분으로 변환"""
    try:
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    except:
        return 0

def minutes_to_time(minutes):
    """분을 시간 문자열로 변환"""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"

def get_valid_data(data, start_hour=8, end_hour=18):
    """유효한 데이터 필터링 (범위 내 예약만)"""
    valid_data = []
    excluded_data = []
    
    for item in data:
        original_minutes = time_to_minutes(item['time'])
        start_minutes = original_minutes - 30
        end_minutes = original_minutes + 30
        
        # 예약 시간 범위가 운영시간과 겹치는지 확인
        if end_minutes > start_hour * 60 and start_minutes < end_hour * 60:
            valid_data.append(item)
        else:
            excluded_data.append(item)
    
    return valid_data, excluded_data

def calculate_time_slots(data, start_hour=8, end_hour=18):
    """시간 슬롯별 예약 현황 계산"""
    valid_data, excluded_data = get_valid_data(data, start_hour, end_hour)
    
    # 10분 간격 시간 슬롯 생성
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
    
    # 각 예약에 대해 슬롯 점유 계산
    for item in valid_data:
        original_minutes = time_to_minutes(item['time'])
        start_minutes = original_minutes - 30
        end_minutes = original_minutes + 30
        
        for slot in time_slots:
            slot_minutes = slot['minutes']
            if start_minutes <= slot_minutes < end_minutes:
                slot['count'] += 1
                slot['reservations'].append(item['id'])
    
    return time_slots, valid_data, excluded_data

def create_heatmap(time_slots, valid_data):
    """히트맵 차트 생성"""
    # 시간대별 데이터 준비
    times = [slot['time'] for slot in time_slots]
    reservation_ids = [item['id'] for item in valid_data]
    
    # 2D 배열 생성 (예약 ID x 시간)
    z_data = []
    y_labels = []
    
    for item in valid_data:
        row = []
        original_minutes = time_to_minutes(item['time'])
        start_minutes = original_minutes - 30
        end_minutes = original_minutes + 30
        
        for slot in time_slots:
            slot_minutes = slot['minutes']
            if start_minutes <= slot_minutes < end_minutes:
                row.append(1)  # 예약됨
            else:
                row.append(0)  # 가능
        
        z_data.append(row)
        y_labels.append(f"ID {item['id']} ({item['time']})")
    
    # 총합 행 추가
    total_row = [slot['count'] for slot in time_slots]
    z_data.append(total_row)
    y_labels.append("합계")
    
    # 히트맵 생성
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
            title="예약 수",
            tickmode="linear",
            tick0=0,
            dtick=1
        ),
        text=[[str(val) if val > 1 else '' for val in row] for row in z_data],
        texttemplate="%{text}",
        textfont={"size": 10, "color": "white"},
        hoverongaps=False,
        hovertemplate="<b>%{y}</b><br>시간: %{x}<br>예약 수: %{z}<extra></extra>"
    ))
    
    fig.update_layout(
        title="시간 예약 현황 차트 (±30분 적용)",
        xaxis_title="시간",
        yaxis_title="예약 ID",
        height=600,
        xaxis=dict(
            tickangle=45,
            tickmode='linear',
            dtick=6  # 1시간 간격으로 표시
        ),
        margin=dict(l=100, r=50, t=50, b=100)
    )
    
    return fig

def create_overlap_chart(time_slots):
    """중복 예약 분포 차트"""
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
            labels={'x': '동시 예약 수', 'y': '시간 슬롯 개수'},
            title='동시 예약 현황 분포',
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

# 메인 애플리케이션
def main():
    st.title("📅 시간 예약 현황 관리 시스템")
    st.markdown("**±30분 버퍼 시간이 적용된 예약 현황을 시각화합니다**")
    
    # 사이드바 설정
    st.sidebar.header("⚙️ 설정")
    
    # 운영 시간 설정
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_hour = st.selectbox("시작 시간", range(0, 24), index=8)
    with col2:
        end_hour = st.selectbox("종료 시간", range(1, 25), index=18)
    
    if start_hour >= end_hour:
        st.sidebar.error("종료 시간은 시작 시간보다 늦어야 합니다.")
        return
    
    # 데이터 입력 방식 선택
    data_input_method = st.sidebar.radio(
        "데이터 입력 방식",
        ["기본 데이터 사용", "CSV 파일 업로드", "수동 입력"]
    )
    
    data = DEFAULT_DATA.copy()
    
    if data_input_method == "CSV 파일 업로드":
        uploaded_file = st.sidebar.file_uploader("CSV 파일을 선택하세요", type="csv")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if 'id' in df.columns and 'time' in df.columns:
                    data = df.to_dict('records')
                    st.sidebar.success(f"{len(data)}개의 예약 데이터를 로드했습니다.")
                else:
                    st.sidebar.error("CSV 파일에 'id'와 'time' 컬럼이 필요합니다.")
            except Exception as e:
                st.sidebar.error(f"파일 읽기 오류: {e}")
    
    elif data_input_method == "수동 입력":
        st.sidebar.subheader("예약 추가")
        with st.sidebar.form("add_reservation"):
            new_id = st.number_input("예약 ID", min_value=1, value=len(data)+1)
            new_time = st.time_input("예약 시간")
            
            if st.form_submit_button("예약 추가"):
                data.append({
                    'id': new_id,
                    'time': new_time.strftime("%H:%M")
                })
                st.sidebar.success("예약이 추가되었습니다.")
    
    # 데이터 처리
    time_slots, valid_data, excluded_data = calculate_time_slots(data, start_hour, end_hour)
    
    # 메트릭 표시
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #4a90e2; margin: 0;">전체 예약</h3>
            <h2 style="margin: 0;">{}</h2>
        </div>
        """.format(len(data)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #27ae60; margin: 0;">유효 예약</h3>
            <h2 style="margin: 0;">{}</h2>
        </div>
        """.format(len(valid_data)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #e74c3c; margin: 0;">제외된 예약</h3>
            <h2 style="margin: 0;">{}</h2>
        </div>
        """.format(len(excluded_data)), unsafe_allow_html=True)
    
    with col4:
        max_overlap = max([slot['count'] for slot in time_slots]) if time_slots else 0
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #f39c12; margin: 0;">최대 중복</h3>
            <h2 style="margin: 0;">{}</h2>
        </div>
        """.format(max_overlap), unsafe_allow_html=True)
    
    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs(["📊 예약 차트", "📈 중복 분석", "📋 예약 목록", "⚠️ 제외된 예약"])
    
    with tab1:
        st.subheader("시간대별 예약 현황")
        
        # 범례
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;">
            <div class="legend-item">
                <div class="legend-color" style="background-color: white; border: 2px solid #ccc;"></div>
                <span>이용 가능</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #ff6b6b;"></div>
                <span>예약됨</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #e74c3c;"></div>
                <span>중복 예약</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 히트맵 차트
        if valid_data:
            fig = create_heatmap(time_slots, valid_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("표시할 유효한 예약이 없습니다.")
    
    with tab2:
        st.subheader("중복 예약 분석")
        
        overlap_fig = create_overlap_chart(time_slots)
        if overlap_fig:
            st.plotly_chart(overlap_fig, use_container_width=True)
            
            # 중복이 많은 시간대 표시
            high_overlap_slots = [slot for slot in time_slots if slot['count'] >= 3]
            if high_overlap_slots:
                st.warning(f"⚠️ {len(high_overlap_slots)}개 시간대에서 3회 이상 중복 예약이 발생했습니다.")
                
                for slot in high_overlap_slots[:5]:  # 상위 5개만 표시
                    st.markdown(f"""
                    <div class="reservation-card">
                        <strong>{slot['time']}</strong>
                        <span class="overlap-badge">{slot['count']}회 중복</span>
                        <br><small>예약 ID: {', '.join(map(str, slot['reservations']))}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("중복 예약이 없습니다.")
    
    with tab3:
        st.subheader("유효한 예약 목록")
        
        if valid_data:
            for item in valid_data:
                original_minutes = time_to_minutes(item['time'])
                start_time = minutes_to_time(original_minutes - 30)
                end_time = minutes_to_time(original_minutes + 30)
                
                st.markdown(f"""
                <div class="reservation-card">
                    <strong>예약 {item['id']}번</strong>
                    <span class="available-badge">유효</span>
                    <br>
                    <small>예약 시간: {item['time']}</small>
                    <br>
                    <small>실제 점유: {start_time} ~ {end_time}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("유효한 예약이 없습니다.")
    
    with tab4:
        st.subheader("범위 밖 제외된 예약")
        
        if excluded_data:
            st.warning(f"{len(excluded_data)}개의 예약이 운영시간 범위를 벗어나 제외되었습니다.")
            
            for item in excluded_data:
                original_minutes = time_to_minutes(item['time'])
                start_time = minutes_to_time(original_minutes - 30)
                end_time = minutes_to_time(original_minutes + 30)
                
                st.markdown(f"""
                <div class="reservation-card excluded-card">
                    <strong>예약 {item['id']}번</strong>
                    <span style="background-color: #e74c3c; color: white; padding: 0.2rem 0.5rem; border-radius: 15px; font-size: 0.8rem;">제외됨</span>
                    <br>
                    <small>예약 시간: {item['time']}</small>
                    <br>
                    <small>실제 점유: {start_time} ~ {end_time}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("모든 예약이 운영시간 범위 내에 있습니다.")
    
    # 데이터 다운로드
    st.markdown("---")
    st.subheader("📥 데이터 다운로드")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("유효한 예약 데이터 다운로드 (CSV)", type="primary"):
            df = pd.DataFrame(valid_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="CSV 파일 다운로드",
                data=csv,
                file_name=f"valid_reservations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("시간 슬롯 분석 결과 다운로드 (CSV)"):
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
                label="분석 결과 다운로드",
                data=csv,
                file_name=f"time_slot_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()