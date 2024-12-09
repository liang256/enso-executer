# enso-executer
A Python-based framework for managing and executing jobs in a modular, scalable, and robust manner. The framework leverages Domain-Driven Design (DDD) principles to separate business logic from data persistence, making it highly adaptable for diverse use cases in production pipelines.

## Key Features
- Domain-Driven Design (DDD):
    - Encapsulates core job execution logic within domain models for better separation of concerns.
    - Ensures maintainability and scalability.
- Event-Driven Architecture:
    - Logs events such as script execution and failure, providing detailed feedback for debugging and auditing.
- Transactional Consistency:
    - Uses a Unit of Work pattern to ensure data consistency during job operations.
- Customizable Workflow:
    - Allows artists or developers to define and execute custom scripts with arguments.
- Error Handling:
    - Gracefully handles failures by rolling back operations and appending failure events.

## How It Works
Core Concepts
- Job: Represents a task containing a list of scripts to be executed sequentially. Each job tracks its state and events.

- Script: Represents an executable action. Scripts are retrieved and executed with custom arguments.

- Unit of Work: Manages the lifecycle of job persistence and ensures consistency during commit operations.

- Events: Captures key activities, including successful execution and errors, for debugging and audit trails.

## Workflow
1. Add a Job: Use the add function to create a new job with custom scripts and arguments.
2. Execute a Job: Use the execute function to run the job, handle errors, and log events.
3. Track Events: Monitor events for detailed feedback on execution progress and failures.

## Usage
```python
from job_execution_framework.service_layer.services import add, execute
from job_execution_framework.service_layer.unit_of_work import InMemoryJobUnitOfWork

# Step 1: Add a new job
instructions = [
    ("script_1", {"arg1": "value1"}),
    ("script_2", {"arg2": "value2"})
]
uow = InMemoryJobUnitOfWork()
job_id = add(instructions, job_uow=uow)

# Step 2: Execute the job
execute(job_id=job_id, job_uow=uow)

# Step 3: Inspect events
job = uow.jobs.get(job_id)
for event in job.events:
    print(event)
```

## Getting Started
### Prerequisites
Ensure you have the following installed:
- Docker
- Docker Compose

### Steps to Up and Use the App
1. Clone the repository:
```bash
git clone <repository-url>
cd enso_executor
```
2. Start the application:
```bash
make up
```
3. Test the API:

- Get list of jobs (should return an empty list):

```bash
curl http://localhost:5005/list-jobs
```
- Add a job:
```bash
curl -X POST http://localhost:5005/add-job \
-H "Content-Type: application/json" \
-d @./example_job.json
```
Expected response:

```json
{"jobid": "generated-job-id"}
```
- Get the job details (replace <jobid> with the returned jobid):
```bash
curl http://localhost:5005/get-job/<jobid>
```
- Execute the job:

```bash
curl -X POST http://localhost:5005/execute-job \
-H "Content-Type: application/json" \
-d '{"jobid": "<jobid>"}'
```
- Get updated list of jobs (to see job updates):

```bash
curl http://localhost:5005/list-jobs
```

### Usage Example
Below is an example of the example_job.json content, which defines a series of instructions for a job:

```json
{
  "instructions": [
    ["example_script", {"arg1": "open houdini file", "arg2": "/path/to/houdini/file.hip"}],
    ["example_script", {"arg1": "do something...", "arg2": "some arguments"}],
    ["example_script", {"arg1": "save houdini file", "arg2": "/release/saved.hip"}]
  ]
}
```
You can modify this file to create custom jobs with different scripts and arguments.

## Design Philosophy
### Challenges in Legacy Systems
- Tightly Coupled Logic:
In legacy systems, execution logic, data persistence, and event tracking are often intertwined. This makes tools difficult to maintain and extend, as a simple change can cascade into unexpected issues.

- Inefficient Debugging:
When a failure occurs, the entire job or workflow often requires retesting from the beginning. Without clear visibility into which script failed and with what parameters, troubleshooting becomes time-consuming and error-prone.

### How Job Execution Framework Solves These Challenges
- Separation of Concerns:
    - The framework encapsulates execution logic in the domain layer, data handling in the unit of work, and events in their own module. This separation improves maintainability and testability.
- Efficient Error Diagnosis:
    - Each script's execution result, including success or failure, is logged as an event. When a failure occurs:
        - The framework identifies exactly which script failed.
        - The parameters used during execution are recorded, allowing developers to quickly isolate and resolve the issue.
    - This eliminates the need to retest the entire workflow, significantly reducing debugging time.
- Extensibility:
    - New scripts or behaviors can be added without modifying the core framework, ensuring flexibility for evolving requirements.
- Scalability:
    - The decoupled architecture allows for future integration with distributed systems or message queues for large-scale workflows.