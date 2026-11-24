import subprocess
import sys
from pathlib import Path


def main() -> None:
    app_path = Path(__file__).parent / "ui" / "app.py"
    # run streamlit
    subprocess.run(args=[sys.executable, "-m", "streamlit", "run", str(app_path)], check=True)



if __name__ == "__main__":
    main()