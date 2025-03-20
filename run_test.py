
import pytest
import sys

# pytestをプログラム的に実行し、結果を出力
exit_code = pytest.main(["-v"])
print(f"Pytest exit code: {exit_code}")
