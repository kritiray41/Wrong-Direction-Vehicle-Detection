#  Wrong Direction Vehicle Detection System

![Python Version](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-000000?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)

An intelligent, real-time computer vision system that identifies vehicles traveling against permitted traffic flow directions on roadways, logs violations automatically, and displays insights via an interactive dashboard.

---

##  Project Overview

Traffic violations involving wrong-way driving pose high safety risks on highways and urban roads. This system leverages deep learning for vehicle detection and multi-object tracking to analyze movement vectors frame-by-frame. By computing vector alignment via dot-product operations against allowed road trajectory vectors, the pipeline flags violations, triggers visual alerts, logs incident metadata, and saves evidence snapshots.

---

##  Key Features

* **Vehicle Detection:** Powered by YOLOv8 for detection across multiple vehicle classes (cars, trucks, buses, motorcycles).
* **Persistent Tracking:** Uses ByteTrack to maintain continuous track IDs and spatial trajectories across frames.
* **Vector-Based Logic:** Directional analysis utilizing vector movement angles and dot-product calculations relative to defined road vectors.
* **Violation Confirmation & Alerts:** State management to confirm consecutive-frame violations and prevent false positives.
* **Automated CSV Logging:** Logs timestamps, unique track IDs, and violation details while preventing duplicate entries.
* **Evidence Snapshot Management:** Automatically captures and saves annotated images of offending vehicles.
* **Interactive Dashboard:** Built with Streamlit to upload raw footage, view processing pipelines, browse violation tables, and inspect snapshot evidence.

---

## 🛠️ Tech Stack

| Domain | Tools & Frameworks |
| :--- | :--- |
| **Language** | Python 3.9+ |
| **Detection & Vision** | YOLOv8 (Ultralytics), OpenCV, Supervision |
| **Object Tracking** | ByteTrack |
| **Numerical Processing** | NumPy |
| **Dashboard & UI** | Streamlit |
| **Version Control** | Git, GitHub |

---

##  Project Structure

```text
Wrong-Direction-Vehicle-Detection/
├── backend/
│   ├── detection.py        # YOLO model loading & inference
│   ├── tracking.py         # ByteTrack integration & ID maintenance
│   ├── direction.py        # Movement vector computation & dot-product logic
│   └── pipeline.py         # Main processing pipeline controller
├── dashboard/
│   ├── app.py              # Streamlit interface entrypoint
│   ├── pages/              # Additional dashboard pages
│   └── components/         # UI visualizers & galleries[cite: 1]
├── logs/                   # Generated CSV violation logs[cite: 1]
├── models/                 # Pretrained YOLO model weights (.pt)[cite: 1]
├── outputs/                # Saved violation snapshots & annotated output videos[cite: 1]
├── tests/                  # Unit tests and edge-case evaluation scripts[cite: 1]
├── utils/
│   ├── logger.py           # Thread-safe CSV logging utility[cite: 1]
│   └── visualizer.py       # Bounding box, trajectory trail, & alert rendering[cite: 1]
├── videos/                 # Input sample video files[cite: 1]
├── .gitignore
├── main.py                 # Pipeline execution entrypoint
├── README.md
└── requirements.txt        # System dependencies[cite: 1]
