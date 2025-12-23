# core/questions.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Question:
    qid: str
    category: str
    difficulty: int
    qtype: str
    text: str
    options: list[str]
    answer_index: int
    explanation: str


def _validate_questions(questions: Iterable[Question]) -> list[Question]:
    # 問題セットの整合性を検証する
    qs = list(questions)

    if not qs:
        raise ValueError("questions is empty")

    seen: set[str] = set()
    for q in qs:
        if not q.qid:
            raise ValueError("qid is empty")
        if q.qid in seen:
            raise ValueError(f"duplicate qid: {q.qid}")
        seen.add(q.qid)

        if not q.category:
            raise ValueError(f"{q.qid}: category is empty")
        if not q.qtype:
            raise ValueError(f"{q.qid}: qtype is empty")
        if not q.text:
            raise ValueError(f"{q.qid}: text is empty")
        if not q.explanation:
            raise ValueError(f"{q.qid}: explanation is empty")

        if not isinstance(q.difficulty, int):
            raise ValueError(f"{q.qid}: difficulty must be int")
        if q.difficulty < 1 or q.difficulty > 5:
            raise ValueError(f"{q.qid}: difficulty must be 1..5")

        if not q.options or len(q.options) < 2:
            raise ValueError(f"{q.qid}: options must have >= 2 items")

        if not isinstance(q.answer_index, int):
            raise ValueError(f"{q.qid}: answer_index must be int")
        if q.answer_index < 0 or q.answer_index >= len(q.options):
            raise ValueError(f"{q.qid}: answer_index out of range")

    return qs


def get_questions() -> list[Question]:
    # 問題セットを返す
    questions = [
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
    return _validate_questions(questions)
