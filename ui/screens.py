# ui/screens.py

from __future__ import annotations

import streamlit as st

from core.state import reset_run
from ui.components import (
    close_card,
    open_card,
    render_progress,
    render_question_text,
    render_tags,
    render_topbar,
)


def render_result_screen(questions: list) -> None:
    # 結果表示：最終回答ベース
    render_topbar("G検定 問題集", "結果表示", "基礎")
    st.write("")

    total_q = len(questions)

    final_wrong = []
    for item in st.session_state.wrong_log:
        q_index = item.get("q_index")
        if not isinstance(q_index, int):
            continue
        if not st.session_state.last_answer_map.get(q_index, False):
            final_wrong.append(item)

    final_wrong_map: dict[int, dict] = {}
    for item in final_wrong:
        q_index = item["q_index"]
        final_wrong_map[q_index] = item

    final_wrong_list = list(final_wrong_map.values())

    wrong = len(final_wrong_list)
    correct = total_q - wrong

    open_card("結果", "最終結果", "")
    st.markdown(
        f"""
<div class="gx-statgrid">
  <div class="gx-stat"><small>総問題数</small><b>{total_q}</b></div>
  <div class="gx-stat"><small>正解数</small><b>{correct}</b></div>
  <div class="gx-stat"><small>不正解数</small><b>{wrong}</b></div>
</div>
""",
        unsafe_allow_html=True,
    )
    close_card()

    st.write("")

    open_card("間違えた問題", "最終回答ベース", "")
    if wrong == 0:
        st.success("全問正解")
    else:
        for item in sorted(final_wrong_list, key=lambda x: x["q_index"]):
            with st.expander(f"問題 {item['q_index']}", expanded=False):
                st.write("問題文")
                st.write(item.get("question", ""))
                st.write("あなたの回答")
                st.write(item.get("selected", ""))
                st.write("正解")
                st.write(item.get("correct", ""))
                st.write("解説")
                st.write(item.get("explanation", ""))
    close_card()

    st.write("")

    if st.button("もう一度", type="primary", use_container_width=True):
        reset_run(total_q)
        st.session_state.mode = "quiz"
        st.rerun()


def render_quiz_screen(questions: list) -> None:
    # 出題画面
    idx = int(st.session_state.idx)
    total = len(questions)

    if total == 0:
        render_topbar("G検定 問題集", "出題モード（単問）", "基礎")
        st.error("問題がありません。")
        return

    if idx < 0:
        idx = 0
        st.session_state.idx = 0
    if idx >= total:
        idx = total - 1
        st.session_state.idx = idx

    q = questions[idx]

    answered_count = int(st.session_state.answered_count)
    correct_count = int(st.session_state.correct_count)
    accuracy = int(round((correct_count / answered_count) * 100)) if answered_count else 0

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
        initial_index = int(st.session_state.selected) if st.session_state.selected is not None else 0

        choice = st.radio(
            "選択肢",
            options=list(range(len(q.options))),
            format_func=lambda i: q.options[i],
            index=initial_index,
            disabled=disabled,
            label_visibility="collapsed",
        )

        if not disabled:
            st.session_state.selected = int(choice)

        def _on_judge() -> None:
            # 判定処理
            st.session_state.answered = True
            st.session_state.answered_count += 1

            q_no = idx + 1
            selected_idx = int(st.session_state.selected)
            is_correct = (selected_idx == int(q.answer_index))

            st.session_state.last_answer_map[q_no] = bool(is_correct)

            if is_correct:
                st.session_state.correct_count += 1
                st.session_state.streak += 1
            else:
                st.session_state.streak = 0
                st.session_state.wrong_log.append(
                    {
                        "q_index": q_no,
                        "question": q.text,
                        "selected": q.options[selected_idx],
                        "correct": q.options[q.answer_index],
                        "explanation": q.explanation,
                    }
                )

        is_last = (idx == total - 1)
        next_label = "結果表示" if is_last else "次へ"

        c1, c2, c3 = st.columns([1, 1, 1.2])
        with c1:
            st.button(
                "判定する",
                type="primary",
                disabled=disabled,
                use_container_width=True,
                on_click=_on_judge,
            )
        with c2:
            prev = st.button("前へ", disabled=(idx == 0), use_container_width=True)
        with c3:
            next_ = st.button(next_label, disabled=not disabled, use_container_width=True)

        if bool(st.session_state.answered):
            if int(st.session_state.selected) == int(q.answer_index):
                st.success("正解")
            else:
                st.error("不正解")
                st.info(f"正解：{q.options[q.answer_index]}")

        with st.expander("解説", expanded=False):
            st.write(q.explanation)

        if prev:
            st.session_state.idx = max(0, idx - 1)
            st.session_state.selected = None
            st.session_state.answered = False
            st.rerun()

        if next_:
            if is_last:
                st.session_state.mode = "result"
            else:
                st.session_state.idx = min(total - 1, idx + 1)
                st.session_state.selected = None
                st.session_state.answered = False
            st.rerun()

    with right:
        final_answered = len(st.session_state.last_answer_map)
        final_correct = sum(1 for v in st.session_state.last_answer_map.values() if v)
        final_remaining = max(0, total - final_answered)

        open_card("学習状況", "", "")
        st.markdown(
            f"""
<div class="gx-statgrid">
  <div class="gx-stat"><small>回答</small><b>{final_answered}</b></div>
  <div class="gx-stat"><small>正解</small><b>{final_correct}</b></div>
  <div class="gx-stat"><small>不正解</small><b>{final_answered - final_correct}</b></div>
  <div class="gx-stat"><small>残り</small><b>{final_remaining}</b></div>
</div>
""",
            unsafe_allow_html=True,
        )
        close_card()

        st.write("")

        open_card("リセット", "", "")
        if st.button("リセット", use_container_width=True):
            reset_run(total)
            st.rerun()
        close_card()
