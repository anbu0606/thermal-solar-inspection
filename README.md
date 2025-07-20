# 🔥 Thermal Inspection of Solar Panels using AI & IBM Maximo

> A real-time, AI-powered defect detection system for solar panels using thermal imaging, IBM Maximo Visual Inspection, and live Grafana dashboards — developed as part of IBM Consulting Internship 2025.

---

## 📌 Project Overview

Solar panel efficiency can drastically drop due to invisible thermal defects like hot spots, cracks, and air gaps. Manual inspections using IR cameras are time-consuming and error-prone.

This project solves that by leveraging **AI-powered thermal image processing** using **IBM Maximo Visual Inspection (MVI)** and **YOLOv3**, combined with a real-time analytics and alerting pipeline using **Flask**, **SQLite**, **MQTT**, **Docker**, and **Grafana**.

---

## 🎯 Key Objectives

- Automate thermal inspections of solar panels.
- Identify potential defects (hot/cold spots, cracks, air gaps).
- Provide real-time alerts and visualization dashboards.
- Improve precision, speed, and energy efficiency.

---

## ⚙️ Features

✅ Trained AI models on thermal images using IBM Maximo  
✅ Defect detection with >90% precision  
✅ Real-time MQTT alerts with 35% latency reduction  
✅ Grafana dashboards connected to live SQLite data  
✅ Dockerized deployment for cross-platform use  
✅ Secure API endpoints protected by HTTP Basic Auth

---

## 🧠 Tech Stack

| Layer             | Technology Used                                     |
|------------------|------------------------------------------------------|
| Image Detection  | YOLOv3 + IBM Maximo Visual Inspection (MVI)         |
| Web API          | Flask + Connexion + Swagger                         |
| Alert System     | MQTT (Mosquitto)                                     |
| Data Storage     | SQLite                                               |
| Dashboard        | Grafana (Dockerized)                                 |
| Deployment       | Docker, Docker Compose                               |
| Authentication   | HTTP Basic Auth                                      |
| Language         | Python 3                                             |

---

## 🧪 Results

| Metric                     | Value                        |
|---------------------------|------------------------------|
| Model Precision            | > 90%                        |
| Diagnostic Accuracy Boost  | +20% vs manual inspection    |
| Alert Latency Improvement  | -35%                         |
| Defects Detected           | Hot spots, Cold spots, Cracks, Air gaps |

---

## 🖼️ Sample Dashboard (Grafana)

<<<<<<< HEAD
![Grafana Screenshot](/thermal-solar-inspection/grafana-dashboard.png)
=======
![Grafana Screenshot](\thermal-solar-inspection\grafana-dashboard.png)
>>>>>>> ffb7430e466252194d4fbc2033a59fd7f9c3a50a

> 📊 The dashboard visualizes panel-level thermal metrics, system alerts, and real-time defect classification.

---

## 🧭 Architecture

```
[IR Camera] → [YOLOv3/MVI Detection] → [SQLite DB] → [Grafana Dashboard]
                                 ↘
                                [MQTT Alert Stream]
