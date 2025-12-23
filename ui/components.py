# ui/components.py

from __future__ import annotations

import html

import streamlit as st


def _esc(text: object) -> str:
    # HTML用にエスケープする
    return html.escape("" if text is None else str(text), quote=True)


def inject_css(css_text: str) -> None:
    # CSSをアプリに適用する
    st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)


def render_topbar(title: str, subtitle: str, set_label: str) -> None:
    # トップバーを描画する
    st.markdown(
        f"""
<div class="gx-topbar">
  <div class="gx-brand">
    <div class="gx-logo" aria-hidden="true">
      <svg viewBox="0 0 24 24" width="20" height="20" fill="none">
        <path d="M7 14.5c0-3 2.3-5.5 5.2-5.5 2.3 0 4.2 1.5 4.8 3.6" stroke="white" stroke-width="2" stroke-linecap="round"/>
        <path d="M7.2 14.5c.6 2.1 2.5 3.6 4.8 3.6 1.6 0 3-.7 4-1.8" stroke="white" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </div>
    <div class="gx-title">
      <b>{_esc(title)}</b>
      <span>{_esc(subtitle)}</span>
    </div>
  </div>
  <div class="gx-actions">
    <div class="gx-pill"><small>セット</small><b>{_esc(set_label)}</b></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def open_card(header_title: str, header_subtitle: str, header_badge: str) -> None:
    # カードの開始を描画する
    st.markdown(
        f"""
<div class="gx-card">
  <div class="gx-card-hd">
    <div class="left">
      <b>{_esc(header_title)}</b>
      <span>{_esc(header_subtitle)}</span>
    </div>
    <div class="gx-badge accent">{_esc(header_badge)}</div>
  </div>
  <div class="gx-card-bd">
""",
        unsafe_allow_html=True,
    )


def close_card() -> None:
    # カードの終了を描画する
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_progress(current: int, total: int, accuracy_pct: int) -> None:
    # 進捗バーを描画する
    try:
        cur = int(current)
        tot = int(total)
        acc = int(accuracy_pct)
    except Exception:
        cur, tot, acc = 0, 0, 0

    pct = 0
    if tot > 0:
        pct = int(round((max(0, min(cur, tot)) / tot) * 100))

    acc = max(0, min(acc, 100))

    st.markdown(
        f"""
<div class="gx-progress">
  <div class="gx-bar"><i style="width:{pct}%;"></i></div>
  <div class="gx-meta">
    <span>{cur} / {tot}</span>
    <span>正答率: {acc}%</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_tags(category: str, difficulty: int, qtype: str) -> None:
    # タグ行を描画する
    try:
        diff = int(difficulty)
    except Exception:
        diff = 0

    st.markdown(
        f"""
<div class="gx-tags">
  <span class="gx-badge">{_esc(category)}</span>
  <span class="gx-badge warn">難易度: {_esc(diff)}</span>
  <span class="gx-badge">形式: {_esc(qtype)}</span>
</div>
""",
        unsafe_allow_html=True,
    )


def render_question_text(text: str) -> None:
    # 問題文を描画する
    st.markdown(f'<div class="gx-qtext">{_esc(text)}</div>', unsafe_allow_html=True)


def render_stats_panel(answered: int, correct: int, streak: int, remaining: int) -> None:
    # 統計カードを描画する
    open_card("学習状況", "", "")
    st.markdown(
        f"""
<div class="gx-statgrid">
  <div class="gx-stat"><small>回答</small><b>{_esc(int(answered))}</b></div>
  <div class="gx-stat"><small>正解</small><b>{_esc(int(correct))}</b></div>
  <div class="gx-stat"><small>連続正解</small><b>{_esc(int(streak))}</b></div>
  <div class="gx-stat"><small>残り</small><b>{_esc(int(remaining))}</b></div>
</div>
""",
        unsafe_allow_html=True,
    )
    close_card()
