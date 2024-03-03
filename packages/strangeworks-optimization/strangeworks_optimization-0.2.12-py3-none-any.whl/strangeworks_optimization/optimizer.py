import copy
import json
import tempfile
import time
from typing import Any, List, Optional

import strangeworks as sw
from strangeworks.core.client.backends import Backend
from strangeworks.core.client.jobs import Job
from strangeworks.core.client.resource import Resource
from strangeworks.core.errors.error import StrangeworksError
from strangeworks_core.types.job import Status
from strangeworks_optimization_models.problem_models import (
    StrangeworksModel,
    StrangeworksModelFactory,
)
from strangeworks_optimization_models.solution_models import (
    StrangeworksSolution,
    StrangeworksSolutionFactory,
)
from strangeworks_optimization_models.solver_models import (
    StrangeworksSolver,
    StrangeworksSolverFactory,
)
from strangeworks_optimization_models.strangeworks_models import (
    StrangeworksOptimizationJob,
    StrangeworksOptimizationModel,
    StrangeworksOptimizationSolution,
    StrangeworksOptimizationSolver,
)


def _get_product_slug(label_name: str) -> str:
    if label_name in ["jij"]:
        return "jijzept"
    elif label_name in ["azure"]:
        return "azure-quantum"
    elif label_name in ["braket"]:
        return "amazon-braket"
    return label_name


class StrangeworksOptimizer:
    """Strangeworks optimization controller."""

    model: StrangeworksModel | None = None
    solver: StrangeworksSolver | None = None
    solution: StrangeworksSolution | None = None
    job: Job | None = None
    tags: List[str] | None = None

    def __init__(
        self,
        model: Any | None = None,
        solver: Any | None = None,
        options: dict | None = None,
        solution: Any | None = None,
        resource_slug: str | None = None,
        tags: List[str] | None = None,
    ) -> None:
        """Initialize the StrangeworksOptimizer.

        If a resource slug is provided, confirm it exists and set is as resource for
        its product. If there is no resource associated with the given slug, raise
        error.

        If no resource slug is provided, try retrieving a resource slug for the
        optimization service. If the user does not have a resource configured, raise
        error.

        Parameters
        ----------
        model: Any | None
            The model that will be used by the optimizer.
        solver: Any | None
            The solver to use for optimization.
        options: dict | None
            Options to pass to the optimizer.
        solution: Any | None
            Solution to be used.
        resource_slug: str | None
            Allows user to specify a specific resource to use.
        tags: List[str] | None
            List of user specified tags that will be associated with the job.
        """
        self.model = StrangeworksModelFactory.from_model(model) if model else None

        if solver:
            self.solver = StrangeworksSolverFactory.from_solver(solver)
            self._init_solver()

        if tags:
            self.tags = tags
        else:
            self.tags = None

        self.options = options
        self.solution = StrangeworksSolutionFactory.from_solution(solution)

        if resource_slug:
            sw.set_resource_for_product(resource_slug=resource_slug, product_slug="optimization")
        self.resource: Resource = sw.get_resource_for_product("optimization")

    def _init_solver(self):
        if self.solver:
            product_slug = _get_product_slug(self.solver.provider)
            self.sub_rsc = sw.get_resource_for_product(product_slug)

            self.solver.strangeworks_parameters = {
                "sub_product_slug": self.sub_rsc.product.slug,
                "sub_resource_slug": self.sub_rsc.slug,
            }

    def run(self) -> Job | None:
        solver = StrangeworksOptimizationSolver.from_solver(self.solver)

        if self.tags:
            for tag in self.tags:
                if len(tag) > 35:
                    raise StrangeworksError("Tag length cannot be greater than 35 characters")

            sw_params = json.loads(solver.strangeworks_parameters)
            sw_params["tags"] = self.tags
            solver.strangeworks_parameters = json.dumps(sw_params)

        if self.options and not isinstance(self.options, dict):  # check for backwards compatibility
            # Transform options class to dict and remove entries that are None
            options = copy.deepcopy(self.options.__dict__)
            for k, v in self.options.__dict__.items():
                if v is None:
                    options.pop(k)
        else:
            options = self.options
        solver.solver_options = json.dumps(options) if self.options else json.dumps(None)

        strangeworks_optimization_job = StrangeworksOptimizationJob(
            model=StrangeworksOptimizationModel.from_model(self.model),
            solver=solver,
            solution=StrangeworksOptimizationSolution.from_solution(self.solution) if self.solution else None,
        )
        res = sw.execute(self.resource, payload=strangeworks_optimization_job.model_dump(), endpoint="run")

        job_slug = json.loads(res["solution"]["strangeworks_parameters"])["job_slug"]
        self.job = sw.jobs(slug=job_slug)[0]
        return self.job

    def results(self, sw_job_slug):
        endpoint = f"results/{sw_job_slug}"
        solution = sw.execute(self.resource, endpoint=endpoint)
        solution = StrangeworksOptimizationSolution(**solution)

        if solution.solution == "running":
            status = self.status(sw_job_slug)

            while not status.is_terminal_state:  # COMPLETED, CANCELLED, or FAILED
                time.sleep(10)
                status = self.status(sw_job_slug)

            if status == Status.COMPLETED:
                solution = sw.execute(self.resource, endpoint=endpoint)
                solution = StrangeworksOptimizationSolution(**solution)
            else:
                raise StrangeworksError(f"Cannot get results, Job status is {status.value}")

        return solution.deserialize()

    def status(self, sw_job_slug) -> Status:
        endpoint = f"status/{sw_job_slug}"
        resp = sw.execute(self.resource, endpoint=endpoint)
        return Status(resp)

    def upload_model(self, model=None) -> str | None:
        strangeworks_optimization_model = StrangeworksOptimizationModel.from_model(model=model or self.model)
        with tempfile.NamedTemporaryFile(mode="w+") as t:
            t.write(strangeworks_optimization_model.model_dump_json())

            f = sw.upload_file(t.name)
        return f.url if isinstance(f.url, str) else None

    def backends(self) -> Optional[Backend]:
        """List of optimization backends."""
        # get resources associated with this workspace
        resources = sw.resources()
        # if workspace has no resources, return an empty list.
        if not resources:
            return []
        # generate list of product slugs to use for filtering backends.
        product_slugs = [x.product.slug for x in resources]
        backends = sw.backends(
            product_slugs=product_slugs,
            backend_type_slugs=["optimization"],
        )

        return backends

    def download_input_file(self, sw_job_slug) -> StrangeworksOptimizationJob:
        # Returns the entire OptimizationJob object/payload
        # If the job has completed, the solution should also be included.

        sw_job = sw.jobs(slug=sw_job_slug)[0]

        for file in sw_job.files:
            if file.file_name == "OptimizationJob.json":
                return StrangeworksOptimizationJob(**sw.download_job_files([file.url])[0])

        raise StrangeworksError("OptimizationJob.json not found in job files")

    def download_input_model(self, sw_job_slug):
        # Parses the OptimizationJob.json and returns the deserialized model

        OptimizationJob = self.download_input_file(sw_job_slug)
        return OptimizationJob.model.deserialize().model

    @property
    def resource_slug(self):
        return self.resource.slug
