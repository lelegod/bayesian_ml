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