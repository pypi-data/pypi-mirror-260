# fallbacks

Used for caching whether a fast path is worthwhile.

This is an extremely simple cache with no locking and an assumption that if
multiple threads/processes try to record for the same key, that it's the same
value (so it doesn't matter which wins).

TODO

* load/save on disk


# Version Compat

Usage of this library should work back to 3.7, but development (and mypy
compatibility) only on 3.10-3.12.  Linting requires 3.12 for full fidelity.

# Versioning

This library follows [meanver](https://meanver.org/) which basically means
[semver](https://semver.org/) along with a promise to rename when the major
version changes.

# License

fallbacks is copyright [Tim Hatch](https://timhatch.com/), and licensed under
the MIT license.  See the `LICENSE` file for details.
