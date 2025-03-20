import pandas as pd
from validate_employee_data import validate_employee_data
import logging

# ロギングの設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("invalid_data_test")


def test_invalid_data():
    """
    異なる種類の無効なデータをテストする関数
    """
    # テストケース1: 型エラー（年齢が文字列）
    logger.info("テストケース1: 型エラー（年齢が文字列）")
    data1 = {
        "employee_id": [1001, 1002],
        "name": ["山田太郎", "佐藤花子"],
        "age": [28, "三十四"],  # 文字列の年齢
        "department": ["IT", "HR"],
        "salary": [350000, 420000],
        "join_date": ["2019-04-01", "2015-09-15"],
        "manager_id": [None, 1003],
        "performance_score": [4.2, 3.8],
    }
    df1 = pd.DataFrame(data1)
    df1["join_date"] = pd.to_datetime(df1["join_date"])
    success1, _, error1 = validate_employee_data(df1)
    print(f"検証結果: {'成功' if success1 else '失敗'}")
    if not success1:
        print(f"エラー: {error1}\n")

    # テストケース2: 値の範囲エラー（給与が基準未満）
    logger.info("テストケース2: 値の範囲エラー（給与が基準未満）")
    data2 = {
        "employee_id": [1001, 1002],
        "name": ["山田太郎", "佐藤花子"],
        "age": [28, 34],
        "department": ["IT", "HR"],
        "salary": [350000, 200000],  # 給与が基準（250000）未満
        "join_date": ["2019-04-01", "2015-09-15"],
        "manager_id": [None, 1003],
        "performance_score": [4.2, 3.8],
    }
    df2 = pd.DataFrame(data2)
    df2["join_date"] = pd.to_datetime(df2["join_date"])
    success2, _, error2 = validate_employee_data(df2)
    print(f"検証結果: {'成功' if success2 else '失敗'}")
    if not success2:
        print(f"エラー: {error2}\n")

    # テストケース3: 固有性エラー（社員IDが重複）
    logger.info("テストケース3: 固有性エラー（社員IDが重複）")
    data3 = {
        "employee_id": [1001, 1001],  # 重複したID
        "name": ["山田太郎", "佐藤花子"],
        "age": [28, 34],
        "department": ["IT", "HR"],
        "salary": [350000, 420000],
        "join_date": ["2019-04-01", "2015-09-15"],
        "manager_id": [None, 1003],
        "performance_score": [4.2, 3.8],
    }
    df3 = pd.DataFrame(data3)
    df3["join_date"] = pd.to_datetime(df3["join_date"])
    success3, _, error3 = validate_employee_data(df3)
    print(f"検証結果: {'成功' if success3 else '失敗'}")
    if not success3:
        print(f"エラー: {error3}\n")

    # テストケース4: データフレームレベルのエラー（部署平均給与が低い）
    logger.info("テストケース4: データフレームレベルのエラー（部署平均給与が低い）")
    data4 = {
        "employee_id": [1001, 1002, 1003],
        "name": ["山田太郎", "佐藤花子", "鈴木一郎"],
        "age": [28, 34, 42],
        "department": ["IT", "IT", "IT"],  # 全員同じ部署
        "salary": [250001, 250002, 250003],  # 平均給与が基準（300000）未満
        "join_date": ["2019-04-01", "2015-09-15", "2010-06-30"],
        "manager_id": [None, 1001, 1001],
        "performance_score": [4.2, 3.8, 4.5],
    }
    df4 = pd.DataFrame(data4)
    df4["join_date"] = pd.to_datetime(df4["join_date"])
    success4, _, error4 = validate_employee_data(df4)
    print(f"検証結果: {'成功' if success4 else '失敗'}")
    if not success4:
        print(f"エラー: {error4}\n")

    # テストケース5: 必須カラム欠落エラー
    logger.info("テストケース5: 必須カラム欠落エラー")
    data5 = {
        "employee_id": [1001, 1002],
        "name": ["山田太郎", "佐藤花子"],
        "age": [28, 34],
        "department": ["IT", "HR"],
        # salary カラムを省略
        "join_date": ["2019-04-01", "2015-09-15"],
        "manager_id": [None, 1003],
        "performance_score": [4.2, 3.8],
    }
    df5 = pd.DataFrame(data5)
    df5["join_date"] = pd.to_datetime(df5["join_date"])
    success5, _, error5 = validate_employee_data(df5)
    print(f"検証結果: {'成功' if success5 else '失敗'}")
    if not success5:
        print(f"エラー: {error5}")


if __name__ == "__main__":
    print("=== 無効なデータの検証テスト ===")
    test_invalid_data()
    print("\n全テストケースが完了しました。")
