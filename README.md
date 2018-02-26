# notifications-ftp
Notifications Reports Microservice

Handle updating of reporting database and provide rest endpoints to fetch
records

Basic Flask/Celery python app.

## Setting Up

### AWS credentials

To run the Reports application, you will need appropriate AWS credentials. You should receive these from whoever administrates your AWS account. Make sure you've got both an access key id and a secret access key.

Your aws credentials should be stored in a folder located at `~/.aws`. Follow [Amazon's instructions](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-config-files) for storing them correctly.

### Virtualenv

```
mkvirtualenv -p /usr/local/bin/python3 notifications-reports
```


##  To run the application

First, run `scripts/bootstrap.sh` to install dependencies.

You need to run the flask application and a local celery instance.

There are three run scripts for running all the necessary parts.

Flask endpoints - for Report database statistic queries
```
scripts/run_app.sh
```

Celery queue reader - to start celery workers which consumes tasks from SQS, posted originally from API.
```
scripts/run_celery.sh
```


##  To test the application

Simply run

```
make build test
```

That will run flake8 for code analysis and our unit test suite.