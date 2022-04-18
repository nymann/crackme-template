import subprocess
from typing import Optional

from cookiecutter.main import cookiecutter
import typer

app = typer.Typer()


class Config:
    def __init__(
        self,
        repo_name: str,
        git_registry_account: str,
        git_registry: str,
        author_name: Optional[str] = None,
        author_email: Optional[str] = None,
    ) -> None:
        self.git_registry = git_registry
        self.repo_name = repo_name
        self.project_slug = repo_name.replace("-", "_")
        self.project_name = " ".join([word.capitalize() for word in repo_name.split("-")])

        self.author_email = author_email or self._git("user.email")
        self.author_name = author_name or self._git("user.name")
        self.git_registry_account = git_registry_account

    def dict(self) -> dict[str, str]:
        return {
            "repo_name": self.repo_name,
            "project_name": self.project_name,
            "project_slug": self.project_slug,
            "author_name": self.author_name,
            "author_email": self.author_email,
            "git_registry": self.git_registry,
            "git_registry_account": self.git_registry_account,
        }

    def _git(self, command: str) -> str:
        output: bytes = subprocess.run(
            f"git config {command}",
            shell=True,
            capture_output=True,
        ).stdout
        return output.decode("utf-8").strip("\n")


@app.command()
def generate(
    repo_name: str = typer.Option(...),
    github_username: str = typer.Option(...),
    git_registry: str = "https://github.com/",
    author_name: Optional[str] = typer.Option(None),
    author_email: Optional[str] = typer.Option(None),
    template: str = typer.Option("https://github.com/nymann/crackme-template.git"),
) -> None:
    config = Config(
        repo_name=repo_name,
        git_registry=git_registry,
        git_registry_account=github_username,
        author_name=author_name,
        author_email=author_email,
    )
    cookiecutter(
        template=template,
        extra_context=config.dict(),
        no_input=True,
    )


if __name__ == "__main__":
    app()
