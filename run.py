import os
import sys
import subprocess
import webbrowser
import time
import socket

def is_port_open(host="127.0.0.1", port=8000):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except (OSError, ConnectionRefusedError):
        return False

def run_project():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")
    dist_dir = os.path.join(frontend_dir, "dist")
    db_file = os.path.join(backend_dir, "vocational.db")

    print("==================================================================")
    print("      VOCATIONAL ELECTIVE EXPLORER — UNIFIED LAUNCHER")
    print("==================================================================")

    # 1. Seed database if not existing
    if not os.path.exists(db_file):
        print("\n[1/3] Initializing and seeding SQLite Database...")
        subprocess.run([sys.executable, os.path.join(backend_dir, "seed_database.py")], check=True)
    else:
        print("\n[1/3] SQLite Database ready.")

    # 2. Build frontend dist if not existing
    if not os.path.exists(dist_dir) or not os.path.exists(os.path.join(dist_dir, "index.html")):
        print("\n[2/3] Building frontend bundle...")
        subprocess.run(["npm", "run", "build"], cwd=frontend_dir, shell=True, check=True)
    else:
        print("\n[2/3] Frontend build bundle ready.")

    print("\n[3/3] Starting server on http://127.0.0.1:8000 ...")

    # Background thread: Wait until server is listening on port 8000 before opening browser
    def open_browser_when_ready():
        print("Waiting for server socket connection...")
        for _ in range(30):
            if is_port_open("127.0.0.1", 8000):
                print("Server is live! Opening browser at http://127.0.0.1:8000")
                time.sleep(0.5)
                webbrowser.open("http://127.0.0.1:8000")
                return
            time.sleep(0.5)

    import threading
    threading.Thread(target=open_browser_when_ready, daemon=True).start()

    # Launch Uvicorn server bound to 127.0.0.1:8000
    try:
        import uvicorn
        # Ensure backend is in sys.path
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True, app_dir=backend_dir)
    except KeyboardInterrupt:
        print("\nServer stopped. Goodbye!")
    except Exception as e:
        print(f"\nError running server: {e}")
        # Fallback to subprocess
        subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"], cwd=backend_dir)

if __name__ == "__main__":
    run_project()
