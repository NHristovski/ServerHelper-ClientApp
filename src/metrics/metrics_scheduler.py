import sched
import time
from src.metrics.metrics_fetcher import get_metrics


class MetricsScheduler(object):
    def __init__(self):
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.interval = 60
        self._running = False

    def periodic(self, action, actionargs=()):
        if self._running:
            self.event = self.schedule.enter(self.interval, 1, self.periodic, (action, actionargs))
            action(*actionargs)

    def start(self):
        self._running = True
        self.periodic(get_metrics)
        self.schedule.run()

    def stop(self):
        self._running = False
        if self.schedule and self.event:
            self.schedule.cancel(self.event)
