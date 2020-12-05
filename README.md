# Development Setup
```shell script
mkvirtualenv execute_stats
workon execute_stats
pip install -r requirements.txt
```

# Build
```shell script
docker build -t <name> .
docker run -d <name> -p8080:8080
```

# ExecuteStats
Sees how long a program takes to excecute and puts it in a grafana graph


# Todo

* Add user authentication
* Add grafana variables
* Make it so the uploaded program runs in a docker container instead of the server.
