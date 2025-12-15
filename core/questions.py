# core/questions.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Question:
    qid: str
    category: str
    difficulty: int
    qtype: str
    text: str
    options: List[str]
    answer_index: int
    explanation: str


def get_questions() -> List[Question]:
    # 問題セットを返す
    return [
        Question(
            qid="q1",
            category="AI基礎",
            difficulty=2,
            qtype="単一選択",
            text="教師あり学習の目的として最も適切なものはどれか。",
            options=[
                "ラベルのないデータから構造を発見する",
                "入力と正解ラベルの対応関係を学習し予測する",
                "報酬を最大化する行動方策を学習する",
                "データを暗号化して安全性を高める",
            ],
            answer_index=1,
            explanation="教師あり学習は、入力と正解ラベルのペアから対応関係を学習し、未知データのラベルを予測する。",
        ),
        Question(
            qid="q2",
            category="統計・評価",
            difficulty=3,
            qtype="単一選択",
            text="二値分類で、適合率（Precision）の定義として正しいものはどれか。",
            options=[
                "TP / (TP + FN)",
                "TP / (TP + FP)",
                "TN / (TN + FP)",
                "(TP + TN) / 全件",
            ],
            answer_index=1,
            explanation="適合率は『陽性と予測したもののうち、実際に陽性だった割合』で、TP/(TP+FP)。",
        ),
        Question(
            qid="q3",
            category="ディープラーニング",
            difficulty=2,
            qtype="単一選択",
            text="CNNが画像認識で強い理由として最も適切な説明はどれか。",
            options=[
                "画像を必ずベクトル化せずに処理できるため",
                "畳み込みで局所特徴を抽出し、重み共有でパラメータを削減できるため",
                "学習に教師データが不要であるため",
                "必ず説明可能性が高くなるため",
            ],
            answer_index=1,
            explanation="畳み込みと重み共有により局所特徴を効率よく扱い、パラメータ数も抑えられる。",
        ),
    ]
