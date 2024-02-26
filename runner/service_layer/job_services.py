from runner.adapters import job_repository as repo


def execute(jobid: str, repo: repo.AbstractJobRepository, executer, session):
    job = repo.get(jobid)
    try:
        executer(job)
        job.complete()
    except Exception as ex:
        job.fail()
    finally:
        session.commit()
