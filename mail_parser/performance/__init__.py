"""High-performance email processing components."""

from .parallel_processor import ParallelEmailProcessor
from .batch_writer import BatchWriter

__all__ = ['ParallelEmailProcessor', 'BatchWriter']
