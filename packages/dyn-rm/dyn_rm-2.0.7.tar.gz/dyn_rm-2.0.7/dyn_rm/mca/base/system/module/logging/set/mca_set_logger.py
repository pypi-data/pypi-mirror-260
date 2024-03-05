from dyn_rm.mca.base.logger.module import MCALoggerModule
import time

class MCASetLogger(MCALoggerModule):
    filename = "set.csv"

    def get_header(self) -> list:
        return ['timestamp', 'event', 'set_name', 'task_id', 'size']

    def create_event_function(self, ev, set):
        event = dict()
        event['timestamp'] = time.time()
        event['event'] = ev
        event['id'] = set.run_service("GET", "GID")
        event['task_id'] = set.run_service("GET", "TASK").run_service("GET", "GID")
        event['size'] = set.run_service("GET", "NUM_PROCS")

        return event
    
    def log_event_function(self, event: dict):
        row = [event['timestamp'], event['event'], event['set_name'], event['task_id'], event['size']]
        self.write_rows(self.get_filename(), [row])   

    def log_events_function(self, events: list):
        rows = []
        for event in events:
            row = [event['timestamp'], event['event'], event['set_name'], event['task_id'], event['size']]
            rows.append(row)
        self.write_rows(self.get_filename(), rows)         

    def postprocessing_function(self, params: dict):
        pass

    def preprocessing_function(self, params: dict):
        pass