"""Shared library for the knowledge-base tools in ``_tools/``.

Everything here is deterministic and dependency-light (PyYAML only) so that
every generator built on it is idempotent: running it twice changes nothing.
"""
