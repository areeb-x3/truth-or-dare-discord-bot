# Built-In/Installed Modules 
from watchfiles import run_process, PythonFilter
import subprocess,sys

# -----------------------------------------------------------------------
# PURPOSE OF THIS FILE: 
# When any changes are made in py files. The
# Bot restarts with new implementations. Run bot_client.py directly to
# avoid restart the bot with every save.
# -----------------------------------------------------------------------

def run_bot():
    subprocess.run(
        [sys.executable, "bot_client.py"]
    )

if __name__ == "__main__":
    run_process(
        ".",
        target=run_bot,
        watch_filter=PythonFilter(),
        debounce=500
    )