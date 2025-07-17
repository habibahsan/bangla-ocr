import os
import subprocess
import sys
import shutil


def clean_previous_builds():
    """Remove previous build artifacts"""
    build_artifacts = ["build", "dist", "main.spec"]
    print("\nCleaning previous build artifacts...")
    for artifact in build_artifacts:
        if os.path.exists(artifact):
            if os.path.isdir(artifact):
                shutil.rmtree(artifact)
                print(f"Deleted directory: {artifact}")
            else:
                os.remove(artifact)
                print(f"Deleted file: {artifact}")
    print("Cleanup complete!\n")


def build_executable(clean_build=False):
    """Build the executable with PyInstaller"""
    if clean_build:
        clean_previous_builds()

    # Configuration - Update these paths as needed
    config = {
        "script": "main.py",
        "venv_site_packages": "venv/Lib/site-packages",
        "tesseract_path": "D:/code/bin/Tesseract-OCR",
        "bert_model_path": "./models/bert/bangla-bert",
        "output_type": "--onefile",  # or "--onedir"
        "windowed": "-w",          # remove for console application
        "additional_hidden_imports": ["transformers", "spacy.lang.bn"],
        "icon_path": "assets/icons/icon.ico"
    }

    # Generate PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--paths", config["venv_site_packages"],
        "--add-data", f"{config['tesseract_path']};Tesseract-OCR",
        "--add-data", f"{config['bert_model_path']};bangla-bert",
        "--collect-all", "bangla-ocr",
        config["output_type"],
        config["windowed"]
    ]

    # Add hidden imports if specified
    for imp in config["additional_hidden_imports"]:
        cmd.extend(["--hidden-import", imp])

    # Add icon if specified
    if config["icon_path"]:
        cmd.extend(["--icon", config["icon_path"]])

    # Add main script
    cmd.append(config["script"])

    # Print the command for verification
    print("\nBuilding with command:")
    print(" ".join(cmd))

    # Run the command
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild completed successfully!")
        print(f"Executable created in: {os.path.abspath('dist')}")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Build Bangla OCR executable')
    parser.add_argument('--clean', action='store_true',
                        help='Clean previous builds before building')
    args = parser.parse_args()

    print("Starting PyInstaller build process...")
    build_executable(clean_build=args.clean)
