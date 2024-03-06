import pyarrow as pa
import io
import time

from kywy.server.kawa_error_manager import KawaErrorManager

_dataset_path_suffix = '_dataset'
_script_path_suffix = '_script'

class KawaDirectoryManager:

    def __init__(self,
                 working_directory,
                 kawa_error_manager: KawaErrorManager):
        self.error_manager = kawa_error_manager
        self._working_directory = working_directory
        self._working_directory.mkdir(exist_ok=True)

    def dataset_path(self, job_id: str):
        return self._working_directory / (job_id + _dataset_path_suffix)

    def script_path(self, job_id: str):
        return self._working_directory / (job_id + _script_path_suffix)

    def write_table(self, job_id: str, data_table: pa.Table):
        try:
            pa.parquet.write_table(data_table, self.dataset_path(job_id))
        except Exception as err:
            self.error_manager.rethrow(err)

    def read_table(self, job_id: str) -> pa.Table:
        try:
            return pa.parquet.read_table(self.dataset_path(job_id))
        except Exception as err:
            self.error_manager.rethrow(err)

    def write_encrypted_script(self, job_id: str, encrypted_script: str):
        try:
            with io.open(self.script_path(job_id), 'w', encoding='utf8') as f:
                f.write(encrypted_script)
        except Exception as err:
            self.error_manager.rethrow(err)

    def read_encrypted_script(self, job_id: str) -> str:
        try:
            with io.open(self.script_path(job_id), 'r', encoding='utf8') as f:
                encrypted_script = f.read()
            return encrypted_script
        except Exception as err:
            self.error_manager.rethrow(err)

    def remove_job_files(self, job_id):
        print('Remove working files for job:', job_id)
        self.dataset_path(job_id).unlink()
        self.script_path(job_id).unlink()

    def remove_files_older_than(self, max_age: int):
        self.__remove_files_older_than(max_age, '*' + _dataset_path_suffix)
        self.__remove_files_older_than(max_age, '*' + _script_path_suffix)

    def __remove_files_older_than(self, max_age: int, pattern: str):
        for item in self._working_directory.glob(pattern):
            if item.is_file():
                mtime = item.stat().st_mtime
                if time.time() - mtime > max_age:
                    print('debug: remove file ' + item.name)
                    item.unlink()

    def is_dataset_file(self, file):
        return file.name().endswith('_dataset')
