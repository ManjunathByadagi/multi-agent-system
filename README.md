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

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Run the project:

```
python main.py
```

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
