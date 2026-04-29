import os
import subprocess
import logging
import re
import time
from git import Repo
from docx import Document
from docx.shared import Pt, RGBColor
from pygments import lexers, lex
from groq import Groq, RateLimitError # Added RateLimitError import

# --- Configuration ---
GROQ_API_KEY = "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" 
REPO_URL = "https://github.com/ayman-5-2024913342-jpg/Ass.git"
# Switch to the 8b model for higher token limits
MODEL_NAME = "llama-3.1-8b-instant" 
WORKING_DIR = "./fortran_workspace"
OUTPUT_DOC = "Assignments_Final_Report.docx"

client = Groq(api_key=GROQ_API_KEY)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def handle_inputs_and_files(code, folder_path):
    """Strictly follows the algorithm to create files and provide STDIN."""
    logger.info("  [Algorithm] Step 1: Checking for file requirements...")
    
    # SYSTEM PROMPT to force only raw data
    sys_msg = "You are a specialized Fortran automation tool. Return ONLY the requested data. No explanations, no conversation, no markdown blocks."

    # 1. File Dependency Check
    file_prompt = f"""Identify if this code reads from a file. 
    If yes, return FILENAME: <name> followed by CONTENT: <data>.
    If no, return NONE.
    CODE: {code}"""
    
    file_res = groq_call(file_prompt, system=sys_msg)
    
    created_file = "NONE"
    if "FILENAME:" in file_res.upper() and "CONTENT:" in file_res.upper():
        try:
            # More robust parsing to handle LLM fluff
            f_name = re.search(r"FILENAME:\s*(\S+)", file_res, re.IGNORECASE).group(1).strip()
            # Split by CONTENT: and take everything after
            f_cont = file_res.split("CONTENT:")[1].strip()
            # Remove markdown code blocks if the LLM ignored instructions
            f_cont = f_cont.replace("```fortran", "").replace("```", "").strip()
            
            with open(os.path.join(folder_path, f_name), 'w') as f:
                f.write(f_cont)
            created_file = f_name
            logger.info(f"  [Input] Created file: {f_name}")
        except Exception as e:
            logger.error(f"  [Input] Parsing error for file creation: {e}")

    # 2. STDIN Check
    logger.info("  [Algorithm] Step 2: Checking for STDIN requirements...")
    stdin_prompt = f"""Check if this code uses READ(*,*). 
    If yes, return ONLY the raw numeric or string values needed to run it. 
    If no, return NONE.
    CODE: {code}"""
    
    stdin_res = groq_call(stdin_prompt, system=sys_msg)
    
    # Clean up STDIN: If LLM gives a sentence, we try to take only the first line or return None
    if "NONE" in stdin_res.upper() or len(stdin_res) > 100: # Heuristic: if it's too long, it's a chat
        stdin_val = None
    else:
        # Strip any accidental markdown or quotes
        stdin_val = stdin_res.replace("`", "").strip()
    
    return stdin_val, created_file

def groq_call(prompt, system="You are a helpful assistant."):
    """Wrapper with System Message support and TPD protection."""
    time.sleep(1.5) # Basic RPM protection
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", # Higher TPD limit
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0 # Force deterministic output
        )
        return completion.choices[0].message.content.strip()
    except RateLimitError as e:
        # ... keep the same retry logic as before ...
        logger.warning("Rate limit hit, sleeping...")
        time.sleep(30)
        return groq_call(prompt, system)

def run_program(executable, stdin_val, folder_path):
    """Executes the program in its specific folder context."""
    try:
        # Run in the folder where the .f90 (and its generated .txt files) live
        res = subprocess.run(
            [executable],
            input=stdin_val,
            capture_output=True,
            text=True,
            timeout=5,
            cwd=folder_path  # CRITICAL: Ensures binary sees the .txt file
        )
        return res.stdout if res.stdout else res.stderr
    except Exception as e:
        return f"Execution Error: {str(e)}"

def add_highlighted_code(doc, code):
    """Applies CodeBlocks-style syntax highlighting."""
    table = doc.add_table(rows=1, cols=1)
    table.style = 'Table Grid'
    paragraph = table.rows[0].cells[0].paragraphs[0]
    lexer = lexers.get_lexer_by_name("fortran")
    token_colors = {
        'Keyword': RGBColor(0, 0, 255),
        'Comment': RGBColor(0, 128, 0),
        'String': RGBColor(163, 21, 21),
        'Number': RGBColor(128, 0, 128)
    }
    for ttype, value in lex(code, lexer):
        run = paragraph.add_run(value)
        run.font.name = 'Consolas'
        run.font.size = Pt(9)
        for key, rgb in token_colors.items():
            if key in str(ttype):
                run.font.color.rgb = rgb
                break

def main():
    if not os.path.exists(WORKING_DIR):
        Repo.clone_from(REPO_URL, WORKING_DIR)
    else:
        Repo(WORKING_DIR).remotes.origin.pull()
    
    doc = Document()
    doc.add_heading('Fortran Automation Report', 0)
    folders = sorted([d for d in os.listdir(WORKING_DIR) if d.startswith('Assignment')])

    for folder in folders:
        folder_path = os.path.abspath(os.path.join(WORKING_DIR, folder))
        doc.add_heading(folder, level=1)
        files = sorted([f for f in os.listdir(folder_path) if f.endswith('.f90')])

        for f90 in files:
            name = os.path.splitext(f90)[0]
            full_path = os.path.join(folder_path, f90)
            logger.info(f"Processing {name}...")

            with open(full_path, 'r') as f:
                code = f.read()

            # Compile
            exe = os.path.join(folder_path, f"{name}.out")
            compile_proc = subprocess.run(['gfortran', full_path, '-o', exe], capture_output=True, text=True)

            # Fix if needed
            if compile_proc.returncode != 0:
                logger.warning(f"  [Fix] {name} failed compilation. Fixing...")
                fix_prompt = f"Fix syntax errors in this Fortran code. Return ONLY code.\nCODE:\n{code}\nERROR:\n{compile_proc.stderr}"
                code = groq_call(fix_prompt)
                with open(full_path, 'w') as f: f.write(code)
                subprocess.run(['gfortran', full_path, '-o', exe])

            # Use Algorithm for Inputs/Files
            stdin_val, created_file = handle_inputs_and_files(code, folder_path)
            output = run_program(exe, stdin_val, folder_path)

            # Document
            doc.add_heading(name, level=2)
            add_highlighted_code(doc, code)
            doc.add_paragraph(f"STDIN Used: {stdin_val} | Files Created: {created_file}", style='Caption')
            out_run = doc.add_paragraph().add_run(f"Output:\n{output}")
            out_run.font.name = 'Consolas'
            
            if os.path.exists(exe): os.remove(exe)

    doc.save(OUTPUT_DOC)
    logger.info("Report complete.")

if __name__ == "__main__":
    main()
