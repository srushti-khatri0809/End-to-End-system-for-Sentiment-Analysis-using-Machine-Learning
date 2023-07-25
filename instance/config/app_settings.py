
name = "Web News Engine"

host = "127.0.0.9"

threaded = False

debug = False

## dev
#port = 5000

#from instance.config.api_keys import *

## prod
import os
port = int(os.environ.get("PORT", 5000))

# Twitter API keys
twitter_keys = {
    "CONSUMER_KEY": "JVhJ9v6VJhOTDjqtKG46i4TsP",
    "SECRET_KEY": "VWDAIgKu4irUNp4fggLnxQ4cB8CfwXxOLJQvMr2X0uR1lF0vDj",
    "ACCESS_TOKEN": "1672614748712767489-Bb047ZK9yGWEpJVDN6Dj0Y6U7B8YvH",
    "SECRET_ACCESS_TOKEN": "XP5tdr8njJfAmjxiBOOnGoI1OBS5XDFbyceSSLG1XFbFy"
}

# NewsAPI API key
newsapi_keys = {
    "KEY": "6457cd76b3fb453b80e270759e830491"
}

# EventRegistry API key
eventregistry_keys = {
    "KEY": "1032623e-8f98-4e56-bf8f-ab6ace519e11"
}


