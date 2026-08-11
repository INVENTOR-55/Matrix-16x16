# NeoMatrix 16x16 Animations & Configuration

This repository contains matrix configuration files, custom frame-by-frame LED animations, script generators, and 3D printable enclosures for a 16x16 RGB LED Matrix project.

![NeoMatrix Preview](images/00.jpg)

## 📁 Repository Structure

* **`animations/`** – Contains source animation files (JSON / C++ headers) for the matrix display.
* **`3d_models/`** – STL and CAD files for printing the custom LED matrix enclosure.
* **`images/`** – Project showcase photos and diagrams.
* **`matrix.yaml`** – Main configuration file for the LED matrix setup.
* **`generate_yaml.py`** – Python utility script to automate or rebuild the `matrix.yaml` config from animation sources.

---

## 🚀 Quick Start

### 1. Requirements
* Python 3.x

### 2. Generate matrix.yaml
To build or update the YAML configuration based on available files inside the `animations/` directory, run:

```bash
python generate_yaml.py
