import argparse

from runner.service_layer import services, unit_of_work


JOB_UOW = unit_of_work.FileSystemJobUnitOfWork()


def main():
    parser = argparse.ArgumentParser(description="Execute job id.")

    parser.add_argument("jobid", type=str, help="The target-id to automate tasks for.")

    args = parser.parse_args()
    services.execute(args.jobid, JOB_UOW)


if __name__ == "__main__":
    main()
