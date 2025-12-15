# app.py

from __future__ import annotations

from pathlib import Path

import streamlit as st

from core.questions import get_questions
from ui.components import (
    close_card,
    inject_css,
    open_card,
    render_progress,
    render_question_text,
    render_tags,
    render_topbar,
)


def _read_text(path: Path) -> str:
    # テキストを読み込む
    return path.read_text(encoding="utf-8")


def _init_state(total: int) -> None:
    # 状態を初期化する
    if "idx" not in st.session_state:
        st.session_state.idx = 0
    if "selected" not in st.session_state:
        st.session_state.selected = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "answered_count" not in st.session_state:
        st.session_state.answered_count = 0
    if "correct_count" not in st.session_state:
        st.session_state.correct_count = 0
    if "streak" not in st.session_state:
        st.session_state.streak = 0
    if "total" not in st.session_state:
        st.session_state.total = total


def _reset_run(total: int) -> None:
    # セッションをリセットする
    st.session_state.idx = 0
    st.session_state.selected = 0
    st.session_state.answered = False
    st.session_state.answered_count = 0
    st.session_state.correct_count = 0
    st.session_state.streak = 0
    st.session_state.total = total


def main() -> None:
    st.set_page_config(page_title="G検定 問題集", layout="wide")

    base = Path(__file__).parent
    inject_css(_read_text(base / "ui" / "styles.css"))

    questions = get_questions()
    _init_state(len(questions))

    idx = int(st.session_state.idx)
    total = len(questions)
    q = questions[idx]

    answered = int(st.session_state.answered_count)
    correct = int(st.session_state.correct_count)
    accuracy = int(round((correct / answered) * 100)) if answered else 0
    remaining = max(0, total - answered)

    render_topbar("G検定 問題集", "出題モード（単問）", "基礎")
    st.write("")

    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        open_card(f"問題 {idx + 1}", f"{q.category} / 難易度 {q.difficulty}", "単問")
        render_progress(idx + 1, total, accuracy)
        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        render_tags(q.category, q.difficulty, q.qtype)
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        render_question_text(q.text)
        close_card()

        st.write("")

        disabled = bool(st.session_state.answered)
        choice = st.radio(
            "選択肢",
            options=list(range(len(q.options))),
            format_func=lambda i: q.options[i],
            index=int(st.session_state.selected),
            disabled=disabled,
            label_visibility="collapsed",
        )

        if not disabled:
            st.session_state.selected = int(choice)

        c1, c2, c3 = st.columns([1, 1, 1.2])
        with c1:
            judge = st.button("判定する", type="primary", disabled=disabled, use_container_width=True)
        with c2:
            prev = st.button("前へ", disabled=(idx == 0), use_container_width=True)
        is_last = (idx == total - 1)
        next_label = "結果表示" if is_last else "次へ"
        with c3:
            next_ = st.button(next_label, disabled=is_last, use_container_width=True)

        if judge:
            st.session_state.answered = True
            st.session_state.answered_count += 1

            is_correct = (int(st.session_state.selected) == int(q.answer_index))
            if is_correct:
                st.session_state.correct_count += 1
                st.session_state.streak += 1
                st.success("正解")
            else:
                st.session_state.streak = 0
                st.error("不正解")
                st.info(f"正解：{q.options[q.answer_index]}")

        with st.expander("解説", expanded=False):
            st.write(q.explanation)

        if prev:
            st.session_state.idx = max(0, idx - 1)
            st.session_state.selected = 0
            st.session_state.answered = False
            st.rerun()

        if next_:
            st.session_state.idx = min(total - 1, idx + 1)
            st.session_state.selected = 0
            st.session_state.answered = False
            st.rerun()

    with right:
        open_card("学習状況", "最小限の指標だけ表示します", "&nbsp;")
        st.markdown(
            f"""
<div class="gx-statgrid">
  <div class="gx-stat"><small>回答</small><b>{answered}</b></div>
  <div class="gx-stat"><small>正解</small><b>{correct}</b></div>
  <div class="gx-stat"><small>連続正解</small><b>{int(st.session_state.streak)}</b></div>
  <div class="gx-stat"><small>残り</small><b>{remaining}</b></div>
</div>
""",
            unsafe_allow_html=True,
        )
        close_card()

        st.write("")

        open_card("操作", "まずは最小機能で運用します", "&nbsp;")
        if st.button("リセット", use_container_width=True):
            _reset_run(total)
            st.rerun()
        close_card()

    st.caption("MVP：出題 → 回答 → 正誤判定。UIはHTML版の構造と見た目に寄せています。")


if __name__ == "__main__":
    main()
