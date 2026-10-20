# Ayan Ali Saleem

**MSc Robotics & Artificial Intelligence, ITMO University (2024–26) — 5.0/5.0, Red Diploma (honours)**
**BE Electrical Engineering, NED University of Engineering and Technology, Karachi**

I work on perception and motion planning for autonomous ground vehicles: training-free 3D perception from camera + LiDAR, depth-supervised 3D reconstruction, and hierarchical planning and control (A* → DWA → MPC → PID).

I am applying for PhD positions in **perception, 3D reconstruction, motion planning, and autonomous navigation**.

[Portfolio](https://ayanali.tech/) · [LinkedIn](https://www.linkedin.com/in/ayan-saleem) · [ORCID](https://orcid.org/0009-0004-4690-1346) · ayansaleem827@gmail.com · Karachi, Pakistan

---

## Selected work

| Project | What it is | Result / status |
|---|---|---|
| **3D Perception for Autonomous Ground Vehicles** (MSc thesis) | Training-free pipeline: YOLOv8m-seg → calibrated LiDAR projection → adaptive mask erosion → DBSCAN → PCA 3D oriented boxes | KITTI: **Car IoU 50.51%, Pedestrian IoU 38.63%, ~11 FPS, 1,874 MiB** peak GPU memory. Code release in preparation |
| **[TriLayerNav](https://github.com/ayanali827/TriNav-Tri-Layer-Navigation-A-DWA-MPC-)** | Tri-layer navigation framework (A*, DWA, MPC, PID) for differential-drive robots in MuJoCo | **Published:** *Gyroscopy and Navigation*, 2026 — [paper](https://link.springer.com/article/10.1134/S2075108726700094) |
| **[Depth-Supervised NeRF](https://github.com/ayanali827/depth-supervised-nerf-notebooks)** | Controlled comparison of hard, soft, and hybrid depth-integration strategies for NeRF training | NeRF Synthetic dataset; PSNR / SSIM / depth-error evaluation |
| **[YOLO benchmark on KITTI](https://github.com/ayanali827/object-detection-autonomous-navigation-yolo)** | YOLOv8 / YOLO11 / YOLO12 compared for driving perception | 954-image KITTI subset: **mAP@0.5 75.6 / 74.8 / 73.2**, 42–45 FPS |
| **[Citation Reliability of Small LLMs](https://github.com/ayanali827/citation-reliability-small-llms)** | 850 references from Phi-3-mini and humains-junior verified against Crossref / OpenAlex across 45 topics | REAL_OK rate: **0.39 on famous topics → 0.03 on niche topics** (topic-level analysis, Wilson CIs) |

## Publications

- **TriLayerNav: A Tri-Layer Navigation Framework Integrating A*, DWA, and MPC for Differential-Drive Robots** — *Gyroscopy and Navigation*, 2026. [Publisher page](https://link.springer.com/article/10.1134/S2075108726700094)
- **Improving NeRF Training Quality Using Depth Data: A Comparative Study of Depth-Integration Strategies for 3D Scene Reconstruction** — 2026, manuscript under review. Code: [depth-supervised-nerf-notebooks](https://github.com/ayanali827/depth-supervised-nerf-notebooks)

## Research interests

- 3D perception and sensor fusion (camera + LiDAR) for autonomous ground vehicles
- 3D reconstruction (NeRF, depth supervision, Gaussian splatting)
- Motion planning and model-based control (A*, DWA, MPC)
- State estimation (UKF) and reliable evaluation methodology

## Methods & tools

Python · PyTorch · Open3D · MuJoCo · ROS · C/C++ · MATLAB
A* · DWA · MPC · PID · UKF · DBSCAN · YOLO · NeRF

---

<sub>perception · planning · autonomy</sub>
