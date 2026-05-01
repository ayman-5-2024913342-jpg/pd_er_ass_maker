# 🚀 Fortran Auto-Report Generator

An intelligent automation pipeline that clones Fortran repositories, compiles code, automatically generates missing input data using AI, and compiles everything into a professional Microsoft Word report.

## 🌟 Key Features

* **Repo Cloning**: Automatically pulls assignments from GitHub.
* **AI-Powered "Self-Healing"**: If a Fortran program fails to compile, the tool sends the error and code to **Groq (Llama 3.1)** to fix syntax errors in real-time.
* **Smart Input Generation**: 
    * Detects `OPEN(FILE=...)` statements and creates realistic data files.
    * Detects `READ(*,*)` (stdin) and generates appropriate user input via AI.
* **Syntax Highlighting**: Generates a `.docx` report with formatted, color-coded Fortran snippets using `Pygments`.
* **Execution Capture**: Runs the compiled binaries and captures the output for the final documentation.

---

## 🛠️ Requirements

### System Dependencies
* **gfortran**: Required to compile the Fortran source files.
* **Git**: Required for repository cloning.

### Python Libraries
```bash
pip install GitPython python-docx pygments groq
