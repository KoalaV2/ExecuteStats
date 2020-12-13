# Development Setup
```shell script
mkvirtualenv execute_stats
workon execute_stats
pip install -r requirements.txt
```

# Build
```shell script
docker build -t <name> .
docker run -p 5000:5000 -d <name> 
```

# ExecuteStats
Sees how long a program takes to excecute and puts it in a grafana graph


# Todo

* Add grafana variables
* Run either downloaded program in docker container or the ExecuteStats program itself in a docker container or both
