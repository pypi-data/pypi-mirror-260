"""Utilities for the build pipeline."""
import importlib
from pathlib import Path
from shutil import rmtree
from types import ModuleType

from airflow.models import DAG

from dkist_processing_core import Workflow


__all__ = ["validate_workflows", "export_dags", "export_notebook_dockerfile", "export_notebooks"]


def validate_workflows(workflow_package: ModuleType, export_path: Path | None = None) -> None:
    """Validate that workflow engine (airflow) objects are acyclic and that exported workflows compile."""
    # configure export path.  Clean up after if export path not provided
    rm_export_path_after_test = not bool(export_path)
    if export_path is None:
        export_path = Path("export/")
    workflows = _extract_workflows_from_package(workflow_package)
    try:
        _validate_workflows(workflows, export_path)
    finally:
        if rm_export_path_after_test:
            rmtree(export_path)
    dags = [w.load() for w in workflows]
    _validate_dags(dags)


def export_dags(workflow_package: ModuleType, path: str | Path) -> list[Path]:
    """Export Airflow DAG files."""
    return [w.export_dag(path=path) for w in _extract_workflows_from_package(workflow_package)]


def export_notebooks(workflow_package: ModuleType, path: str | Path) -> list[Path]:
    """Export Jupyter Notebook files."""
    return [w.export_notebook(path=path) for w in _extract_workflows_from_package(workflow_package)]


def export_notebook_dockerfile(workflow_package: ModuleType, path: str | Path) -> Path:
    """Export a dockerfile to containerize notebooks."""
    path = Path(path)
    notebook_paths = export_notebooks(workflow_package=workflow_package, path=path)
    category = _extract_category_from_workflows(workflow_package=workflow_package)
    dockerfile = NotebookDockerfile(notebook_paths=notebook_paths, category=category)
    dockerfile_path = Path("Dockerfile")
    dockerfile_path.touch(exist_ok=False)
    with open(dockerfile_path, mode="w") as f:
        f.write(dockerfile.contents)
    return dockerfile_path


def _extract_category_from_workflows(workflow_package: ModuleType) -> str:
    workflows = _extract_workflows_from_package(workflow_package)
    categories = {w.category for w in workflows}
    if len(categories) > 1:
        raise ValueError(
            f"Multiple categories found in provided workflows. Categories found: {categories}"
        )
    return categories.pop()


def _extract_workflows_from_package(workflow_package: ModuleType) -> list[Workflow]:
    return _extract_objects_from_package_by_type(workflow_package, Workflow)


def _extract_objects_from_package_by_type(package: ModuleType, object_type: type) -> list:
    modules = _parse_unprotected_modules_names_from_package(package)
    objects = []
    for module in modules:
        imported_module = importlib.import_module(f".{module}", package.__name__)
        objects += [var for var in vars(imported_module).values() if isinstance(var, object_type)]
    return objects


def _parse_unprotected_modules_names_from_package(package: ModuleType) -> list[str]:
    package_path = Path(package.__path__[0])
    return [m.stem for m in package_path.glob("[!_]*.py")]


def _validate_dags(dags: list[DAG]) -> None:
    """Validate dags by ensuring they can be traversed without cycles and are syntactically correct."""
    for d in dags:
        try:
            d.topological_sort()
        except Exception as e:
            raise SyntaxError(f"DAG {d.dag_id} malformed.  Parsing resulted in error: {e=}") from e


def _validate_workflows(workflows: list[Workflow], export_path: Path) -> None:
    """Validate workflows by ensuring their exported version compiles as python and that there is at least one node."""
    for w in workflows:
        try:
            workflow_py = w.export_dag(path=export_path)
            with workflow_py.open(mode="r") as f:
                compile(f.read(), filename=f"{workflow_py.stem}.pyc", mode="exec")
        except Exception as e:
            raise SyntaxError(
                f"Workflow {w.workflow_name} malformed. "
                f"Parsing exported workflow resulted in error: {e=}"
            ) from e
        if len(w.nodes) == 0:
            raise ValueError(f"Workflow {w.workflow_name} has 0 nodes.")


class NotebookDockerfile:
    """Build a Dockerfile for deployment as a Manual Processing Worker."""

    def __init__(self, notebook_paths: list[Path], category: str):
        self.notebook_paths = notebook_paths
        self.category = category

    def notebook_paths_are_relative(self):
        """Validate that the notebook paths are all relative."""
        return all([not p.is_absolute() for p in self.notebook_paths])

    @property
    def contents(self) -> str:
        """Return the Dockerfile body."""
        return "\n".join(self.preamble + self.setup + self.notebooks + self.command)

    @property
    def preamble(self) -> list[str]:
        """Dockerfile preamble lines."""
        return ["FROM python:3.11", "ENV LANG=C.UTF-8"]

    @property
    def setup(self) -> list[str]:
        """Environment setup lines."""
        return [
            "COPY . /app",
            "WORKDIR /app",
            "RUN python -m pip install -U pip",
            "RUN pip install notebook",
            "RUN pip freeze | grep notebook= > constraints.txt",
            "RUN cat constraints.txt",
            "RUN python -m pip install -c constraints.txt .",
        ]

    @property
    def notebooks(self) -> list[str]:
        """Generate workflow notebooks and include in Docker container."""
        return [f"COPY {notebook_path} /notebooks/" for notebook_path in self.notebook_paths]

    @property
    def command(self) -> list[str]:
        """Run notebook server on deployment."""
        port = 8888
        return [
            f"EXPOSE {port}",
            f"CMD jupyter notebook --NotebookApp.allow_root=True --NotebookApp.base_url='/mpw-{self.category}/' --NotebookApp.ip='0.0.0.0' --NotebookApp.port={port} --MappingKernelManager.cull_idle_timeout=300 --notebook-dir=/notebooks --allow-root",
        ]
