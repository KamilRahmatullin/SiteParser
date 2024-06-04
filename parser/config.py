import environ
from pathlib import Path


ENV_DIR = Path(__file__).resolve().parent.parent / '.env'

env = environ.Env()
with open(ENV_DIR, 'r') as f:
    environ.Env.read_env(f)