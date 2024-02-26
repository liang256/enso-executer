import argparse
import json
from runner.service_layer import job_services, unit_of_work
from runner.adapters import job_repository, executer, repository as script_repo


JOB_UOW = unit_of_work.FileSystemJobUnitOfWork()
EXECUTER = executer.LocalExecuter(script_repo.FileSystemRepository())


def main():
    parser = argparse.ArgumentParser(description="Execute job id.")

    # Positional argument for target-id
    parser.add_argument(
        "jobid", type=str, help="The target-id to automate tasks for."
    )

    args = parser.parse_args()

    with JOB_UOW:
        print([j.state for j in JOB_UOW.jobs.list()])

    job_services.execute(args.jobid, JOB_UOW, EXECUTER)

    job = JOB_UOW.jobs.get(args.jobid)  # read

    print(f"executed {job.id}: {job.state}")


if __name__ == "__main__":
    main()
