"""社員データバリデーションのためのPanderaスキーマ定義。"""

import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema, Check


def create_employee_schema() -> DataFrameSchema:
    """社員データバリデーションのためのPanderaスキーマを作成する。

    Returns:
        DataFrameSchema: 社員データ検証用のPanderaスキーマ

    Notes:
        以下のバリデーションを実装:
        - 社員ID: 1000以上の整数で一意
        - 名前: 2～20文字の文字列
        - 年齢: 18～65歳の整数
        - 部署: 許可されたリスト内の値
        - 給与: 25万円以上の整数
        - 入社日: 2000年以降の日付
        - 上司ID: NULL or 自分自身でない社員ID
        - 評価スコア: 1.0～5.0の浮動小数点数
        - 部署平均給与: 30万円以上
        - 管理職の評価スコア: 3.5以上
    """
    return DataFrameSchema(
        {
            # 社員ID: 1000以上の整数で一意である必要がある
            "employee_id": Column(
                int,
                Check.greater_than_or_equal_to(1000),
                unique=True,
                nullable=False,
                description="社員ID（1000以上の一意の整数）",
            ),
            # 名前: 文字列で2〜20文字の長さ
            "name": Column(
                str,
                Check.str_length(min_value=2, max_value=20),
                nullable=False,
                description="社員名（2-20文字）",
            ),
            # 年齢: 18〜65歳の整数
            "age": Column(
                int,
                Check.in_range(18, 65),
                nullable=False,
                description="年齢（18-65歳）",
            ),
            # 部署: 許可されたリストの中の値
            "department": Column(
                str,
                Check.isin(["IT", "HR", "Finance", "Marketing", "Sales", "R&D"]),
                nullable=False,
                description="部署名",
            ),
            # 給与: 250000以上の数値
            "salary": Column(
                int,
                Check.greater_than_or_equal_to(250000),
                nullable=False,
                description="月給（円）",
            ),
            # 入社日: 日付型、2000年以降の日付
            "join_date": Column(
                pd.DatetimeDtype(),
                Check(
                    lambda x: x >= pd.Timestamp("2000-01-01"),
                    error="入社日は2000年1月1日以降である必要があります",
                ),
                nullable=False,
                description="入社日",
            ),
            # 上司のID: NULLまたは自分自身のIDではない社員ID
            "manager_id": Column(
                int,
                # 上司IDがNULLでなければ、自分自身のIDと異なること
                Check(
                    lambda x, df: pd.isna(x) | (x != df["employee_id"]),
                    element_wise=True,
                    error="上司IDは自分自身のIDと異なる必要があります",
                ),
                nullable=True,
                description="上司の社員ID",
            ),
            # 評価スコア: 1.0〜5.0の範囲の浮動小数点数
            "performance_score": Column(
                float,
                Check.in_range(1.0, 5.0),
                nullable=False,
                description="業績評価スコア（1.0-5.0）",
            ),
        },
        # カスタムデータフレームレベルのチェック
        checks=[
            # 各部署の平均給与が300000円以上であることを確認
            Check(
                lambda df: df.groupby("department")["salary"].mean() >= 300000,
                error="各部署の平均給与は300000円以上である必要があります",
            ),
            # 管理職（他の人の上司になっている人）の評価スコアが3.5以上であることを確認
            Check(
                lambda df: df[df["employee_id"].isin(df["manager_id"].dropna())][
                    "performance_score"
                ].min()
                >= 3.5,
                error="管理職の評価スコアは3.5以上である必要があります",
            ),
        ],
        # スキーマの名前と説明
        name="社員情報スキーマ",
        description="会社社員の基本情報と業績に関するデータスキーマ",
    )
