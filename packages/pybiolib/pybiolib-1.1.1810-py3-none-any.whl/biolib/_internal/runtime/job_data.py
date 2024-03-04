import json
from biolib.typing_utils import TypedDict, Optional, cast


class RuntimeJobDataDict(TypedDict):
    version: str
    job_requested_machine: str
    job_uuid: str
    job_auth_token: str


class RuntimeJobData:
    _job_data: Optional[RuntimeJobDataDict] = None

    @staticmethod
    def get() -> Optional[RuntimeJobDataDict]:
        if not RuntimeJobData._job_data:
            try:
                with open('/biolib/secrets/biolib_system_secret', mode='r') as file:
                    job_data: RuntimeJobDataDict = json.load(file)
            except BaseException:
                return None

            if not job_data['version'].startswith('1.'):
                raise Exception(f"Unexpected system secret version {job_data['version']} expected 1.x.x")

            RuntimeJobData._job_data = job_data

        return cast(RuntimeJobDataDict, RuntimeJobData._job_data)
