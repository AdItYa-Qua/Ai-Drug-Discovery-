## 🚀 Overview
NeuralChem AI is an AI-powered, cloud-native platform designed to streamline early-stage drug discovery by integrating real-time molecular visualization, AI-driven docking insights, and automated literature analysis. Leveraging **Graph Neural Networks (GNNs)** and **Natural Language Processing (NLP)**, NeuralChem AI accelerates drug candidate screening, optimizes molecular structures, and provides deep insights into chemical interactions.

## 🧪 Problem Statement
Chemical researchers face significant challenges due to fragmented research data, time-consuming manual analysis, and the complexity of identifying optimal drug compounds. NeuralChem AI solves these inefficiencies by providing a unified, AI-powered platform for real-time drug discovery insights.

## 🎯 Key Features
- **🔬 2D Molecular Visualization** – Intuitive molecular structure representation with interactive insights.
- **🤖 AI-Powered Docking Insights** – Predict binding affinities, optimize ligand interactions, and refine docking strategies.
- **📚 Automated Literature Integration** – NLP-driven research paper analysis for relevant insights.
- **⚛️ Structure-Based Molecular Optimization** – AI-driven suggestions to enhance stability and efficacy.
- **📊 Interactive Dashboard** – A user-friendly interface to visualize results, compare drug candidates, and generate reports.
- **☁️ Cloud-Native & Scalable** – Built on Google Cloud for secure and high-performance computations.
- **📎 SMILES-Based Input** – Accepts molecular input in **SMILES format** for seamless integration.

## 🔧 Tech Stack
- **Frontend:** React.js (for interactive UI)
- **Backend:** FastAPI (for AI model serving)
- **AI Models:** Graph Neural Networks (GNNs), NLP-based literature analysis
- **Database:** PostgreSQL (for structured data storage)
- **Infrastructure:** Google Cloud, Docker, Kubernetes

## 📌 Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Node.js (for frontend development)
- Docker (for containerization)

### Steps to Run Locally
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-username/NeuralChem-AI.git
   cd NeuralChem-AI
   ```
2. **Set Up Backend:**
   ```sh
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
3. **Set Up Frontend:**
   ```sh
   cd frontend
   npm install
   npm start
   ```
4. **Run Docker (Optional):**
   ```sh
   docker-compose up --build
   ```
5. Access the application at `(https://8813a3d3-eca7-43a0-852a-bdde576179b8-00-2yur58r2pj322.riker.replit.dev/docking/results/5ebfe03e-e25f-476f-b905-86a50cd9db67 )`

## 📜 API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/predict-binding` | Predicts ligand-receptor binding affinity |
| `POST` | `/suggest-structure` | Provides AI-driven molecular optimization suggestions |
| `GET` | `/literature-insights` | Fetches relevant research insights based on input molecule |

## 🛠 Contributors
- **Aditya More** 
- **Srisailesh** 
- **Kritagya Sharma** 
- **Ranjan Kumar** 

## 🤝 Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to your fork and create a Pull Request

## 📧 Contact
For inquiries, reach out to [adityamore18706@gmail.com] or open an issue on GitHub.

---
_Developed by **404NotFound** - Indian Institute of Petroleum and Energy (IIPE)_
