# core/state.py

from __future__ import annotations

import streamlit as st


def init_state(total: int) -> None:
    # セッション状態を初期化する（存在しないキーのみ作成）

    if not isinstance(total, int) or total < 0:
        raise ValueError("total must be non-negative int")

    if "mode" not in st.session_state:
        st.session_state.mode = "quiz"

    if "idx" not in st.session_state:
        st.session_state.idx = 0

    if "selected" not in st.session_state:
        st.session_state.selected = None

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

    if "wrong_log" not in st.session_state:
        st.session_state.wrong_log = []

    if "last_answer_map" not in st.session_state:
        # key: 問題番号(int, 1始まり), value: 正誤(bool)
        st.session_state.last_answer_map = {}


def reset_run(total: int) -> None:
    # セッション状態を完全に初期状態へ戻す

    if not isinstance(total, int) or total < 0:
        raise ValueError("total must be non-negative int")

    st.session_state.mode = "quiz"
    st.session_state.idx = 0
    st.session_state.selected = None
    st.session_state.answered = False
    st.session_state.answered_count = 0
    st.session_state.correct_count = 0
    st.session_state.streak = 0
    st.session_state.total = total
    st.session_state.wrong_log = []
    st.session_state.last_answer_map = {}
