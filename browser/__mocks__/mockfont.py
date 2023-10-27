class MockFont:
    def __init__(self, *args, **kwargs):
        pass

    def measure(self, text):
        return len(text) * 10

    def metrics(self, metric=None):
        all_metrics = {"linespace": 18, "ascent": 12, "descent": 3}
        if metric is None:
            return all_metrics
        else:
            return all_metrics[metric]


