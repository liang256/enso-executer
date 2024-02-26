import argparse
import json
from runner.service_layer import job_services
from runner.adapters import job_repository, executer, repository as script_repo


class FakeSession:
    def __init__(self, job_repo) -> None:
        self.job_repo = job_repo

    def commit(self):
        data = {}

        for job in self.job_repo.jobs.values():
            data[job.id] = {"instructions": job.instructions, "state": job.state}

        with open(self.job_repo.path, "w") as file:
            file.write(json.dumps(data))


JOB_REPO = job_repository.FileSystemRepository()
EXECUTER = executer.LocalExecuter(script_repo.FileSystemRepository())
SESSION = FakeSession(JOB_REPO)


def main():
    parser = argparse.ArgumentParser(description="Execute job id.")

    # Positional argument for target-id
    parser.add_argument(
        "jobid", type=str, help="The target-id to automate tasks for."
    )

    args = parser.parse_args()

    job_services.execute(args.jobid, JOB_REPO, EXECUTER, SESSION)

    job = JOB_REPO.get(args.jobid)  # read

    print(f"executed {job.id}: {job.state}")


if __name__ == "__main__":
    main()
