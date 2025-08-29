import os
import google.generativeai as genai
from datetime import datetime
from html import escape
from colorama import init, Fore, Style
from termcolor import colored
import pyfiglet
import time

# ========== INIT ==========
init(autoreset=True)

# ========== BANNER ==========
def print_banner():
    banner = pyfiglet.figlet_format("ARY-MAL-ANA", font="slant")
    print(colored(banner, "cyan"))
    print(colored("🔒 Code Malware Analyzer powered by Gemini AI 🔒", "yellow"))
    print(colored("✨ Made with ❤️ by Aryan Giri ✨", "magenta", attrs=["bold"]))
    print(colored("="*70, "green"))

# ========== USER CONFIGURATION ==========
FILE_EXTENSIONS = [
    ".py", ".sh", ".bat", ".vbs", ".ps1",  # scripts
    ".c", ".cpp", ".h",                     # C/C++
    ".java",                                # Java
    ".js", ".ts",                            # JS/TS
    ".php",                                 # PHP
    ".rb",                                  # Ruby
    ".go"                                   # Go
    # Add more as needed
]

# ========== LOAD GEMINI API KEY ==========
KEY_FILE = "key.txt"
if not os.path.isfile(KEY_FILE):
    print(f"{Fore.RED}❌ Error: key.txt not found.")
    exit()
with open(KEY_FILE, "r") as kf:
    API_KEY = kf.read().strip()
if not API_KEY:
    print(f"{Fore.RED}❌ Error: key.txt is empty.")
    exit()

# ========== INIT GEMINI ==========
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# ========== BUILD PROMPT ==========
def build_prompt(filename, content):
    return (
        f"You are a malware analysis AI. Analyze the following script and classify it as:\n\n"
        f"✅ SAFE — If script is clean and does nothing harmful.\n"
        f"❌ MALICIOUS — If it performs dangerous operations (e.g., deletes files, connects to remote servers, steals data, etc.)\n"
        f"⚠ SUSPICIOUS — If obfuscated, unknown, or potentially risky.\n\n"
        f"Always explain **why**.\n\n"
        f"Respond in EXACTLY this format:\n"
        f"Label: [✅|❌|⚠]\n"
        f"Reason: [detailed reason why]\n\n"
        f"File: {filename}\n"
        f"Content:\n```\n{content}\n```"
    )

# ========== ANALYZE SCRIPT WITH TIMEOUT ==========
def analyze_script(file_path, timeout_sec):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        prompt = build_prompt(os.path.basename(file_path), content)

        start_time = time.time()
        response = model.generate_content(prompt)  # Gemini API call
        duration = time.time() - start_time

        if duration > timeout_sec:
            return f"Label: ⚠\nReason: Request exceeded time limit of {timeout_sec} sec."
        return response.text.strip()

    except Exception as e:
        return f"Label: ⚠\nReason: Failed to analyze due to error: {e}"

# ========== SCAN FOLDER ==========
def scan_folder(folder_path, timeout_sec):
    results = []
    files = [os.path.join(root, f) for root, _, fs in os.walk(folder_path) for f in fs if any(f.lower().endswith(ext) for ext in FILE_EXTENSIONS)]
    total_files = len(files)
    if total_files == 0:
        print(colored("⚠ No script files found.", "yellow"))
        return results

    for idx, full_path in enumerate(files, 1):
        print(colored(f"🔍 [{idx}/{total_files}] Analyzing: {full_path}", "cyan"))
        result = analyze_script(full_path, timeout_sec)
        if "Label: ✅" in result:
            print(colored(f"✅ SAFE — {os.path.basename(full_path)}", "green"))
        elif "Label: ❌" in result:
            print(colored(f"❌ MALICIOUS — {os.path.basename(full_path)}", "red"))
        else:
            print(colored(f"⚠ SUSPICIOUS — {os.path.basename(full_path)}", "yellow"))
        results.append((full_path, result))
    return results

# ========== SAVE TXT ==========
def save_txt_report(results, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Gemini Script Analysis Report — {datetime.now()}\n")
        f.write(f"Made with ❤️ by Aryan Giri\n\n")
        for file_path, result in results:
            f.write(f"File: {file_path}\n{result}\n{'-'*60}\n")
    print(colored(f"📄 TXT report saved to {filename}", "green"))

# ========== SAVE HTML ==========
def save_html_report(results, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Gemini Report</title>
<style>
body {{ font-family: Arial; background: #f0f2f5; padding: 20px; }}
.card {{ background: #fff; padding: 15px; margin-bottom: 15px; border-radius: 10px;
box-shadow: 0 0 12px rgba(0,0,0,0.15); }}
.safe {{ color: green; }}
.malicious {{ color: red; }}
.suspicious {{ color: orange; }}
h1 {{ text-align: center; color: #333; }}
.footer {{ text-align:center; margin-top:30px; font-size:14px; color:#555; }}
</style></head><body>
<h1>AR-MAL-ANA Script Analysis Report</h1>
<p style="text-align:center;">Generated on: {datetime.now()}</p>
""")
        for file_path, result in results:
            if "Label: ✅" in result:
                label, label_class = "✅", "safe"
            elif "Label: ❌" in result:
                label, label_class = "❌", "malicious"
            else:
                label, label_class = "⚠", "suspicious"
            reason = result.split("Reason:", 1)[-1].strip()
            f.write(f"""<div class="card">
<h2>{escape(file_path)}</h2>
<p class="{label_class}"><strong>Label:</strong> {label}</p>
<p><strong>Reason:</strong> {escape(reason)}</p>
</div>""")
        f.write(f"<div class='footer'>✨ Made with ❤️ by Aryan Giri ✨</div>")
        f.write("</body></html>")
    print(colored(f"🌐 HTML report saved to {filename}", "green"))

# ========== MAIN ==========
def main():
    print_banner()
    folder = input(colored("📁 Enter path to folder to scan: ", "magenta")).strip()
    if not os.path.isdir(folder):
        print(colored("❌ Folder does not exist.", "red"))
        return

    print(colored("\n⏱ You can set a time limit per Gemini request (recommended: 1-3 seconds).", "yellow"))
    print(colored("This prevents the program from hanging on large scripts or slow responses.", "yellow"))
    try:
        timeout_sec = float(input(colored("🕒 Enter time limit per file (in seconds): ", "magenta")).strip())
        if timeout_sec <= 0:
            raise ValueError
    except:
        timeout_sec = 2  # default
        print(colored(f"⚠ Invalid input. Defaulting to {timeout_sec} sec.", "yellow"))

    output_type = input(colored("📄 Choose report type (txt/html/both): ", "magenta")).strip().lower()
    if output_type not in ["txt", "html", "both"]:
        print(colored("⚠ Invalid choice. Defaulting to both.", "yellow"))
        output_type = "both"

    filename = input(colored("📝 Enter output filename (without extension): ", "magenta")).strip()
    if not filename:
        filename = "analysis_report"

    print(colored(f"\n🚀 Scanning folder: {folder}\n", "cyan", attrs=["bold"]))
    results = scan_folder(folder, timeout_sec)
    if not results:
        return

    if output_type in ["txt", "both"]:
        save_txt_report(results, f"{filename}.txt")
    if output_type in ["html", "both"]:
        save_html_report(results, f"{filename}.html")

    print(colored("\n🎉 All done! Reports generated successfully!", "green", attrs=["bold"]))
    print(colored("✨ Made with ❤️ by Aryan Giri ✨", "magenta", attrs=["bold"]))
    print(colored("="*70, "green"))

if __name__ == "__main__":
    main()
