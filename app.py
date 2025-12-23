# app.py

from __future__ import annotations

from pathlib import Path

import streamlit as st

from core.questions import get_questions
from core.state import init_state
from ui.components import inject_css
from ui.screens import render_quiz_screen, render_result_screen


def _read_text(path: Path) -> str:
    # テキストを読み込む
    return path.read_text(encoding="utf-8")


def main() -> None:
    st.set_page_config(page_title="G検定 問題集", layout="wide")

    base = Path(__file__).parent
    css_path = base / "ui" / "styles.css"
    inject_css(_read_text(css_path))

    questions = get_questions()
    init_state(len(questions))

    mode = str(st.session_state.mode)

    if mode == "result":
        render_result_screen(questions)
    else:
        st.session_state.mode = "quiz"
        render_quiz_screen(questions)


if __name__ == "__main__":
    main()
