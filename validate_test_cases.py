import pandas as pd
from validate_employee_data import validate_employee_data
import logging

# ロギングの設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("validation_test")


def run_test(test_name, description, dataframe):
    """テストケースを実行して結果を表示する関数"""
    print(f"\n===== テストケース: {test_name} =====")
    print(f"説明: {description}")
    print("テストデータ:")
    print(dataframe)

    # バリデーション実行
    success, validated_df, error_msg = validate_employee_data(dataframe)

    print(f"\n結果: {'成功 ✓' if success else '失敗 ✗'}")
    if success:
        print("バリデーションに合格しました。データは有効です。")
    else:
        print(f"エラー内容: {error_msg}")

    print("=" * 50)
    return success


# テストケース1: 正常なデータ
def test_valid_data():
    """正常なデータを検証するテスト"""
    description = """
    全ての条件を満たす正常なデータ。
    - 社員IDは一意である
    - 名前は2～20文字の文字列
    - 年齢は18～65歳の整数
    - 部署は許可リスト内の値
    - 給与は25万円以上
    - 入社日は2000年以降
    - 上司IDは自分自身でない
    - 評価スコアは1.0～5.0の範囲内
    - 部署平均給与は30万円以上
    - 管理職の評価スコアは3.5以上
    """
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

    return run_test("正常データ", description, df)


# テストケース2: データ型エラー
def test_wrong_data_type():
    """データ型が誤っているケースのテスト"""
    description = """
    年齢が文字列になっているデータ。
    Panderaのカラム型バリデーションでエラーとなる。
    """
    data = {
        "employee_id": [1001, 1002],
        "name": ["山田太郎", "佐藤花子"],
        "age": [28, "三十四"],  # 年齢が文字列
        "department": ["IT", "HR"],
        "salary": [350000, 420000],
        "join_date": ["2019-04-01", "2015-09-15"],
        "manager_id": [None, 1003],
        "performance_score": [4.2, 3.8],
    }
    df = pd.DataFrame(data)
    df["join_date"] = pd.to_datetime(df["join_date"])

    return run_test("データ型エラー", description, df)


# テストケース3: 値の範囲エラー
def test_value_range_error():
    """値が許容範囲外のケースのテスト"""
    description = """
    給与が最低基準（25万円）を下回っているデータ。
    Panderaの値チェック（greater_than_or_equal_to）でエラーとなる。
    """
    data = {
        "employee_id": [1001, 1002],
        "name": ["山田太郎", "佐藤花子"],
        "age": [28, 34],
        "department": ["IT", "HR"],
        "salary": [350000, 200000],  # 給与が基準未満
        "join_date": ["2019-04-01", "2015-09-15"],
        "manager_id": [None, 1003],
        "performance_score": [4.2, 3.8],
    }
    df = pd.DataFrame(data)
    df["join_date"] = pd.to_datetime(df["join_date"])

    return run_test("値の範囲エラー", description, df)


# テストケース4: 一意性制約エラー
def test_uniqueness_error():
    """一意性制約に違反するケースのテスト"""
    description = """
    社員IDが重複しているデータ。
    Panderaの一意性チェック（unique=True）でエラーとなる。
    """
    data = {
        "employee_id": [1001, 1001],  # 社員IDが重複
        "name": ["山田太郎", "佐藤花子"],
        "age": [28, 34],
        "department": ["IT", "HR"],
        "salary": [350000, 420000],
        "join_date": ["2019-04-01", "2015-09-15"],
        "manager_id": [None, 1003],
        "performance_score": [4.2, 3.8],
    }
    df = pd.DataFrame(data)
    df["join_date"] = pd.to_datetime(df["join_date"])

    return run_test("一意性制約エラー", description, df)


# テストケース5: 列間の関係エラー
def test_column_relationship_error():
    """列間の関係性に違反するケースのテスト"""
    description = """
    上司IDが自分自身になっているデータ。
    Panderaのカスタム要素単位チェック（Check with element_wise=True）
    でエラーとなる。
    """
    data = {
        "employee_id": [1001, 1002],
        "name": ["山田太郎", "佐藤花子"],
        "age": [28, 34],
        "department": ["IT", "HR"],
        "salary": [350000, 420000],
        "join_date": ["2019-04-01", "2015-09-15"],
        "manager_id": [None, 1002],  # 社員IDと同じ値（自分が自分の上司）
        "performance_score": [4.2, 3.8],
    }
    df = pd.DataFrame(data)
    df["join_date"] = pd.to_datetime(df["join_date"])

    return run_test("列間の関係エラー", description, df)


# テストケース6: 許容値リストエラー
def test_allowed_values_error():
    """許容値リストに違反するケースのテスト"""
    description = """
    存在しない部署名が含まれているデータ。
    Panderaの値リストチェック（Check.isin）でエラーとなる。
    """
    data = {
        "employee_id": [1001, 1002],
        "name": ["山田太郎", "佐藤花子"],
        "age": [28, 34],
        "department": ["IT", "Legal"],  # 許可リストにない部署
        "salary": [350000, 420000],
        "join_date": ["2019-04-01", "2015-09-15"],
        "manager_id": [None, 1003],
        "performance_score": [4.2, 3.8],
    }
    df = pd.DataFrame(data)
    df["join_date"] = pd.to_datetime(df["join_date"])

    return run_test("許容値リストエラー", description, df)


# テストケース7: データフレームレベルのチェックエラー
def test_dataframe_check_error():
    """データフレームレベルの条件に違反するケースのテスト"""
    description = """
    部署の平均給与が基準（30万円）を下回っているデータ。
    Panderaのデータフレームレベルチェックでエラーとなる。
    """
    data = {
        "employee_id": [1001, 1002, 1003],
        "name": ["山田太郎", "佐藤花子", "鈴木一郎"],
        "age": [28, 34, 42],
        "department": ["IT", "IT", "IT"],  # 全員同じ部署
        "salary": [250001, 250002, 250003],  # 平均給与が基準未満
        "join_date": ["2019-04-01", "2015-09-15", "2010-06-30"],
        "manager_id": [None, 1001, 1001],
        "performance_score": [4.2, 3.8, 4.5],
    }
    df = pd.DataFrame(data)
    df["join_date"] = pd.to_datetime(df["join_date"])

    return run_test("データフレームレベルのチェックエラー", description, df)


# テストケース8: 必須カラム欠落エラー
def test_missing_column_error():
    """必須カラムが欠落しているケースのテスト"""
    description = """
    必須カラム（給与）が欠落しているデータ。
    Panderaのスキーマ検証でエラーとなる。
    """
    data = {
        "employee_id": [1001, 1002],
        "name": ["山田太郎", "佐藤花子"],
        "age": [28, 34],
        "department": ["IT", "HR"],
        # salary カラムを省略
        "join_date": ["2019-04-01", "2015-09-15"],
        "manager_id": [None, 1003],
        "performance_score": [4.2, 3.8],
    }
    df = pd.DataFrame(data)
    df["join_date"] = pd.to_datetime(df["join_date"])

    return run_test("必須カラム欠落エラー", description, df)


# テストケース9: 管理職の評価スコアチェック
def test_manager_score_error():
    """管理職の評価スコアが基準未満のケースのテスト"""
    description = """
    管理職（他の社員の上司）の評価スコアが基準（3.5）を下回るデータ。
    Panderaのデータフレームレベルのカスタムチェックでエラーとなる。
    """
    data = {
        "employee_id": [1001, 1002, 1003, 1004],
        "name": ["山田太郎", "佐藤花子", "鈴木一郎", "田中美香"],
        "age": [28, 34, 42, 23],
        "department": ["IT", "HR", "Finance", "Marketing"],
        "salary": [350000, 420000, 580000, 310000],
        "join_date": ["2019-04-01", "2015-09-15", "2010-06-30", "2022-01-10"],
        "manager_id": [None, 1003, None, 1003],
        "performance_score": [4.2, 3.8, 3.3, 3.2],  # 社員ID=1003の評価が3.5未満
    }
    df = pd.DataFrame(data)
    df["join_date"] = pd.to_datetime(df["join_date"])

    return run_test("管理職の評価スコアエラー", description, df)


# テストケース10: 日付範囲エラー
def test_date_range_error():
    """日付が許容範囲外のケースのテスト"""
    description = """
    入社日が基準日（2000年1月1日）より前のデータ。
    Panderaのカスタム日付チェックでエラーとなる。
    """
    data = {
        "employee_id": [1001, 1002],
        "name": ["山田太郎", "佐藤花子"],
        "age": [28, 34],
        "department": ["IT", "HR"],
        "salary": [350000, 420000],
        "join_date": ["2019-04-01", "1999-09-15"],  # 2000年以前の日付
        "manager_id": [None, 1003],
        "performance_score": [4.2, 3.8],
    }
    df = pd.DataFrame(data)
    df["join_date"] = pd.to_datetime(df["join_date"])

    return run_test("日付範囲エラー", description, df)


def main():
    """全テストケースを実行"""
    print("===== Panderaバリデーションテスト =====")

    tests = [
        ("テスト1: 正常データ", test_valid_data),
        ("テスト2: データ型エラー", test_wrong_data_type),
        ("テスト3: 値の範囲エラー", test_value_range_error),
        ("テスト4: 一意性制約エラー", test_uniqueness_error),
        ("テスト5: 列間の関係エラー", test_column_relationship_error),
        ("テスト6: 許容値リストエラー", test_allowed_values_error),
        ("テスト7: データフレーム全体チェックエラー", test_dataframe_check_error),
        ("テスト8: 必須カラム欠落エラー", test_missing_column_error),
        ("テスト9: 管理職の評価スコアエラー", test_manager_score_error),
        ("テスト10: 日付範囲エラー", test_date_range_error),
    ]

    # 各テストの結果を記録
    results = []
    for test_name, test_func in tests:
        print(f"\n実行中: {test_name}")
        success = test_func()
        results.append((test_name, "成功" if success else "失敗"))

    # 結果サマリーを表示
    print("\n===== テスト結果サマリー =====")
    for test_name, result in results:
        status_symbol = "✓" if result == "成功" else "✗"
        print(f"{test_name}: {result} {status_symbol}")

    # 成功率を計算
    success_count = sum(1 for _, result in results if result == "成功")
    print(
        f"\n成功率: {success_count}/{len(results)} ({success_count / len(results) * 100:.1f}%)"
    )
    print("\nテスト完了！")


if __name__ == "__main__":
    main()
