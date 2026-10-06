"""
UI Bootstrap & Custom Styling Helpers (Streamlit Custom Style Layer 2)
====================================================================
Adheres to the architectural patterns demonstrated in Paldom/streamlit-custom-style:
  - Layer 1: Native theme config (.streamlit/brand-theme.toml)
  - Layer 2: Shared page bootstrap (init_page, st.logo, st.html)
  - Layer 3: Keyed CSS selectors (.st-key-*) for rock-solid UI durability
"""

from pathlib import Path
import streamlit as st


def _load_css(path: str | Path = "assets/styles.css") -> None:
    """Loads external CSS securely via Streamlit's native st.html element."""
    css_path = Path(path)
    if css_path.exists():
        content = css_path.read_text(encoding="utf-8")
        try:
            # Modern Streamlit 1.30+ native HTML injection
            st.html(f"<style>{content}</style>")
        except AttributeError:
            st.markdown(f"<style>{content}</style>", unsafe_allow_html=True)


def init_page(
    page_title: str = "CPIP · Decision Intelligence Platform",
    page_icon: str = "🌐",
    layout: str = "wide",
    initial_sidebar_state: str = "expanded"
) -> None:
    """Centralized page bootstrap initializing configs, CSS, and branded logos."""
    try:
        st.set_page_config(
            page_title=page_title,
            page_icon=page_icon,
            layout=layout,
            initial_sidebar_state=initial_sidebar_state
        )
    except Exception:
        pass  # Already initialized

    # Load Keyed CSS
    _load_css("assets/styles.css")

    # Apply Branded Sidebar Logo (Streamlit 1.35+ official feature)
    logo_path = Path("assets/logo.svg")
    icon_path = Path("assets/logo_icon.svg")
    if hasattr(st, "logo") and logo_path.exists() and icon_path.exists():
        try:
            st.logo(str(logo_path), icon_image=str(icon_path))
        except Exception:
            pass


def render_metric_card(
    label: str,
    value: str,
    sub: str = "",
    trend: str = "",
    trend_type: str = "positive",
    variant: str = "cyan",
    fill_pct: int = 75
) -> None:
    """Renders a modern glassmorphic KPI card inside a keyed container (.st-key-*)."""
    color_map = {
        "cyan": "#00d2ff",
        "violet": "#8b5cf6",
        "emerald": "#10b981",
        "red": "#e50914",
        "amber": "#f59e0b",
        "blue": "#3b82f6"
    }
    accent = color_map.get(variant, "#00d2ff")
    trend_class = f"trend-{trend_type}"

    html = f"""
    <div class="custom-card-header">
      <span class="custom-card-label">{label}</span>
      {f'<span class="trend-badge {trend_class}">{trend}</span>' if trend else ''}
    </div>
    <div class="custom-card-val">{value}</div>
    <div class="card-sparkbar">
      <div class="card-sparkbar-fill" style="width: {fill_pct}%; background: {accent};"></div>
    </div>
    <div class="custom-card-footer">
      <span style="color: #94a3b8; font-size: 11px;">{sub}</span>
    </div>
    """
    with st.container(key=f"metric_{variant}"):
        st.markdown(html, unsafe_allow_html=True)


def apply_plotly_theme(fig, is_dark: bool = True):
    """Applies executive glassmorphic styling to Plotly figures."""
    paper_bg = "rgba(0,0,0,0)"
    plot_bg = "rgba(0,0,0,0)"
    text_color = "#f8fafc" if is_dark else "#0f172a"
    grid_color = "rgba(255, 255, 255, 0.06)" if is_dark else "rgba(0, 0, 0, 0.06)"

    fig.update_layout(
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(family="Plus Jakarta Sans, sans-serif", color=text_color, size=11),
        title_font=dict(family="Plus Jakarta Sans, sans-serif", color=text_color, size=14),
        legend=dict(
            font=dict(color=text_color, size=10),
            bgcolor="rgba(14, 19, 34, 0.6)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1
        ),
        margin=dict(l=30, r=20, t=40, b=30),
        xaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=grid_color,
            tickfont=dict(color="#94a3b8", family="JetBrains Mono", size=10)
        ),
        yaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=grid_color,
            tickfont=dict(color="#94a3b8", family="JetBrains Mono", size=10)
        )
    )
    return fig
