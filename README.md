# 🚀 SYNAPSE – Synthetic Data Intelligence Platform

## 🌐 Live Application

👉[https://synapse-ai-data-platform.streamlit.app/]

---

##  Overview

SYNAPSE is an end-to-end synthetic data generation and validation platform designed to simulate real-world datasets and evaluate their usability for machine learning.

Unlike traditional synthetic data tools that only generate data, SYNAPSE goes further by **measuring how trustworthy and useful the generated data is** through statistical and ML-based validation techniques.

---

##  Key Features

### 🔹 Synthetic Data Generation

* Domain-specific dataset simulation for:

  * E-commerce
  * IoT systems
  * Fintech transactions
* Supports scalable dataset creation with configurable size and ratio
* Adaptive generation:

  * Uses CTGAN 
  * Falls back to optimized statistical sampling for reliability

---

### 🔹 Data Quality Evaluation

SYNAPSE evaluates synthetic data across three critical dimensions:

#### 📊 1. Distribution Similarity

* Compares statistical distributions between real and synthetic data
* Ensures realistic feature behavior

#### 🔗 2. Correlation Fidelity

* Preserves relationships between variables
* Validates feature dependencies using correlation matrices

#### 🤖 3. ML Utility Score

* Measures how well models trained on synthetic data perform
* Uses cross-training strategy:

  * Train on real → test on synthetic
  * Train on synthetic → test on real

---

### 🔹 🧠 Trust Score System

* Combines all validation metrics into a unified **Trust Score**
* Categorizes dataset reliability:

  * High Trust
  * Moderate Trust
  * Low Trust

---

### 🔹 📊 Interactive Dashboard

Built with Streamlit and Plotly:

* Real-time dataset insights
* Interactive visualizations:

  * Feature distributions
  * Correlation heatmaps
  * Target balance
* KPI indicators with visual signals (🟢🟡🔴)

---

### 🔹 📥 Export Ready

* Download full synthetic datasets as CSV
* Ready for ML model training and experimentation

---

## 🏗️ Architecture

```text
User Input → Event Simulation → Data Processing → Silver Layer (DuckDB)
→ Gold Mart → Synthetic Generation → Validation → Dashboard
```

---

## ⚙️ Tech Stack

| Category         | Tools                         |
| ---------------- | ----------------------------- |
| Language         | Python                        |
| Backend          | DuckDB                        |
| Data Processing  | Pandas, NumPy                 |
| Machine Learning | Scikit-learn                  |
| Synthetic Data   | SDV (CTGAN) + Custom Fallback |
| Visualization    | Plotly                        |
| Frontend         | Streamlit                     |
| Deployment       | Streamlit Cloud               |

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/arunp061106/SYNAPSE.git
cd SYNAPSE
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the Application

```bash
streamlit run app.py
```

---

## 📊 Sample Use Cases

* Training ML models when real data is unavailable
* Data privacy-preserving analytics
* Testing data pipelines and ML systems
* Benchmarking model robustness

---

## 🧠 What Makes SYNAPSE Unique?

Most synthetic data tools focus only on generation.

SYNAPSE introduces a **trust-driven approach** by answering:

> “Is this synthetic data actually useful for machine learning?”

This is achieved through:

* Statistical validation
* Relationship preservation
* Model performance testing

---

## 🔮 Future Enhancements

* Support for time-series synthetic data
* Multi-table relational data generation
* Advanced GAN-based modeling
* API-based dataset generation
* Real-time monitoring dashboard

---

## 👨‍💻 Author

**Arun Karthick P**
*Aspiring Data Analyst*
B.TECH CSE
Student iN SRM INSTITUTE OF SCIENCE AND TECHNOLOGY, TIRUCHIRAPALLI.

---

## ⭐ Acknowledgements

* Open-source ML ecosystem
* Streamlit community
* Synthetic data research advancements
