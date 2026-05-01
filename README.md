# 🚀 Pd er assignment Generator

An intelligent automation pipeline that clones Fortran repositories, compiles code, automatically generates missing input data using AI, and compiles everything into a Microsoft Word file.

## 🌟 Key Features

* **Repo Cloning**: Automatically pulls assignments from GitHub.
* **AI-Powered "Self-Healing"**: If a Fortran program fails to compile, the tool sends the error and code to **Groq (Llama 3.1)** to fix syntax errors in real-time.
* **Smart Input Generation**: 
    * Detects `OPEN(FILE=...)` statements and creates realistic data files.
    * Detects `READ(*,*)` (stdin) and generates appropriate user input via AI.
* **Syntax Highlighting**: Generates a `.docx` report with formatted, color-coded Fortran snippets using `Pygments`.
* **Execution Capture**: Runs the compiled binaries and captures the output for the final documentation.

---

## 🛠️ System Requirements

### 1. External Dependencies
* **Python**: [Download here](https://www.python.org/). **(IMPORTANT: Check the box "Add Python to PATH" during installation)**.
* **GFortran**: 
    * **Windows**: Install [MinGW-w64](https://www.mingw-w64.org/) (ensure `gfortran` is in your PATH).
    * **Mac**: Run `brew install gcc` in Terminal.
* **Git**: [Download here](https://git-scm.com/). (ensure `git` is in your PATH).

### 2. Python Libraries
Open your terminal or command prompt and run:
```bash
pip install GitPython python-docx pygments groq
```

### 3. Verify the requirements
Open terminal or command prompt and verify:
* **Python**: `python3 --vesrion`.
* **GFortran**: `gfortran --version`.
* **Git**: `git --version`.

### 4. Running:
Open main.py and change REPO_URL in line 15 with your own github repo.
The groq api key is for testing purposes only so you may want to create your api key from [groq_api](https://console.groq.com/)

## Note
This readme is mostly ai generated and im too lazy to verify it let alone write my own, lemme know if you have any issues
