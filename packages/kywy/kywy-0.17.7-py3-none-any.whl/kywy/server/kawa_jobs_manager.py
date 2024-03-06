import concurrent.futures
import json
import threading

from kywy.server.job_info import JobInfo
from kywy.server.kawa_directory_manager import KawaDirectoryManager
from kywy.server.kawa_error_manager import KawaErrorManager


class KawaJobsManager:

    def __init__(self,
                 kawa_directory_manager: KawaDirectoryManager,
                 kawa_error_manager: KawaErrorManager):
        self.directory_manager = kawa_directory_manager
        self.error_manager = kawa_error_manager
        self.jobs = {}
        # starts cleaner thread
        self.MAX_OLD_JOB = 24 * 3600  # 24 hours old
        self.CHECK_OLD_JOB_INTERVAL = 1 * 3600  # 1 hour
        threading.Timer(self.CHECK_OLD_JOB_INTERVAL, self.clear_old_jobs).start()

    def add_job(self,
                job_id: str,
                future: concurrent.futures.Future):
        self.jobs[job_id] = JobInfo(job_id, future)

    def poll_jobs(self, json_action_payload):
        try:
            poll_jobs = json_action_payload['jobs']
            poll_result = {}
            for job_id in poll_jobs:
                job_info = self.jobs.get(job_id)
                if job_info:
                    poll_result[job_id] = self.job_poll_result(job_info)
                else:
                    # Not found, maybe the Python server was restarted
                    poll_result[job_id] = self.job_poll_result_not_found()

            json_poll_result = json.dumps(poll_result)
            print('json_poll_result', json_poll_result)
            return json_poll_result

        except Exception as err:
            self.error_manager.rethrow(err)

    def job_poll_result(self, job_info: JobInfo):
        is_done = job_info.future.done()
        # intermediate events: how to know which ones are new since last polling?
        if is_done:
            if job_info.future.cancelled():
                return {'status': 'CANCELLED'}
            elif job_info.future.exception():
                return {
                    'status': 'FAILURE',
                    'error': self.error_manager.error_to_str(job_info.future.exception())
                }
            else:
                return {'status': 'SUCCESS'}  # TODO: result? (which form?)
        else:
            if job_info.future.running():
                return {'status': 'RUNNING'}
            else:
                return {'status': 'PENDING'}

    @staticmethod
    def job_poll_result_not_found():
        # May occur if the Python server was restarted, and so the job queue was lost
        return {'status': 'NOT_FOUND'}

    def clear_old_jobs(self):
        self.clear_old_jobs_from_map()
        self.directory_manager.remove_files_older_than(self.MAX_OLD_JOB)

    def clear_old_jobs_from_map(self):
        keep = {}
        for job_id, job_info in self.jobs.items():
            if not job_info.is_older(self.MAX_OLD_JOB):
                keep[job_id] = job_info
        self.jobs = keep
