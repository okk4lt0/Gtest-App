# ui/components.py

from __future__ import annotations

import streamlit as st


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
      <b>{title}</b>
      <span>{subtitle}</span>
    </div>
  </div>
  <div class="gx-actions">
    <div class="gx-pill"><small>セット</small><b>{set_label}</b></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def open_card(header_title: str, header_subtitle: str, header_badge: str) -> None:
    # カードの開始を描画する
    badge_html = f'<div class="gx-badge accent">{header_badge}</div>' if header_badge else ""
    st.markdown(
        f"""
<div class="gx-card">
  <div class="gx-card-hd">
    <div class="left">
      <b>{header_title}</b>
      <span>{header_subtitle}</span>
    </div>
    {badge_html}
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
    pct = 0 if total <= 0 else int(round((current / total) * 100))
    st.markdown(
        f"""
<div class="gx-progress">
  <div class="gx-bar"><i style="width:{pct}%;"></i></div>
  <div class="gx-meta">
    <span>{current} / {total}</span>
    <span>正答率: {accuracy_pct}%</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_tags(category: str, difficulty: int, qtype: str) -> None:
    # タグ行を描画する
    st.markdown(
        f"""
<div class="gx-tags">
  <span class="gx-badge">{category}</span>
  <span class="gx-badge warn">難易度: {difficulty}</span>
  <span class="gx-badge">形式: {qtype}</span>
</div>
""",
        unsafe_allow_html=True,
    )


def render_question_text(text: str) -> None:
    # 問題文を描画する
    st.markdown(f'<div class="gx-qtext">{text}</div>', unsafe_allow_html=True)


def render_result_summary(total: int, correct: int, wrong: int) -> None:
    # 結果サマリーを描画する
    st.markdown(
        f"""
<div class="gx-statgrid">
  <div class="gx-stat"><small>総問題数</small><b>{total}</b></div>
  <div class="gx-stat"><small>正解数</small><b>{correct}</b></div>
  <div class="gx-stat"><small>不正解数</small><b>{wrong}</b></div>
  <div class="gx-stat"><small>正答率</small><b>{int(round((correct/total)*100)) if total else 0}%</b></div>
</div>
""",
        unsafe_allow_html=True,
    )
