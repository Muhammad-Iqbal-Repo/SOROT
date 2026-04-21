# ui/components.py
"""
Small, reusable UI primitives used across the app.
Import these instead of duplicating inline HTML/CSS.
"""
import streamlit as st


def badge(text: str, color: str) -> str:
    """
    Returns an HTML inline pill badge.

    Args:
        text:  Label shown inside the badge.
        color: CSS background colour (hex or named colour).

    Returns:
        An HTML string — pass to st.markdown(..., unsafe_allow_html=True).
    """
    return (
        f'<span style="'
        f"background:{color};"
        f"color:white;"
        f"padding:2px 10px;"
        f"border-radius:12px;"
        f"font-size:0.8em;"
        f"margin:2px;"
        f'display:inline-block">'
        f"{text}</span>"
    )


def section_header(icon: str, title: str) -> None:
    """Renders a consistent section subheader with an icon."""
    st.subheader(f"{icon} {title}")


def empty_state(message: str = "Tidak ditemukan") -> None:
    """Renders a muted caption for empty data sections."""
    st.caption(message)


def confidence_color(level: str) -> str:
    """Maps a confidence level string to a display colour."""
    return {"high": "#2e7d32", "medium": "#f57c00", "low": "#c62828"}.get(
        level, "#757575"
    )
