#!/usr/bin/env python
"""Panderaバリデーションのサンプル実行スクリプト。"""

import json
import logging
import sys
from pathlib import Path

import pandas as pd

from pandera_validation.utils import validate_employee_data


# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("validation.log"), logging.StreamHandler()],
)
logger = logging.getLogger("sample_validation")


def load_sample_data(file_path=None):
    """サンプルデータをCSVから読み込むか、デフォルトデータを生成する。

    Args:
        file_path: 読み込むCSVファイルのパス（Noneの場合はデフォルトデータを生成）

    Returns:
        pd.DataFrame: 読み込んだ社員データ
    """
    if file_path and Path(file_path).exists():
        logger.info(f"CSVファイル {file_path} からデータを読み込みます")
        df = pd.read_csv(file_path)
        if "join_date" in df.columns:
            df["join_date"] = pd.to_datetime(df["join_date"])
        return df

    logger.info("デフォルトサンプルデータを生成します")
    data = {
        "employee_id": [1001, 1002, 1003, 1004, 1005],
        "name": ["山田太郎", "佐藤花子", "鈴木一郎", "田中美香", "伊藤健太"],
        "age": [28, 34, 42, 23, 31],
        "department": ["IT", "HR", "Finance", "Marketing", "IT"],
        "salary": [350000, 420000, 580000, 310000, 400000],
        "join_date": [
            "2019-04-01",
            "2015-09-15",
            "2010-06-30",
            "2022-01-10",
            "2017-11-05",
        ],
        "manager_id": [None, 1003, None, 1002, 1003],
        "performance_score": [4.2, 3.8, 4.5, 3.2, 4.0],
    }
    df = pd.DataFrame(data)
    df["join_date"] = pd.to_datetime(df["join_date"])
    return df


def main():
    """メインの実行関数。"""
    # コマンドライン引数からCSVファイルパスを取得（指定がなければNone）
    file_path = sys.argv[1] if len(sys.argv) > 1 else None

    # サンプルデータの読み込み
    employee_df = load_sample_data(file_path)

    # データの概要表示
    print("\n=== 検証対象データの概要 ===")
    print(f"レコード数: {len(employee_df)}")
    print(f"カラム: {', '.join(employee_df.columns)}")
    print("\nサンプル:")
    print(employee_df.head(2))

    # バリデーション実行
    print("\n=== バリデーション実行 ===")
    success, validated_df, error_msg, summary = validate_employee_data(employee_df)

    if success:
        print("✅ 検証成功！データは有効です。")
        print(f"レコード数: {summary['record_count']}")

        # 検証後のデータをCSVに保存
        validated_df.to_csv("validated_employees.csv", index=False)
        print("検証済みデータを 'validated_employees.csv' に保存しました")

        # データサマリーを表示
        print("\n=== データサマリー ===")
        print(f"平均年齢: {summary['avg_age']:.1f}歳")
        print(f"平均給与: {summary['avg_salary']:.0f}円")
        print(f"平均評価: {summary['avg_score']:.2f}")

        # サマリーを保存
        with open("validation_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print("サマリーデータを 'validation_summary.json' に保存しました")
    else:
        print("❌ 検証失敗！データにエラーがあります。")
        print(f"エラー内容: {error_msg}")

        # エラーログをJSONに保存
        with open("validation_errors.json", "w", encoding="utf-8") as f:
            json.dump(
                {"timestamp": pd.Timestamp.now().isoformat(), "error": error_msg},
                f,
                ensure_ascii=False,
                indent=2,
            )
        print("エラー詳細を 'validation_errors.json' に保存しました")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
