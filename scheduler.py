"""
Device Scheduler — runs periodic tasks and time-based triggers.
"""

import schedule
import time
import threading
import logging

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, workflow_engine):
        self.engine  = workflow_engine
        self._thread = None
        self._stop   = threading.Event()

    def start(self):
        # Evaluate time-based rules every minute
        schedule.every(1).minutes.do(self.engine.evaluate_time_triggers)
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info("Scheduler started")

    def stop(self):
        self._stop.set()
        schedule.clear()
        logger.info("Scheduler stopped")

    def _run(self):
        while not self._stop.is_set():
            schedule.run_pending()
            time.sleep(1)
