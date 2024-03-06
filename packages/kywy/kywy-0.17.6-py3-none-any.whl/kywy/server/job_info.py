import time


class JobInfo:
    def __init__(self, job_id: str, future):
        self.future = future
        self.job_id = job_id
        self.polled_after_done = False
        self.intermediate_events = []
        self.timestamp_seconds = time.time()

    def is_older(self, delay_seconds):
        return time.time() - self.timestamp_seconds > delay_seconds
