"""pytestのための共通テストフィクスチャ。"""

import pytest
import pandas as pd


@pytest.fixture
def valid_employee_df():
    """テスト用の有効な社員データを生成するフィクスチャ。

    Returns:
        pd.DataFrame: 検証を通過する有効な社員データ
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
    return df


@pytest.fixture
def invalid_age_df(valid_employee_df):
    """年齢が無効な社員データを生成するフィクスチャ。"""
    df = valid_employee_df.copy()
    df.at[1, "age"] = "三十四"  # 年齢が文字列
    return df


@pytest.fixture
def invalid_salary_df(valid_employee_df):
    """給与が無効な社員データを生成するフィクスチャ。"""
    df = valid_employee_df.copy()
    df.at[1, "salary"] = 200000  # 給与が基準未満
    return df


@pytest.fixture
def duplicate_id_df(valid_employee_df):
    """社員IDが重複した社員データを生成するフィクスチャ。"""
    df = valid_employee_df.copy()
    df.at[1, "employee_id"] = 1001  # 社員IDを重複させる
    return df


@pytest.fixture
def self_manager_df(valid_employee_df):
    """上司IDが自分自身の社員データを生成するフィクスチャ。"""
    df = valid_employee_df.copy()
    df.at[1, "manager_id"] = 1002  # 上司IDを自分自身に設定
    return df


@pytest.fixture
def invalid_department_df(valid_employee_df):
    """存在しない部署名の社員データを生成するフィクスチャ。"""
    df = valid_employee_df.copy()
    df.at[1, "department"] = "Legal"  # 許可リストにない部署名
    return df


@pytest.fixture
def low_avg_salary_df():
    """部署の平均給与が基準未満の社員データを生成するフィクスチャ。"""
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
    return df


@pytest.fixture
def low_manager_score_df():
    """管理職の評価スコアが基準未満の社員データを生成するフィクスチャ。"""
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
    return df


@pytest.fixture
def early_join_date_df(valid_employee_df):
    """入社日が基準日より前の社員データを生成するフィクスチャ。"""
    df = valid_employee_df.copy()
    df.at[1, "join_date"] = pd.Timestamp("1999-09-15")  # 2000年以前の日付
    return df


@pytest.fixture
def missing_column_df():
    """必須カラムが欠落した社員データを生成するフィクスチャ。"""
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
    return df
