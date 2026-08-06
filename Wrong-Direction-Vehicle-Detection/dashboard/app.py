import streamlit as st
import tempfile
import os
import sys
import glob

# Add the ROOT directory (parent of 'dashboard') to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.dashboard_pipeline import run_dashboard_pipeline
from utils.snapshot import SnapshotManager

# Configure Streamlit page layout
st.set_page_config(page_title="Wrong Direction Vehicle Detection", layout="wide")
st.title("🚦 Traffic Violation Detection Dashboard")

# Sidebar - Video Upload
st.sidebar.header("1. Upload Video")
uploaded_file = st.sidebar.file_uploader("Upload a traffic video (MP4/AVI)", type=["mp4", "avi", "mov"])

# Sidebar - Settings
st.sidebar.header("2. Control Panel")



start_button = st.sidebar.button("Start Analysis")

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') 
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    col_feed, col_stats = st.columns([2, 1])
    
    with col_feed:
        st.subheader("📹 Live Video Feed")
        stframe = st.empty()
        
    with col_stats:
        st.subheader("📊 Violation Dashboard")
        metric_placeholder = st.empty()
        table_placeholder = st.empty()

    st.markdown("---")
    st.subheader("🖼️ Captured Violation Snapshots")
    gallery_placeholder = st.empty()

    if start_button:
        snapshot_mgr = SnapshotManager()
        violation_records = []
        recorded_ids = set()

        # Pass the selected_road_type into the pipeline
        for frame_rgb, wrong_way_ids in run_dashboard_pipeline(video_path):
            
            # Display live frame with updated container width parameter
            stframe.image(frame_rgb, channels="RGB", use_container_width=True)
            
            for v_id in wrong_way_ids:
                if v_id not in recorded_ids:
                    recorded_ids.add(v_id)
                    violation_records.append({"Vehicle ID": f"ID-{v_id}", "Status": "WRONG DIRECTION"})

            with metric_placeholder.container():
                st.metric(label="Total Violations Detected", value=len(recorded_ids))

            with table_placeholder.container():
                if violation_records:
                    st.dataframe(violation_records, use_container_width=True)
                else:
                    st.info("No violations detected yet.")

            snapshot_files = sorted(glob.glob("snapshots/*.jpg"), key=os.path.getmtime, reverse=True)
            if snapshot_files:
                with gallery_placeholder.container():
                    cols = st.columns(4)
                    for idx, img_path in enumerate(snapshot_files[:8]): 
                        cols[idx % 4].image(img_path, caption=os.path.basename(img_path), use_container_width=True)

        st.success("Analysis Complete!")