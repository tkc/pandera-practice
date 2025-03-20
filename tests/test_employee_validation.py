"""社員データバリデーションのテスト。"""

import pytest
import pandas as pd
import pandera as pa

from pandera_validation.schemas import create_employee_schema
from pandera_validation.utils import validate_employee_data


class TestEmployeeSchema:
    """社員データスキーマのテストクラス。"""

    def test_valid_data(self, valid_employee_df):
        """正常なデータがバリデーションを通過することを確認。"""
        schema = create_employee_schema()
        # エラーが発生しなければテスト成功
        validated_df = schema.validate(valid_employee_df)
        assert len(validated_df) == len(valid_employee_df)

    def test_wrong_data_type(self, invalid_age_df):
        """年齢が文字列の場合、SchemaErrorが発生することを確認。"""
        schema = create_employee_schema()
        # SchemaErrorが発生することを期待
        with pytest.raises(pa.errors.SchemaError) as excinfo:
            schema.validate(invalid_age_df)

        # エラーメッセージに特定の文言が含まれているか確認
        assert "age" in str(excinfo.value)  # エラーメッセージにageカラムの記述があるか
        assert "int" in str(excinfo.value)  # データ型に関するエラーメッセージがあるか

    def test_value_range_error(self, invalid_salary_df):
        """給与が最低基準を下回る場合、SchemaErrorが発生することを確認。"""
        schema = create_employee_schema()
        # SchemaErrorが発生することを期待
        with pytest.raises(pa.errors.SchemaError) as excinfo:
            schema.validate(invalid_salary_df)

        # エラーメッセージに特定の文言が含まれているか確認
        assert "salary" in str(excinfo.value)
        assert "greater_than_or_equal_to" in str(excinfo.value) or "250000" in str(
            excinfo.value
        )

    def test_uniqueness_error(self, duplicate_id_df):
        """社員IDが重複する場合、SchemaErrorが発生することを確認。"""
        schema = create_employee_schema()
        # SchemaErrorが発生することを期待
        with pytest.raises(pa.errors.SchemaError) as excinfo:
            schema.validate(duplicate_id_df)

        # エラーメッセージに特定の文言が含まれているか確認
        assert "employee_id" in str(excinfo.value)
        assert "unique" in str(excinfo.value)

    def test_column_relationship_error(self, self_manager_df):
        """上司IDが自分自身の場合、SchemaErrorが発生することを確認。"""
        schema = create_employee_schema()
        # SchemaErrorが発生することを期待
        with pytest.raises(pa.errors.SchemaError) as excinfo:
            schema.validate(self_manager_df)

        # エラーメッセージに特定の文言が含まれているか確認
        assert "manager_id" in str(excinfo.value)
        assert "上司ID" in str(excinfo.value) or "自分自身" in str(excinfo.value)

    def test_allowed_values_error(self, invalid_department_df):
        """存在しない部署名の場合、SchemaErrorが発生することを確認。"""
        schema = create_employee_schema()
        # SchemaErrorが発生することを期待
        with pytest.raises(pa.errors.SchemaError) as excinfo:
            schema.validate(invalid_department_df)

        # エラーメッセージに特定の文言が含まれているか確認
        assert "department" in str(excinfo.value)
        assert "isin" in str(excinfo.value) or "Legal" in str(excinfo.value)

    def test_dataframe_check_error(self, low_avg_salary_df):
        """部署の平均給与が基準を下回る場合、SchemaErrorが発生することを確認。"""
        schema = create_employee_schema()
        # SchemaErrorが発生することを期待
        with pytest.raises(pa.errors.SchemaError) as excinfo:
            schema.validate(low_avg_salary_df)

        # エラーメッセージに特定の文言が含まれているか確認
        assert "平均給与" in str(excinfo.value) or "300000" in str(excinfo.value)

    def test_manager_score_error(self, low_manager_score_df):
        """管理職の評価スコアが基準未満の場合、SchemaErrorが発生することを確認。"""
        schema = create_employee_schema()
        # SchemaErrorが発生することを期待
        with pytest.raises(pa.errors.SchemaError) as excinfo:
            schema.validate(low_manager_score_df)

        # エラーメッセージに特定の文言が含まれているか確認
        assert "管理職" in str(excinfo.value) or "評価スコア" in str(excinfo.value)

    def test_date_range_error(self, early_join_date_df):
        """入社日が許容範囲外の場合、SchemaErrorが発生することを確認。"""
        schema = create_employee_schema()
        # SchemaErrorが発生することを期待
        with pytest.raises(pa.errors.SchemaError) as excinfo:
            schema.validate(early_join_date_df)

        # エラーメッセージに特定の文言が含まれているか確認
        assert "join_date" in str(excinfo.value) or "入社日" in str(excinfo.value)
        assert "2000" in str(excinfo.value)

    def test_missing_column_error(self, missing_column_df):
        """必須カラムが欠落している場合、SchemaErrorが発生することを確認。"""
        schema = create_employee_schema()
        # SchemaErrorが発生することを期待
        with pytest.raises(pa.errors.SchemaError) as excinfo:
            schema.validate(missing_column_df)

        # エラーメッセージに特定の文言が含まれているか確認
        assert "salary" in str(excinfo.value)


class TestEmployeeValidation:
    """社員データバリデーション関数のテストクラス。"""

    def test_validation_success(self, valid_employee_df):
        """正常なデータの場合、バリデーションが成功することを確認。"""
        success, validated_df, error_msg, summary = validate_employee_data(
            valid_employee_df
        )

        assert success is True
        assert validated_df is not None
        assert error_msg is None
        assert summary is not None
        assert summary["record_count"] == len(valid_employee_df)
        assert "avg_salary" in summary

    def test_validation_failure(self, invalid_salary_df):
        """無効なデータの場合、バリデーションが失敗することを確認。"""
        success, validated_df, error_msg, summary = validate_employee_data(
            invalid_salary_df
        )

        assert success is False
        assert validated_df is None
        assert error_msg is not None
        assert "salary" in error_msg
        assert summary is None

    @pytest.mark.parametrize(
        "age,should_pass",
        [
            (18, True),  # 最小許容年齢
            (65, True),  # 最大許容年齢
            (17, False),  # 許容範囲未満
            (66, False),  # 許容範囲超過
            (40, True),  # 通常値
        ],
    )
    def test_age_validation(self, valid_employee_df, age, should_pass):
        """様々な年齢値に対するバリデーションをテスト。"""
        df = valid_employee_df.copy()
        df.at[0, "age"] = age

        success, validated_df, error_msg, _ = validate_employee_data(df)

        if should_pass:
            assert success is True
            assert validated_df is not None
            assert validated_df.at[0, "age"] == age
        else:
            assert success is False
            assert "age" in error_msg

    @pytest.mark.parametrize(
        "score,should_pass",
        [
            (1.0, True),  # 最小許容値
            (5.0, True),  # 最大許容値
            (0.9, False),  # 許容範囲未満
            (5.1, False),  # 許容範囲超過
            (3.5, True),  # 通常値
        ],
    )
    def test_performance_score_validation(self, valid_employee_df, score, should_pass):
        """様々な評価スコアに対するバリデーションをテスト。"""
        df = valid_employee_df.copy()
        df.at[0, "performance_score"] = score

        success, validated_df, error_msg, _ = validate_employee_data(df)

        if should_pass:
            assert success is True
            assert validated_df is not None
            assert validated_df.at[0, "performance_score"] == score
        else:
            assert success is False
            assert "performance_score" in error_msg

    def test_exception_handling(self, valid_employee_df, monkeypatch):
        """予期せぬ例外が適切に処理されることを確認。"""

        # モック関数でスキーマ作成時に例外を発生させる
        def mock_create_schema():
            raise RuntimeError("テスト用の予期せぬエラー")

        # create_employee_schema関数をモックに置き換え
        monkeypatch.setattr(
            "pandera_validation.utils.validation.create_employee_schema",
            mock_create_schema,
        )

        # バリデーション実行
        success, validated_df, error_msg, summary = validate_employee_data(
            valid_employee_df
        )

        # 結果の検証
        assert success is False
        assert validated_df is None
        assert "予期しないエラー" in error_msg
        assert "テスト用の予期せぬエラー" in error_msg
        assert summary is None
