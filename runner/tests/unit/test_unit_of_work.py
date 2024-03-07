from runner.domain import model
from runner.service_layer import unit_of_work


def test_can_commit():
    uof = unit_of_work.FileSystemJobUnitOfWork()
    with uof:
        uof.jobs.add(model.Job(id="dummy-job-id", instructions=[]))
        uof.commit()

    with uof:
        assert uof.jobs.get("dummy-job-id")
