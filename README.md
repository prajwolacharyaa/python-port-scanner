# Note: change your IP address according to your need, I just use 127.0.0.1 
python3     	Runs the Python 3 interpreter
main.py     	Python script (the scanner program)
127.0.0.1    	Target IP address 
-s 1	        Start scanning from port 1
-e 100      	End scanning at port 100

# Professional Python Port Scanner

This project is a beginner-friendly Python port scanner for authorized cybersecurity learning and lab testing.

Use this project only on systems and networks you own or have permission to test.

## To Do in Kali Linux

### Step 1: Open Terminal

Open your Kali Linux terminal inside UTM.

### Step 2: Clone or copy the project

If the project is on GitHub, run:

```bash
git clone https://github.com/prajwolacharyaa/professional-python-port-scanner.git
cd professional-python-port-scanner
```

If you copied the project manually, go into the project folder with:

```bash
cd professional-python-port-scanner
```

### Step 3: Check Python

```bash
python3 --version
```

If Python is missing, install it:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

### Step 4: Check project files

```bash
ls
```

You should see:

- `README.md`
- `main.py`
- `requirements.txt`
- `port_scanner`
- `tests`

### Step 5: Create a virtual environment

```bash
python3 -m venv .venv
```

### Step 6: Activate the virtual environment

```bash
source .venv/bin/activate
```

### Step 7: Install requirements

```bash
pip install -r requirements.txt
```

### Step 8: Check syntax

```bash
python3 -m compileall main.py port_scanner tests
```

### Step 9: Run tests

```bash
python3 -m unittest discover -s tests -v
```

### Step 10: Run the scanner

```bash
python3 main.py 127.0.0.1 -s 1 -e 100
```

### Step 11: Save scan results

```bash
python3 main.py 127.0.0.1 -s 1 -e 100 -o scan_results/report.json
```

### Step 12: Check the saved file

```bash
cat scan_results/report.json
```

### Step 13: Test invalid input handling

```bash
python3 main.py 127.0.0.1 -s 100 -e 50
```

You should see a clean error message.

## To Do in Windows

### Step 1: Install Python

Download and install Python from [python.org](https://www.python.org/downloads/windows/).

Important:
- During installation, check `Add Python to PATH`

### Step 2: Download or clone the project

Option 1: Download ZIP from GitHub and extract it.

Option 2: Clone with Git:

```powershell
git clone https://github.com/prajwolacharyaa/professional-python-port-scanner.git
cd professional-python-port-scanner
```

### Step 3: Open Command Prompt or PowerShell

Go to the project folder:

```powershell
cd professional-python-port-scanner
```

### Step 4: Check Python

```powershell
python --version
```

If `python` does not work, try:

```powershell
python3 --version
```

### Step 5: Create a virtual environment

```powershell
python -m venv .venv
```

### Step 6: Activate the virtual environment

In PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

In Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### Step 7: Install requirements

```powershell
pip install -r requirements.txt
```

### Step 8: Check syntax

```powershell
python -m compileall main.py port_scanner tests
```

### Step 9: Run tests

```powershell
python -m unittest discover -s tests -v
```

### Step 10: Run the scanner

```powershell
python main.py 127.0.0.1 -s 1 -e 100
```

### Step 11: Save scan results

```powershell
python main.py 127.0.0.1 -s 1 -e 100 -o scan_results\report.json
```

### Step 12: Open the saved file

```powershell
type scan_results\report.json
```

## To Do in Mac

### Step 1: Open Terminal

Press `Command + Space`, type `Terminal`, and open it.

### Step 2: Go to the project folder

If you already have the project locally:

```bash
cd /Users/prajwolacharya/Documents/Codex/2026-05-07-create-a-complete-professional-github-ready
```

If you want to clone from GitHub:

```bash
git clone https://github.com/prajwolacharyaa/professional-python-port-scanner.git
cd professional-python-port-scanner
```

### Step 3: Check Python

```bash
python3 --version
```

### Step 4: Create a virtual environment

```bash
python3 -m venv .venv
```

### Step 5: Activate the virtual environment

```bash
source .venv/bin/activate
```

### Step 6: Install requirements

```bash
pip install -r requirements.txt
```

### Step 7: Check syntax

```bash
python3 -m compileall main.py port_scanner tests
```

### Step 8: Run tests

```bash
python3 -m unittest discover -s tests -v
```

### Step 9: Run the scanner

```bash
python3 main.py 127.0.0.1 -s 1 -e 100
```

### Step 10: Save scan results

```bash
python3 main.py 127.0.0.1 -s 1 -e 100 -o scan_results/report.json
```

### Step 11: Check the saved file

```bash
cat scan_results/report.json
```

## Quick Commands

### Kali Linux

```bash
python3 -m unittest discover -s tests -v
python3 main.py 127.0.0.1 -s 1 -e 100
python3 main.py 127.0.0.1 -s 1 -e 100 -o scan_results/report.json
```

### Windows

```powershell
python -m unittest discover -s tests -v
python main.py 127.0.0.1 -s 1 -e 100
python main.py 127.0.0.1 -s 1 -e 100 -o scan_results\report.json
```

### Mac

```bash
python3 -m unittest discover -s tests -v
python3 main.py 127.0.0.1 -s 1 -e 100
python3 main.py 127.0.0.1 -s 1 -e 100 -o scan_results/report.json
```
