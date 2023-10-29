from typing import Union, overload

class MockFont:
    def __init__(self, *args: None, **kwargs: int | str) -> None:
        pass

    def measure(self, text: str) -> int:
        return len(text) * 10

    @overload 
    def metrics(self, metric: None) -> dict[str, int]: ...

    @overload 
    def metrics(self, metric: str) -> int: ...

    def metrics(self, metric: str | None = None) -> Union[int, dict[str, int]]:
        all_metrics = {"linespace": 18, "ascent": 12, "descent": 3}
        if metric is None:
            return all_metrics
        else:
            return all_metrics[metric]


