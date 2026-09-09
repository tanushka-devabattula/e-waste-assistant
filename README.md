# ♻️ AI E-Waste Assistant

An AI-powered decision-support assistant that helps users choose a responsible pathway for unwanted or damaged electronic devices.

Instead of simply asking whether an item is "waste", the assistant recommends one of five pathways:

**Repair → Reuse → Donate/Refurbish → Recycle → Responsible Disposal**

---

## 🚀 Live Demo

The AI E-Waste Assistant is deployed using Streamlit Community Cloud and is publicly accessible as a web application.

---

## 🎯 Problem Statement

Electronic waste is increasing rapidly, while people often do not know what to do with old, damaged, or unwanted electronic devices.

The AI E-Waste Assistant provides contextual guidance based on the device type, age, working status, condition, and optionally an uploaded image.

The goal is to encourage responsible consumption, extend device lifetimes where possible, and promote appropriate e-waste handling.

---

## 🤖 Key Features

### 1. AI-Powered Recommendation

Uses a Large Language Model (LLM) to analyze the user's device information and recommend the most appropriate e-waste pathway.

### 2. Lightweight RAG

Retrieves relevant guidance from a curated local e-waste knowledge base before generating the recommendation.

### 3. Vision AI

Users can optionally upload a device image. A vision-capable AI model provides supporting visual analysis.

### 4. Safety Guardrails

A rule-based safety check detects potentially hazardous battery conditions such as:

- Swollen batteries
- Leaking batteries
- Overheating
- Burning or smoke
- Damaged or ruptured batteries

For hazardous conditions, the system prioritizes professional handling instead of repair.

### 5. Sustainability Impact

Provides a qualitative explanation of how the recommended pathway can contribute to sustainable consumption and responsible e-waste management.

### 6. Responsible AI

The application includes transparency, human oversight, privacy, reliability, and image-analysis limitations.

---

## 🌱 SDG Alignment

### Primary SDG: SDG 12 — Responsible Consumption and Production

The project supports responsible consumption by encouraging:

- Repair instead of premature replacement
- Reuse of functional devices
- Donation and refurbishment
- Responsible electronic-waste recycling
- Safe disposal of hazardous electronic components

---

## 🧠 System Workflow

User Input
    │
    ├── Device Type
    ├── Age
    ├── Working Status
    ├── Condition
    └── Optional Image
          │
          ▼
   Safety Risk Check
          │
          ▼
   Knowledge Retrieval
        (RAG)
          │
          ▼
      AI Analysis
          │
          ├── Text LLM
          └── Vision AI
          │
          ▼
  Safety Override if Required
          │
          ▼
 Recommended E-Waste Pathway
          │
          ▼
 Sustainability Impact

---

## 🛠️ Technologies Used

- Python
- Streamlit
- OpenRouter API
- Large Language Models (LLMs)
- Vision AI
- Retrieval-Augmented Generation (RAG)
- Git & GitHub
- python-dotenv

---

## 📂 Project Structure

e-waste-assistant/
│
├── app.py
├── knowledge_base.txt
├── requirements.txt
├── README.md
└── .gitignore

> API credentials are stored securely outside the Git repository and are never committed to source control.

---

## ☁️ Deployment

The application is deployed using Streamlit Community Cloud.

The application uses a secure deployment secret for the OpenRouter API key rather than storing the key in the GitHub repository.

---

## 🔐 Safety & Responsible AI

The assistant is designed as an AI decision-support tool and does not replace professional inspection.

Important safeguards include:

- No step-by-step DIY repair instructions
- No instructions for dismantling or modifying devices
- Hazardous battery conditions trigger a safety override
- Damaged batteries are directed toward professional handling
- Image analysis is treated as supporting evidence
- Users are advised not to provide sensitive personal information
- Recommendations should be independently verified when safety is involved

---

## ⚠️ Limitations

- AI recommendations may contain errors.
- Image analysis cannot reliably identify hidden internal damage.
- Battery health and electrical safety cannot be confirmed from an image alone.
- The sustainability impact shown is qualitative and is not a scientific carbon-footprint calculation.
- The current RAG implementation uses lightweight keyword-based retrieval rather than a vector database or embedding-based retrieval system.

---

## 🔮 Future Improvements

- Location-based e-waste collection facility recommendations
- More comprehensive verified e-waste knowledge sources
- Embedding-based RAG with a vector database
- Improved device image classification
- Multilingual support
- E-waste collection and recycling center integration

---

## 👩‍💻 Project

**AI E-Waste Repair, Reuse & Responsible Disposal Assistant**

Built as part of the **1M1B AI for Sustainability Virtual Internship**.

**Author:** Tanushka Devabattula