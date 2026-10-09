"""
Unit and Integration Tests for serve_dashboard.py and helpers.py.
Verifies HTTP Server Endpoints, Health Probes, Route Rewriting,
and Power BI / Glassmorphic UI Helper Visualizations.
"""

import json
import urllib.request
import urllib.error
import plotly.graph_objects as go
import pytest

from serve_dashboard import is_port_available
from helpers import apply_plotly_theme, create_kpi_gauge, create_waterfall_chart


class TestDashboardServer:
    """Tests the running flagship HTTP dashboard server."""

    BASE_URL = "http://localhost:8080"

    def test_port_availability_utility(self):
        """Verifies port availability detection on ephemeral sockets."""
        # Port 8080 is currently occupied by the running server
        assert is_port_available(8080) is False

        # Port 59999 is likely free
        assert is_port_available(59999) is True

    @pytest.mark.parametrize("endpoint", ["/health", "/api/health", "/status", "/api/status"])
    def test_health_endpoints(self, endpoint):
        """Verifies health check endpoints return HTTP 200 with JSON payload."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=3) as resp:
                assert resp.status == 200
                assert "application/json" in resp.headers.get("Content-Type", "")
                assert resp.headers.get("Access-Control-Allow-Origin") == "*"
                assert "no-cache" in resp.headers.get("Cache-Control", "")

                body = json.loads(resp.read().decode("utf-8"))
                assert body["status"] == "UP"
                assert body["healthy"] is True
                assert body["version"] == "2.4.0"
        except urllib.error.URLError as e:
            pytest.fail(f"Flagship server health check failed at {url}: {e}")

    def test_root_index_serving(self):
        """Verifies root endpoint serves the flagship HTML dashboard."""
        url = f"{self.BASE_URL}/"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=3) as resp:
                assert resp.status == 200
                content = resp.read().decode("utf-8", errors="replace")
                assert "<!DOCTYPE html>" in content
                assert "CinePulse" in content or "Decision Intelligence" in content
        except urllib.error.URLError as e:
            pytest.fail(f"Flagship server root index failed: {e}")

    def test_catalog_json_serving(self):
        """Verifies catalog.json is served with 50 validated titles."""
        url = f"{self.BASE_URL}/catalog.json"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=3) as resp:
                assert resp.status == 200
                catalog = json.loads(resp.read().decode("utf-8"))
                assert isinstance(catalog, list)
                assert len(catalog) == 50
        except urllib.error.URLError as e:
            pytest.fail(f"Flagship server catalog.json failed: {e}")


class TestUIHelpers:
    """Tests UI helper visualizers and theme adapters."""

    def test_apply_plotly_theme_dark(self):
        """Verifies Plotly dark theme application."""
        fig = go.Figure(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]))
        themed_fig = apply_plotly_theme(fig, is_dark=True)

        layout = themed_fig.layout
        assert layout.paper_bgcolor == "rgba(0,0,0,0)"
        assert layout.plot_bgcolor == "rgba(0,0,0,0)"
        assert layout.font.color == "#f8fafc"
        assert "Plus Jakarta Sans" in layout.font.family

    def test_apply_plotly_theme_light(self):
        """Verifies Plotly light theme application."""
        fig = go.Figure(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]))
        themed_fig = apply_plotly_theme(fig, is_dark=False)

        layout = themed_fig.layout
        assert layout.font.color == "#0f172a"

    def test_create_kpi_gauge_higher_is_better(self):
        """Verifies KPI dial gauge generation with higher-is-better logic."""
        fig = create_kpi_gauge(
            title="Outflow Quality",
            value=94.5,
            target=90.0,
            min_val=50.0,
            max_val=100.0,
            prefix="",
            suffix="%",
            higher_is_better=True
        )

        assert len(fig.data) == 1
        indicator = fig.data[0]
        assert indicator.type == "indicator"
        assert indicator.mode == "gauge+number+delta"
        assert indicator.value == 94.5
        assert indicator.delta.reference == 90.0

    def test_create_kpi_gauge_lower_is_better(self):
        """Verifies KPI dial gauge generation with lower-is-better logic."""
        fig = create_kpi_gauge(
            title="Energy Consumption",
            value=450.0,
            target=500.0,
            min_val=200.0,
            max_val=800.0,
            higher_is_better=False
        )

        assert len(fig.data) == 1
        indicator = fig.data[0]
        assert indicator.value == 450.0
        assert indicator.delta.increasing.color == "#e50914"  # Red if increasing
        assert indicator.delta.decreasing.color == "#10b981"  # Green if decreasing

    def test_create_waterfall_chart(self):
        """Verifies Power BI-style waterfall chart construction."""
        categories = ["Baseline", "Water Conservation", "Pump Optimization", "Net OpEx"]
        values = [100.0, -15.0, -8.0, 77.0]
        measures = ["absolute", "relative", "relative", "total"]

        fig = create_waterfall_chart(
            title="Executive Cost Reconciliation",
            categories=categories,
            values=values,
            measures=measures,
            prefix="$",
            suffix="k"
        )

        assert len(fig.data) == 1
        wf = fig.data[0]
        assert wf.type == "waterfall"
        assert wf.measure == tuple(measures) or list(wf.measure) == measures
        assert list(wf.x) == categories
        assert list(wf.y) == values
