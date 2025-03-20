# Pandera Practice

このプロジェクトは、Panderaを使用したデータバリデーションの実装例を示すデモプロジェクトです。

## プロジェクト構成

```
pandera-validation-demo/
├── pyproject.toml        # Poetry設定ファイル
├── README.md             # プロジェクト説明
├── pandera_validation/   # ソースコード
│   ├── __init__.py
│   ├── schemas/          # Panderaスキーマ定義
│   │   ├── __init__.py
│   │   └── employee.py
│   └── utils/            # ユーティリティ関数
│       ├── __init__.py
│       └── validation.py
└── tests/                # テストコード
    ├── __init__.py
    ├── conftest.py       # テスト共通フィクスチャ
    └── test_employee_validation.py
```

## セットアップ

Poetryを使用して環境をセットアップします：

```bash
# Poetryをインストール（まだの場合）
curl -sSL https://install.python-poetry.org | python3 -

# 依存関係をインストール
poetry install
```

## テストの実行

```bash
# すべてのテストを実行
poetry run pytest

# カバレッジレポート付きでテストを実行
poetry run pytest --cov=pandera_validation

# 詳細なテスト結果を表示
poetry run pytest -v
```

## 機能説明

このデモでは、Panderaを使用して従業員データの以下のバリデーションを行っています：

- データ型の検証
- 値の範囲チェック
- 一意性の検証
- 列間関係の検証
- カスタムバリデーション関数
- データフレームレベルの検証

詳細はソースコードのドキュメントを参照してください。
