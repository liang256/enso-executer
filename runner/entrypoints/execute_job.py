import argparse
import json
import sys
from runner.service_layer import job_services, unit_of_work
from runner.adapters import job_repository, executer, repository as script_repo


JOB_UOW = unit_of_work.FileSystemJobUnitOfWork()
EXECUTER = executer.SimpleExecuter(script_repo.FileSystemRepository())


def main():
    parser = argparse.ArgumentParser(description="Execute job id.")

    parser.add_argument(
        "jobid", type=str, help="The target-id to automate tasks for."
    )

    args = parser.parse_args()
    job_services.execute(args.jobid, JOB_UOW, EXECUTER)


if __name__ == "__main__":
    main()
