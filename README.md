🏗️ Fortran Assignment Automation Tool

An intelligent automation pipeline that clones Fortran repositories, detects program dependencies using AI, compiles/executes code, and generates a comprehensive professional report in .docx format.

🌟 Key Features

GitHub Integration: Automatically clones and pulls the latest code from your specified repository.

AI-Driven Data Generation: Uses Llama 3.1 (8B) via Groq to analyze Fortran source code and generate:

Required STDIN (input values for READ(*,*)).

Necessary external data files (.txt, .dat) defined in OPEN statements.

Auto-Fix Logic: If a Fortran file fails to compile, the tool sends the error log back to the AI for a syntax fix and retries the compilation.

Visual Reporting: Generates a Word document with syntax highlighting (CodeBlocks style) and captured output blocks.

🛠️ Prerequisites

Before running the tool, ensure your environment meets the following requirements:

System Tools:

gfortran: The GNU Fortran compiler must be installed and accessible via command line.

Git: Installed and configured on your system.

Hardware:

Windows users are supported via built-in NTFS path-handling logic.

🚀 Getting Started

1. Installation

Clone this automation repository and install the Python dependencies:

git clone <this-automation-repo-url>
cd fortran-automation-tool
pip install -r requirements.txt


Note: If you don't have a requirements.txt, install manually: pip install groq GitPython python-docx pygments

2. Configuration

Open main.py and modify the Configuration section at the top:

# 1. Update your Repo URL
REPO_URL = "[https://github.com/your-profile/your-assignments-repo.git](https://github.com/your-profile/your-assignments-repo.git)"

# 2. Update your API Key
GROQ_API_KEY = "gsk_your_actual_key_here"


[!IMPORTANT]
API KEY SECURITY: The key currently in the script is for testing purposes only. It is highly recommended to create your own Groq API Key for personal use. Never commit your private key to a public repository.

3. Usage

Run the script:

python main.py


The tool will create a fortran_workspace directory, process all folders starting with the word "Assignment", and finally export Assignments_Final_Report.docx.

📂 Expected Repository Structure

For the tool to work correctly, your target GitHub repository should follow this structure:

Your-Repo/
├── Assignment 1/
│   ├── program1.f90
│   └── program2.f90
├── Assignment 2/
│   └── task1.f90
└── ...


🧪 How it Works (The Algorithm)

Clone: Cleanly clones the repository using flags to handle Windows-specific path errors.

Analysis: Scans .f90 files for READ and OPEN statements.

AI Generation: Requests the Groq LLM to provide exact raw data needed to satisfy the program's logic.

Compile: Executes gfortran. If it fails, it utilizes AI to "repair" the source code.

Execute: Runs the binary with the generated STDIN and local files.

Export: Aggregates code, inputs, and results into a formatted Word document.

📜 License

Distributed under the MIT License. See LICENSE for more information.

Developed for automatic academic reporting and Fortran code verification.
