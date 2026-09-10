"""
IntelliFormat Performance Package
Benchmarking suite measuring execution latency, throughput, and peak memory usage on large manuscripts.
"""

from .benchmark import run_benchmark, BenchmarkRunner

__all__ = ["run_benchmark", "BenchmarkRunner"]
