#  Wrong Direction Vehicle Detection System

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-000000?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)

<br/>

**A state-of-the-art, real-time computer vision & telemetry solution designed to detect vehicles traveling against permitted traffic flow, automatically capture violation evidence, and display actionable telemetry via a SOC-grade terminal.**

[Explore Features](#-key-features) • [System Architecture](#-system-architecture) • [Quick Start](#-quick-start) • [Dashboard Overview](#-dashboard--ui)

</div>

---

##  Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start Guide](#-quick-start)
- [Dashboard & UI](#-dashboard--ui)
- [Configuration & Road Layouts](#-configuration--road-layouts)
- [License & Acknowledgments](#-license--acknowledgments)

---

##  Overview

Wrong-way driving (WWD) on highways and urban roads is a primary contributor to severe traffic fatalities. This system addresses the issue by integrating **deep learning detection (YOLOv8)** with **robust spatial tracking (ByteTrack)** and **Self-Calibrating Anomaly Detection**.

Rather than relying purely on rigid tripwires, the pipeline dynamically computes vector movement angles and dot products relative to established lane flows. The result is an adaptive, high-precision monitoring system paired with a matte-graphite **Security Operations Center (SOC)** dashboard.

---

##  Key Features

| Feature | Description |
| :--- | :--- |
|  **Multi-Class Detection** | Real-time localization of cars, trucks, buses, and motorcycles powered by YOLOv8. |
|  **Persistent Tracking** | Maintains continuous track IDs and spatial trajectory trails across frames using ByteTrack. |
|  **Self-Calibrating Logic** | Dynamically analyzes direction vectors to adapt to 1-way, 2-way, or angled traffic flows. |
|  **Evidence Capture** | Automatically crops and stores high-resolution snapshot captures of offending vehicles. |
|  **Audit Trail Logging** | Generates thread-safe CSV logs with timestamps, track IDs, and violation metadata. |
|  **Industrial SOC UI** | High-contrast Streamlit terminal featuring live telemetry, metrics, and evidence galleries. |

---

##  System Architecture

```mermaid
flowchart TD
    A[📹 Video Input Stream] --> B[🔍 YOLOv8 Detection Engine]
    B --> C[ ByteTrack Tracking System]
    C --> D[ Trajectory History Manager]
    D --> E[ Self-Calibrating Anomaly Analyzer]
    E -->|Normal Flow| F[ Render Trajectory Trails]
    E -->|Violation Detected| G[ Trigger Alarm & Vector Alert]
    G --> H[ Snapshot Crop & CSV Audit Logger]
    F --> I[ SOC Terminal Dashboard]
    H --> I
