# Multi-Agent System 🤖

## 📌 Overview

This project implements a Multi-Agent System where multiple AI agents collaborate to solve tasks efficiently.

## ⚙️ Architecture

The system consists of the following agents:

* Planner → Plans the tasks
* Researcher → Collects relevant information
* Writer → Generates output
* Critic → Reviews and improves output

## 📁 Project Structure

agents/     → Agent logic (planner, researcher, writer, critic)
memory/     → Stores intermediate results
utils/      → LLM and search utilities
main.py     → Main execution file

## 🚀 How to Run

1. Create and activate the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install the runtime dependencies:

```powershell
python -m pip install streamlit langchain-openai python-dotenv tavily-python
```

3. Run the project:

```powershell
streamlit run app.py
```

PowerShell note: older Windows PowerShell versions do not support `&&`.
Run commands one at a time, or use `;` as the separator:

```powershell
mkdir ai_agent; cd ai_agent
```

The Linux/macOS command `source venv/bin/activate` does not work in PowerShell.

## 🔐 Environment Variables

Create a `.env` file in the root directory and add:

```
OPENAI_API_KEY=your_api_key_here
```

## ✨ Features

* Multi-agent collaboration
* Modular and scalable design
* Easy to extend with new agents

## 👨‍💻 Author

Manjunath Byadagi
