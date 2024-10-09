import environ

env = environ.Env()
environ.Env.read_env('.env')

ELEVATION_API_KEY = env('ELEVATION_API_KEY')