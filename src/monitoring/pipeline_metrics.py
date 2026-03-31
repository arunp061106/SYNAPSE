import time

class PipelineMonitor:

    def __init__(self):
        self.start_time = time.time()
        self.total_events = 0
        self.total_batches = 0

    def record_batch(self, batch_size):
        self.total_batches += 1
        self.total_events += batch_size

    def report(self):
        elapsed = time.time() - self.start_time

        throughput = self.total_events / elapsed if elapsed > 0 else 0

        return {
            "elapsed_seconds": round(elapsed, 2),
            "total_events": self.total_events,
            "total_batches": self.total_batches,
            "events_per_sec": round(throughput, 2)
        }