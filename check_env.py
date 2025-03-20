
import sys
import os
import subprocess

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"sys.path: {sys.path}")
print(f"Current working directory: {os.getcwd()}")
print(f"Contents of current directory: {os.listdir('.')}")

try:
    import pandera
    print(f"Pandera version: {pandera.__version__}")
except ImportError:
    print("Pandera is not installed")

try:
    import pandas
    print(f"Pandas version: {pandas.__version__}")
except ImportError:
    print("Pandas is not installed")

try:
    import pytest
    print(f"Pytest version: {pytest.__version__}")
except ImportError:
    print("Pytest is not installed")

# パッケージパスを確認
try:
    import pandera_validation
    print(f"pandera_validation path: {pandera_validation.__file__}")
except ImportError:
    print("pandera_validation module not found in path")

# テストを見つけられるかチェック
try:
    result = subprocess.run(
        ["poetry", "run", "python", "-m", "pytest", "--collect-only", "-v"],
        capture_output=True,
        text=True
    )
    print("\nPytest collection output:")
    print(result.stdout)
    if result.stderr:
        print("Pytest collection errors:")
        print(result.stderr)
except Exception as e:
    print(f"Error running pytest collection: {e}")
