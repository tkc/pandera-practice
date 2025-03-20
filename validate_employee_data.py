import pandas as pd
import pandera as pa
from employee_schema import create_employee_schema
import logging
import json

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("validation.log"), logging.StreamHandler()],
)
logger = logging.getLogger("employee_validator")


def validate_employee_data(df):
    """
    社員データのバリデーションを実行し、結果を返す関数

    Parameters:
    -----------
    df : pandas.DataFrame
        検証する社員データのデータフレーム

    Returns:
    --------
    tuple
        (検証結果のブール値, 検証済みデータフレームまたはNone, エラーメッセージまたはNone)
    """
    try:
        # スキーマの取得
        schema = create_employee_schema()

        # バリデーション実行
        validated_df = schema.validate(df)

        # 成功ログ
        logger.info(
            f"バリデーション成功: {len(validated_df)}件のレコードが検証されました"
        )

        # 部署ごとの人数集計
        dept_counts = validated_df.groupby("department").size()
        logger.info(f"部署別人数: {dept_counts.to_dict()}")

        # 成功結果を返す
        return (True, validated_df, None)

    except pa.errors.SchemaError as e:
        # スキーマエラー
        error_msg = str(e)
        logger.error(f"バリデーションエラー: {error_msg}")

        # 失敗結果を返す
        return (False, None, error_msg)

    except Exception as e:
        # その他の例外
        error_msg = f"予期しないエラーが発生しました: {str(e)}"
        logger.error(error_msg)

        # 失敗結果を返す
        return (False, None, error_msg)


def main():
    """
    メイン実行関数 - サンプルデータを作成して検証する
    """
    # サンプルデータの作成
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
        "manager_id": [None, 1003, 1005, 1002, 1003],
        "performance_score": [4.2, 3.8, 4.5, 3.2, 4.0],
    }

    df = pd.DataFrame(data)
    df["join_date"] = pd.to_datetime(df["join_date"])

    # バリデーション実行
    success, validated_df, error_msg = validate_employee_data(df)

    if success:
        print("検証成功！データは有効です。")
        print(f"レコード数: {len(validated_df)}")

        # 検証後のデータをCSVに保存
        validated_df.to_csv("validated_employees.csv", index=False)
        print("検証済みデータを 'validated_employees.csv' に保存しました")

        # データサマリーを表示
        print("\n=== データサマリー ===")
        print(f"平均年齢: {validated_df['age'].mean():.1f}歳")
        print(f"平均給与: {validated_df['salary'].mean():.0f}円")
        print(f"平均評価: {validated_df['performance_score'].mean():.2f}")
    else:
        print("検証失敗！データにエラーがあります。")
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


if __name__ == "__main__":
    main()
