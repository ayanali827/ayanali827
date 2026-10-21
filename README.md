<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img src="assets/banner-dark.svg" width="100%" alt="Ayan Ali Saleem — Robotics and AI Researcher: perception, planning, autonomy">
</picture>

<br>

<a href="https://www.linkedin.com/in/ayan-saleem"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>&nbsp;
<a href="https://ayanali.tech/"><img src="https://img.shields.io/badge/Portfolio-0d1117?style=for-the-badge&logo=googlechrome&logoColor=79c0ff" alt="Portfolio"></a>&nbsp;
<a href="https://orcid.org/0009-0004-4690-1346"><img src="https://img.shields.io/badge/ORCID-0d1117?style=for-the-badge&logo=orcid&logoColor=a6ce39" alt="ORCID"></a>&nbsp;
<a href="mailto:ayansaleem827@gmail.com"><img src="https://img.shields.io/badge/Email-ayansaleem827@gmail.com-79c0ff?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>

</div>

---

# Ayan Ali Saleem

**MSc Robotics & Artificial Intelligence, ITMO University (2024–26) — 5.0/5.0, Red Diploma (honours)**
**BE Electrical Engineering, NED University of Engineering and Technology, Karachi**

I build autonomous systems that **see, decide, and move**: training-free 3D perception from camera + LiDAR, depth-supervised 3D reconstruction, and hierarchical planning and control. I am applying for **PhD positions in perception, 3D reconstruction, motion planning, and autonomous navigation**.

---

## 🧭 My research, as one system

```mermaid
flowchart LR
    subgraph PERCEPTION["👁️ Perception"]
        CAM["Camera"] --> SEG["YOLOv8m-seg<br/>segmentation"]
        LID["LiDAR"] --> PROJ["Calibrated<br/>projection"]
        SEG --> PROJ
        PROJ --> CLU["DBSCAN + PCA"]
        CLU --> BOX["3D oriented<br/>bounding boxes"]
    end
    subgraph RECON["🧊 3D Reconstruction"]
        IMG["Multi-view<br/>images"] --> NERF["NeRF"]
        DEP["Depth supervision<br/>hard · soft · hybrid"] --> NERF
        NERF --> GEO["Geometry +<br/>novel views"]
    end
    subgraph PLAN["🧭 Planning & Control"]
        ASTAR["A*<br/>global planning"] --> DWA["DWA<br/>local avoidance"]
        DWA --> MPC["MPC<br/>trajectory following"]
        MPC --> PID["PID<br/>wheel control"]
    end
    BOX --> ASTAR
    GEO -.-> PROJ
    PID --> ROBOT["🤖 Autonomous<br/>ground vehicle"]

    classDef perc fill:#0d2b45,stroke:#79c0ff,color:#e6f2ff;
    classDef recon fill:#2b1a45,stroke:#bc8cff,color:#f2eaff;
    classDef plan fill:#0d3b2e,stroke:#3fb950,color:#e6fff2;
    class CAM,SEG,LID,PROJ,CLU,BOX perc;
    class IMG,DEP,NERF,GEO recon;
    class ASTAR,DWA,MPC,PID plan;
```

---

## 🔬 Selected work — visual tour

<table>
<tr>
<td width="50%" valign="top">

### 3D Perception for Autonomous Ground Vehicles
*MSc thesis — training-free, no 3D training data*

<img src="https://ayanali.tech/assets/portfolio/project-msc-lidar-point-cloud.png" width="100%" alt="LiDAR point cloud of a street scene, coloured by the perception pipeline">

**KITTI — Car IoU 50.51% · Pedestrian IoU 38.63% · ~11 FPS · 1,874 MiB GPU**
YOLOv8m-seg → LiDAR projection → adaptive mask erosion → DBSCAN → PCA 3D boxes. *Code release in preparation.*

</td>
<td width="50%" valign="top">

### [TriLayer-Nav](https://github.com/ayanali827/TriNav-Tri-Layer-Navigation-A-DWA-MPC-)
*Published — Gyroscopy and Navigation, 2026*

<img src="https://raw.githubusercontent.com/ayanali827/TriNav-Tri-Layer-Navigation-A-DWA-MPC-/main/docs/obstacle_navigation.gif" width="100%" alt="Differential-drive robot navigating around obstacles in MuJoCo using A*, DWA and MPC">

**A\* → DWA → MPC → PID** in MuJoCo, for differential-drive robots.
[Paper](https://doi.org/10.1134/S2075108726700094) · [Code](https://github.com/ayanali827/TriNav-Tri-Layer-Navigation-A-DWA-MPC-)

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [Depth-Supervised NeRF](https://github.com/ayanali827/depth-supervised-nerf-notebooks)
*Does depth supervision fix NeRF geometry?*

<img src="https://ayanali.tech/assets/portfolio/project-depth-nerf-reconstruction.jpg" width="100%" alt="3D scene reconstruction result from the depth-supervised NeRF study">

Controlled comparison of **hard, soft, and hybrid** depth integration on NeRF Synthetic — PSNR / SSIM / depth error.
[Code + notebooks](https://github.com/ayanali827/depth-supervised-nerf-notebooks)

</td>
<td width="50%" valign="top">

### [YOLO Benchmark on KITTI](https://github.com/ayanali827/object-detection-autonomous-navigation-yolo)
*YOLOv8 vs YOLO11 vs YOLO12, like-for-like*

<img src="https://github.com/user-attachments/assets/75aa519e-cb2a-46f0-9afe-71a0348bf83f" width="100%" alt="YOLO object detection on a driving scene — cars and pedestrians boxed">

**mAP@0.5 — 75.6 / 74.8 / 73.2 · 42–45 FPS** on a 954-image KITTI subset, with per-class results.
[Code + results](https://github.com/ayanali827/object-detection-autonomous-navigation-yolo)

</td>
</tr>
</table>

**Also:** 📚 **[Citation Reliability of Small LLMs](https://github.com/ayanali827/citation-reliability-small-llms)** — 850 references from Phi-3-mini and humains-junior verified against Crossref / OpenAlex across 45 topics. REAL_OK rate: **0.39 on famous topics → 0.03 on niche topics** (topic-level analysis, Wilson CIs). A study of when LLM-generated citations can and cannot be trusted.

---

## 📄 Publications

- Mughal, U. A. B., **Ali, A.**, Urwa, & Abramchuk, M. V. **TriLayer-Nav: A Tri-Layer Navigation Framework Integrating A*, Dynamic Window Approach, and Model Predictive Control for Differential-Drive Robots** — *Gyroscopy and Navigation*, 2026, Vol. 17, No. 1, pp. 24–33. [Publisher page](https://link.springer.com/article/10.1134/S2075108726700094)
- **Improving NeRF Training Quality Using Depth Data: A Comparative Study of Depth-Integration Strategies for 3D Scene Reconstruction** — 2026, manuscript under review. Code: [depth-supervised-nerf-notebooks](https://github.com/ayanali827/depth-supervised-nerf-notebooks)

## 🎯 Research interests

- 3D perception and sensor fusion (camera + LiDAR) for autonomous ground vehicles
- 3D reconstruction — NeRF, depth supervision, Gaussian splatting
- Motion planning and model-based control — A*, DWA, MPC
- State estimation (UKF) and rigorous, reproducible evaluation

<div align="center">

## 🛠️ Tech stack

<img src="https://skillicons.dev/icons?i=python,pytorch,opencv,matlab,latex,git,github&perline=7" alt="Python, PyTorch, OpenCV, MATLAB, LaTeX, Git, GitHub">

**Methods:** A* · DWA · MPC · PID · UKF · DBSCAN · YOLO · NeRF · ROS · MuJoCo · Open3D · C/C++

</div>

---

<div align="center">

## 📊 Signals

<table>
<tr>
<td width="50%" align="center" valign="middle">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/radar-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/radar-light.svg">
  <img src="assets/radar-dark.svg" width="400" alt="Skill radar chart">
</picture>

</td>
<td width="50%" align="center" valign="middle">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-stats-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-stats-light.svg">
  <img src="assets/card-stats-dark.svg" width="400" alt="GitHub statistics">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-langs-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-langs-light.svg">
  <img src="assets/card-langs-dark.svg" width="400" alt="Language stack">
</picture>

</td>
</tr>
</table>

<sub>perception · planning · autonomy</sub>

</div>
