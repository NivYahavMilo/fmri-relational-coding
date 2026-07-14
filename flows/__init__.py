"""Analysis flows: one module per analysis, each exposing a top-level ``run(...)``.

Each flow composes the shared functions in ``rc_core`` and ``data_access`` — there is no base
class or dispatcher; call ``flows.<analysis>.run(...)`` directly.
"""
