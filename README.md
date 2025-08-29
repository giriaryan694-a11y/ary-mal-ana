# 🔒 ARY-MAL-ANA

AI-powered code analyzer that scans entire directories and detects malicious, suspicious, or safe files.
✨ Made with ❤️ by Aryan Giri

## 📌 Why ARY-MAL-ANA?

In today’s world, people often copy-paste or run random scripts from the internet without knowing what they actually do.
This is dangerous ⚠️ because such scripts may:

❌ Delete files or damage your system

❌ Steal sensitive information (passwords, tokens, configs)

❌ Connect to remote servers without permission

❌ Execute hidden backdoors

ARY-MAL-ANA solves this by using Google Gemini AI to:

Analyze the logic of the code

Explain what the script is doing

Assign a safety rating (✅ Safe / ⚠ Suspicious / ❌ Malicious)

This way, you know before you run any unknown script.

## ✨ Features

📂 Full-directory scanning – analyze every supported file in a folder.

🖥 Multi-language support – Python, Shell, Batch, VBS, PowerShell, C/C++, Java, JavaScript, PHP, Ruby, Go, and more.

🧠 AI-powered reasoning – Gemini explains why a file is safe, suspicious, or malicious.

⏱ Configurable time limit per request – prevents hanging on large/complex files.

📄 Custom report generation – export results in TXT, HTML, or both.

🎨 Fancy CLI – banner, colors, and status icons for better UX.

## 🚀 Installation
```
#Clone the repo :
 
git clone https://github.com/giriaryan694-a11y/ary-mal-ana.git
cd ary-mal-ana

# Install dependencies
pip install -r requirements.txt


Create a file called key.txt in the project folder and paste your Gemini API key inside.
```
## ⚡ Usage
```bash
python ary-mal-ana.py
```

The program will:

Ask for a folder to scan

Ask for a time limit per file (e.g., 2 seconds)

Ask for report type (txt, html, or both)

Generate a detailed report with analysis & reasoning

## 📄 Example Output
```bash
🔍 [1/3] Analyzing: test.py
✅ SAFE — test.py
Reason: Script only prints "Hello World" and has no malicious actions.

🔍 [2/3] Analyzing: keylogger.py
❌ MALICIOUS — keylogger.py
Reason: Captures keystrokes and sends them to remote server.

🔍 [3/3] Analyzing: obfuscated.js
⚠ SUSPICIOUS — obfuscated.js
Reason: Code is heavily obfuscated and difficult to verify safely.


Reports are saved as:

analysis_report.txt

analysis_report.html
```
## 🔮 Future Plans

Add real-time file monitoring (auto-scan when new scripts are downloaded).

Integrate threat intelligence feeds for known malicious patterns.

Provide risk scoring system instead of only labels.

## 🤝 Contributing

Pull requests and feature suggestions are welcome!
