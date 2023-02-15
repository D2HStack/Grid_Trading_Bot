import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# Constants
BASE_URL = "https://testnet.binancefuture.com"
WSS_URL = "wss://stream.binancefuture.com/ws"
PUBLIC_KEY = env('PUBLIC_KEY')
SECRET_KEY = env('SECRET_KEY')
