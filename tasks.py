import os
from invoke import Context, task

WINDOWS = os.name == "nt"
PYTHON_VERSION = "3.12"

import shutil

@task
def install(c: Context):
    """Install dependencies. Checks if runs within 'bayesian_ml' env, otherwise runs in it."""
    if os.environ.get("CONDA_DEFAULT_ENV") == "bayesian_ml":
        run_cmd = lambda cmd: c.run(cmd, echo=True, pty=not WINDOWS)
    else:
        run_cmd = lambda cmd: c.run(f"conda run -n bayesian_ml {cmd}", echo=True, pty=not WINDOWS)

    run_cmd("pip install -r requirements.txt")

    if shutil.which("nvidia-smi"):
        run_cmd('pip install "jax[cuda13]"')
    else:
        run_cmd("pip install jax")

@task(help={'path': "Optional path to create the environment in. If not provided, uses default name 'bayesian_ml'."})
def create_env(c: Context, path=None):
    """Create a conda environment."""
    jax_pkg = '"jax[cuda13]"' if shutil.which("nvidia-smi") else "jax"

    if path:
        env_path = f"{path}\\bayesian_ml"
        c.run(f'conda create -p "{env_path}" python={PYTHON_VERSION} pip --no-default-packages --yes', echo=True, pty=not WINDOWS)
        
        pip_exe = os.path.join(env_path, "Scripts", "pip.exe") if WINDOWS else os.path.join(env_path, "bin", "pip")
        
        c.run(f'"{pip_exe}" install -r requirements.txt', echo=True, pty=not WINDOWS)
        c.run(f'"{pip_exe}" install {jax_pkg}', echo=True, pty=not WINDOWS)
    else:
        c.run(f'conda create -n bayesian_ml python={PYTHON_VERSION} pip --no-default-packages --yes', echo=True, pty=not WINDOWS)
        c.run("conda run -n bayesian_ml pip install -r requirements.txt", echo=True, pty=not WINDOWS)
        c.run(f"conda run -n bayesian_ml pip install {jax_pkg}", echo=True, pty=not WINDOWS)