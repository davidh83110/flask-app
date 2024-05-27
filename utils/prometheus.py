from prometheus_flask_exporter import RESTfulPrometheusMetrics


class PrometheusMetrics:
    def __init__(self, app, api):
        # For flask_prometheus_exporter
        self.metrics = RESTfulPrometheusMetrics(app, api, default_latency_as_histogram=False, export_defaults=False)
