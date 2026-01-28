import os
from invoke import Context, task

@task
def install(c: Context):
    """Install dependencies."""
    c.run("pip install -r requirements.txt", echo=True)

@task
def create_env(c: Context):
    """Create a conda environment."""
    c.run("conda create -n bayesian_ml python=3.12 --yes", echo=True)
    c.run("pip install -r requirements.txt", echo=True)

@task
def build_notes(c: Context):
    """Build LaTeX notes using pdflatex."""
    with c.cd("notes"):
        # Run twice to ensure TOC and references are correct
        c.run("pdflatex -interaction=nonstopmode main.tex", echo=True)
        c.run("pdflatex -interaction=nonstopmode main.tex", echo=True)

@task
def clean_notes(c: Context):
    """Clean LaTeX build artifacts."""
    with c.cd("notes"):
        exts = ["aux", "log", "out", "toc"]
        for ext in exts:
            cmd = f"del *.{ext}" if os.name == 'nt' else f"rm *.{ext}"
            c.run(cmd, echo=True, warn=True)