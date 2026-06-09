# 💰 Expense Tracker CLI

A clean, modern Command Line Expense Tracker built with Python.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features
- Add expenses with category & description
- List & filter expenses
- Monthly & All-time summary
- Delete expenses
- Export to CSV
- Beautiful terminal UI

## 🚀 Installation & Usage

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
pip install -e .

# Usage Examples:
expense add 15.50 --cat Food --desc "Lunch"
expense list
expense summary
expense export
