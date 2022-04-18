import json
from pathlib import Path
import shutil

from cookiecutter.main import cookiecutter
from crackmes_dl.api import CrackmesApi
from crackmes_dl.endpoints import Metadata
from github import Github
import typer

app = typer.Typer()


class Config:
    def __init__(
        self,
        github: Github,
        metadata: Metadata,
        binary_filename: str,
    ) -> None:
        self._github = github
        self.binary_filename = binary_filename
        user = self._github.get_user()
        self.git_registry = "https://github.com/"
        repo_name = metadata.name.replace(" ", "-")
        repo_name = f"crackme-{repo_name.lower()}"

        self.repo_name = repo_name
        try:
            user.create_repo(
                name=repo_name,
                description=f"Solution for {metadata.author}'s {metadata.name}",
                homepage=metadata.crackme_url,
            )
        except Exception:
            # Repo already exists
            pass
        self.project_slug = repo_name.replace("-", "_")
        self.project_name = " ".join([word.capitalize() for word in repo_name.split("-")])

        self.author_email = user.email
        self.author_name = user.name
        self.git_registry_account = user.login

    def dict(self) -> dict[str, str]:
        return {
            "repo_name": self.repo_name,
            "project_name": self.project_name,
            "project_slug": self.project_slug,
            "author_name": self.author_name,
            "author_email": self.author_email,
            "git_registry": self.git_registry,
            "git_registry_account": self.git_registry_account,
            "binary": self.binary_filename,
        }


@app.command()
def generate(
    github_access_token: str = typer.Option(...),
    crackme_id: str = typer.Option(...),
    template: str = typer.Option("https://github.com/nymann/crackme-template.git"),
) -> None:
    github = Github(login_or_token=github_access_token)

    crackmes_api = CrackmesApi(domain="https://crackmes.one")
    crackmes_api.download_single(output_dir=Path("."), crackme_id=crackme_id)
    with open(f"{crackme_id}/metadata.json") as json_file:
        metadata = Metadata(**json.load(json_file))
    binary_filename: Path = [file for file in Path(crackme_id).glob("*") if not file.name == "metadata.json"][0]
    config = Config(github=github, metadata=metadata, binary_filename=binary_filename.name)
    cookiecutter(
        template=template,
        extra_context=config.dict(),
        no_input=True,
    )
    shutil.move(src=crackme_id, dst=f"{config.repo_name}/bin")


if __name__ == "__main__":
    app()
