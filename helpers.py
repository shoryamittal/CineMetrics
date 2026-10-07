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
    fill_pct: int = 75,
    key: str | None = None
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
    clean_label = "".join(c for c in label.lower() if c.isalnum() or c == "_").replace(" ", "_")
    card_key = key or f"metric_{variant}_{clean_label}"
    with st.container(key=card_key):
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


def create_kpi_gauge(
    title: str,
    value: float,
    target: float,
    min_val: float,
    max_val: float,
    prefix: str = "",
    suffix: str = "",
    is_dark: bool = True,
    higher_is_better: bool = True
):
    """Creates a Power BI-style Executive KPI Bullet Dial Gauge."""
    import plotly.graph_objects as go

    if higher_is_better:
        steps = [
            {'range': [min_val, max(min_val, target * 0.75)], 'color': "rgba(229, 9, 20, 0.22)"},
            {'range': [max(min_val, target * 0.75), target], 'color': "rgba(245, 158, 11, 0.22)"},
            {'range': [target, max_val], 'color': "rgba(16, 185, 129, 0.22)"}
        ]
    else:
        steps = [
            {'range': [min_val, target], 'color': "rgba(16, 185, 129, 0.22)"},
            {'range': [target, min(max_val, target * 1.25)], 'color': "rgba(245, 158, 11, 0.22)"},
            {'range': [min(max_val, target * 1.25), max_val], 'color': "rgba(229, 9, 20, 0.22)"}
        ]

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        number={
            'prefix': prefix,
            'suffix': suffix,
            'font': {'family': 'JetBrains Mono', 'size': 26, 'color': '#f8fafc'}
        },
        delta={
            'reference': target,
            'prefix': prefix,
            'suffix': suffix,
            'increasing': {'color': '#10b981' if higher_is_better else '#e50914'},
            'decreasing': {'color': '#e50914' if higher_is_better else '#10b981'}
        },
        title={'text': title, 'font': {'family': 'Plus Jakarta Sans', 'size': 13, 'color': '#94a3b8'}},
        gauge={
            'axis': {
                'range': [min_val, max_val],
                'tickcolor': '#94a3b8',
                'tickfont': {'family': 'JetBrains Mono', 'size': 9, 'color': '#64748b'}
            },
            'bar': {'color': "#00d2ff", 'thickness': 0.28},
            'bgcolor': 'rgba(14, 19, 34, 0.6)',
            'borderwidth': 1,
            'bordercolor': 'rgba(255, 255, 255, 0.1)',
            'steps': steps,
            'threshold': {
                'line': {'color': '#f59e0b', 'width': 3},
                'thickness': 0.8,
                'value': target
            }
        }
    ))
    fig.update_layout(
        height=220,
        margin=dict(l=25, r=25, t=35, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def create_waterfall_chart(
    title: str,
    categories: list,
    values: list,
    measures: list,
    prefix: str = "",
    suffix: str = "",
    is_dark: bool = True
):
    """Creates a Power BI-style Executive Waterfall Reconciliation Bridge."""
    import plotly.graph_objects as go

    text_labels = []
    for v, m in zip(values, measures):
        if m == "relative":
            text_labels.append(f"{prefix}{v:+,.1f}{suffix}")
        else:
            text_labels.append(f"{prefix}{v:,.1f}{suffix}")

    fig = go.Figure(go.Waterfall(
        name=title,
        orientation="v",
        measure=measures,
        x=categories,
        textposition="outside",
        text=text_labels,
        y=values,
        connector={"line": {"color": "rgba(255, 255, 255, 0.25)", "dash": "dot", "width": 1.5}},
        increasing={"marker": {"color": "#10b981"}},
        decreasing={"marker": {"color": "#e50914"}},
        totals={"marker": {"color": "#00d2ff"}}
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(family="Plus Jakarta Sans", size=14, color="#f8fafc")),
        height=380,
        margin=dict(l=35, r=25, t=50, b=40),
        waterfallgap=0.3
    )
    apply_plotly_theme(fig, is_dark=is_dark)
    return fig
