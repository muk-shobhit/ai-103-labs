# AI-103 Exam Labs

This repository contains the practical lab exercises and demonstration code used for the AI-103 exam preparation. It provides hands-on demos that illustrate key concepts and services covered in the course, along with runnable Python examples for experimenting locally.

---

[![Create Your First MCP Server](https://img-c.udemycdn.com/course/480x270/7149081_f2e6_7.jpg?w=640&q=75)](https://www.udemy.com/course/ai-103-azure-ai-apps-agents-developer-associate-exam-prep)

Overview
- Purpose: practical, exam-oriented labs with concise demos to reinforce AI-103 topics.
- Includes runnable Python demos and integration examples for common Azure AI services.

Practical demo
- Each lab includes a short, focused practical demonstration you can run locally to explore concepts and verify behavior. These demos are intended to supplement study and provide tangible examples for exam preparation.

Prerequisites
- An active Azure account and subscription (required to run demos that call Azure services).
- Python 3.8 or newer installed.
- `pip` available for installing Python dependencies.
- (Optional) Azure CLI installed for authentication: `az login`.

Quick setup
1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1  # PowerShell
```

2. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r src/requirements.txt
```

3. Authenticate to Azure (if you will use Azure services):

```powershell
az login
# optionally: az account set --subscription <your-subscription-id>
```

Running demos
- After installing dependencies and authenticating, run the included Python demo scripts to see the practical examples in action. Each demo prints output and usage notes to the console.

Notes
- Some demos require Azure service credentials or configuration (e.g., service principal, resource keys, or environment variables). Set the credentials in env file wherever needed.
- This repository is intended for learning and exam practice. Use it as a hands-on supplement to course material.

Contributing
- Feel free to open issues or submit pull requests with improvements, clarifications, or additional demo code.