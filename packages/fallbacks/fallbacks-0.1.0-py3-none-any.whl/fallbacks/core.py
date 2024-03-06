from __future__ import annotations


class Var:
    """
    Storage for whether a fast path should be taken.

    >>> supports_range_requests = Var(__name__, "range_requests")
    >>> worth_trying = supports_range_requests.check(host)
    ... if worth_trying:
    ...     # fast path, if it works
    ...     try:
    ...         resp = sess.get(...)
    ...     except HTTPError as e:
    ...         if e.code == 501:
    ...             supports_range_requests.record(host, False)
    ...         # any HTTPError results in slow path, but only 501 records
    ...     process(resp)
    ...     supports_range_requests.record(host, True)
    ...     return
    ... # slow path
    ... resp = sess.get(...)
    ... process(resp)
    """

    def __init__(self, app: str, name: str) -> None:
        self._cache: dict[str, bool] = {}

    def check(self, key: str, default: bool = True) -> bool:
        return self._cache.get(key, default)

    def record(self, key: str, value: bool) -> None:
        self._cache[key] = value
