"""データバリデーション実行のためのユーティリティ関数。"""

import logging
from typing import Tuple, Optional, Dict, Any

import pandas as pd
import pandera as pa

from pandera_validation.schemas import create_employee_schema


# ロガーの設定
logger = logging.getLogger(__name__)


def validate_employee_data(
    df: pd.DataFrame,
) -> Tuple[bool, Optional[pd.DataFrame], Optional[str], Optional[Dict[str, Any]]]:
    """社員データのバリデーションを実行し、結果を返す関数。

    Args:
        df: 検証する社員データのデータフレーム

    Returns:
        Tuple[bool, Optional[pd.DataFrame], Optional[str], Optional[Dict[str, Any]]]:
            - 検証結果のブール値
            - 検証済みデータフレームまたはNone
            - エラーメッセージまたはNone
            - 検証結果のサマリー情報またはNone
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

        # 検証結果のサマリー情報を作成
        summary = {
            "record_count": len(validated_df),
            "departments": validated_df["department"].value_counts().to_dict(),
            "avg_age": validated_df["age"].mean(),
            "avg_salary": validated_df["salary"].mean(),
            "avg_score": validated_df["performance_score"].mean(),
        }

        # 部署ごとの人数集計
        dept_counts = validated_df.groupby("department").size()
        logger.info(f"部署別人数: {dept_counts.to_dict()}")

        # 成功結果を返す
        return True, validated_df, None, summary

    except pa.errors.SchemaError as e:
        # スキーマエラー
        error_msg = str(e)
        logger.error(f"バリデーションエラー: {error_msg}")

        # 失敗結果を返す
        return False, None, error_msg, None

    except Exception as e:
        # その他の例外
        error_msg = f"予期しないエラーが発生しました: {str(e)}"
        logger.error(error_msg, exc_info=True)

        # 失敗結果を返す
        return False, None, error_msg, None
