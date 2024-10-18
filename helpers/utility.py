import subprocess
import threading

def run_command(command):
    """Execute a shell command."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return {"error": str(e)}

def threaded_function(target, *args):
    """Run a function in a new thread."""
    thread = threading.Thread(target=target, args=args)
    thread.start()
    return thread

