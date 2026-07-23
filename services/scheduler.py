"""
Hermes AI OS — Scheduler Service

Schedule-based task execution using the schedule library.
Supports periodic scans, health checks, and analytics reports.
"""

import logging
import threading
import time
from typing import Callable, Dict, Optional

import schedule

logger = logging.getLogger("hermes.services.scheduler")


class HermesScheduler:
    """Scheduler for periodic Hermes tasks.

    Usage::

        sched = HermesScheduler()
        sched.every(30, "minutes", my_scan_function)
        sched.start()  # runs in background thread
    """

    def __init__(self) -> None:
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._jobs: Dict[str, schedule.Job] = {}

    def every(
        self,
        interval: int,
        unit: str,
        task: Callable,
        name: Optional[str] = None,
    ) -> None:
        """Schedule a task to run at a fixed interval.

        Args:
            interval: How often to run (e.g. 30).
            unit: Time unit — "seconds", "minutes", "hours".
            task: Callable to execute.
            name: Optional name for this job.
        """
        job_name = name or task.__name__

        scheduler_unit = getattr(schedule.every(interval), unit, None)
        if scheduler_unit is None:
            logger.error("Invalid schedule unit: %s", unit)
            return

        job = scheduler_unit.do(task)
        self._jobs[job_name] = job
        logger.info("Scheduled '%s' every %d %s", job_name, interval, unit)

    def start(self) -> None:
        """Start the scheduler in a background thread."""
        if self._running:
            logger.warning("Scheduler already running")
            return

        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("Scheduler started")

    def _run_loop(self) -> None:
        """Internal loop that checks for pending jobs."""
        while self._running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        schedule.clear()
        logger.info("Scheduler stopped")

    def list_jobs(self) -> Dict[str, str]:
        """Return a map of job_name -> next_run."""
        return {
            name: str(job.next_run) for name, job in self._jobs.items()
        }
