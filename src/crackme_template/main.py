import subprocess
from typing import Optional

from cookiecutter.main import cookiecutter
import typer

app = typer.Typer()


class Config:
    def __init__(
        self,
        author_name: Optional[str],
        author_email: Optional[str],
    ) -> None:
        self.author_email = author_email or self._git("user.email")
        self.author_name = author_name or self._git("user.name")

    def dict(self) -> dict[str, str]:
        return {
            "author_name": self.author_name,
            "author_email": self.author_email,
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
    author_name: Optional[str] = typer.Option(None),
    author_email: Optional[str] = typer.Option(None),
) -> None:
    config = Config(author_name=author_name, author_email=author_email)
    cookiecutter(
        template="https://github.com/nymann/crackme-template.git",
        extra_context=config.dict(),
    )


if __name__ == "__main__":
    app()
