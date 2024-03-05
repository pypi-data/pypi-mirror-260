from biolib import api
from biolib._internal.runtime import RuntimeJobData as _RuntimeJobData


def set_main_result_prefix(result_prefix: str) -> None:
    runtime_job_data = _RuntimeJobData.get()
    if not runtime_job_data:
        raise Exception('Unable to load BioLib runtime job data') from None

    api.client.patch(
        data={'result_name_prefix': result_prefix},
        headers={'Job-Auth-Token': runtime_job_data['job_auth_token']},
        path=f"/jobs/{runtime_job_data['job_uuid']}/main_result/",
    )
