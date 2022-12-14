# UdaConnect
## Overview
### Background
Conferences and conventions are hotspots for making connections. Professionals in attendance often share the same interests and can make valuable business and personal connections with one another. At the same time, these events draw a large crowd and it's often hard to make these connections in the midst of all of these events' excitement and energy. To help attendees make connections, we are building the infrastructure for a service that can inform attendees if they have attended the same booths and presentations at an event.

### Goal
You work for a company that is building a app that uses location data from mobile devices. Your company has built a [POC](https://en.wikipedia.org/wiki/Proof_of_concept) application to ingest location data named UdaTracker. This POC was built with the core functionality of ingesting location and identifying individuals who have shared a close geographic proximity.

Management loved the POC so now that there is buy-in, we want to enhance this application. You have been tasked to enhance the POC application into a [MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) to handle the large volume of location data that will be ingested.

To do so, ***you will refactor this application into a microservice architecture using message passing techniques that you have learned in this course***. It’s easy to get lost in the countless optimizations and changes that can be made: your priority should be to approach the task as an architect and refactor the application into microservices. File organization, code linting -- these are important but don’t affect the core functionality and can possibly be tagged as TODO’s for now!

### Architecture Design

<img src="/docs/architecture_design.PNG" />


### Technologies
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - API webserver
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
* [PostgreSQL](https://www.postgresql.org/) - Relational database
* [PostGIS](https://postgis.net/) - Spatial plug-in for PostgreSQL enabling geographic queries]
* [Vagrant](https://www.vagrantup.com/) - Tool for managing virtual deployed environments
* [VirtualBox](https://www.virtualbox.org/) - Hypervisor allowing you to run multiple operating systems
* [K3s](https://k3s.io/) - Lightweight distribution of K8s to easily develop against a local cluster
* [gRPC](https://grpc.io/) - is a modern open source high performance Remote Procedure Call (RPC) framework that can run in any environment. It can efficiently connect services in and across data centers with pluggable support for load balancing, tracing, health checking and authentication.
* [Apache Kafka](https://kafka.apache.org/) - is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications.

## Running the app
The project has been set up such that you should be able to have the project up and running with Kubernetes.

### Prerequisites
We will be installing the tools that we'll need to use for getting our environment set up properly.
1. [Install Docker](https://docs.docker.com/get-docker/)
2. [Set up a DockerHub account](https://hub.docker.com/)
3. [Set up `kubectl`](https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cluster-access/kubectl/)
4. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads) with at least version 6.0
5. [Install Vagrant](https://www.vagrantup.com/docs/installation) with at least version 2.0

### Environment Setup
To run the application, you will need a K8s cluster running locally and to interface with it via `kubectl`. We will be using Vagrant with VirtualBox to run K3s.

#### Initialize K3s
In this project's root, run `vagrant up`.
```bash
$ vagrant up
```
The command will take a while and will leverage VirtualBox to load an [openSUSE](https://www.opensuse.org/) OS and automatically install [K3s](https://k3s.io/). When we are taking a break from development, we can run `vagrant suspend` to conserve some ouf our system's resources and `vagrant resume` when we want to bring our resources back up. Some useful vagrant commands can be found in [this cheatsheet](https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4).

#### Set up `kubectl`
After `vagrant up` is done, you will SSH into the Vagrant environment and retrieve the Kubernetes config file used by `kubectl`. We want to copy the contents of this file into our local environment so that `kubectl` knows how to communicate with the K3s cluster.
```bash
$ vagrant ssh
```
You will now be connected inside of the virtual OS. Run `sudo cat /etc/rancher/k3s/k3s.yaml` to print out the contents of the file. You should see output similar to the one that I've shown below. Note that the output below is just for your reference: every configuration is unique and you should _NOT_ copy the output I have below.

Copy the contents from the output issued from your own command into your clipboard -- we will be pasting it somewhere soon!
```bash
$ sudo cat /etc/rancher/k3s/k3s.yaml

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJWekNCL3FBREFnRUNBZ0VBTUFvR0NDcUdTTTQ5QkFNQ01DTXhJVEFmQmdOVkJBTU1HR3N6Y3kxelpYSjIKWlhJdFkyRkFNVFU1T1RrNE9EYzFNekFlRncweU1EQTVNVE13T1RFNU1UTmFGdzB6TURBNU1URXdPVEU1TVROYQpNQ014SVRBZkJnTlZCQU1NR0dzemN5MXpaWEoyWlhJdFkyRkFNVFU1T1RrNE9EYzFNekJaTUJNR0J5cUdTTTQ5CkFnRUdDQ3FHU000OUF3RUhBMElBQk9rc2IvV1FEVVVXczJacUlJWlF4alN2MHFseE9rZXdvRWdBMGtSN2gzZHEKUzFhRjN3L3pnZ0FNNEZNOU1jbFBSMW1sNXZINUVsZUFOV0VTQWRZUnhJeWpJekFoTUE0R0ExVWREd0VCL3dRRQpBd0lDcERBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUFvR0NDcUdTTTQ5QkFNQ0EwZ0FNRVVDSVFERjczbWZ4YXBwCmZNS2RnMTF1dCswd3BXcWQvMk5pWE9HL0RvZUo0SnpOYlFJZ1JPcnlvRXMrMnFKUkZ5WC8xQmIydnoyZXpwOHkKZ1dKMkxNYUxrMGJzNXcwPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://127.0.0.1:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    password: 485084ed2cc05d84494d5893160836c9
    username: admin
```
Type `exit` to exit the virtual OS and you will find yourself back in your computer's session. Create the file (or replace if it already exists) `~/.kube/config` and paste the contents of the `k3s.yaml` output here.

Afterwards, you can test that `kubectl` works by running a command like `kubectl describe services`. It should not return any errors.

### Steps

Use one of the methods below to run udaconnect services 

### Method 1 : Using command line :

1. `kubectl apply -f deployment/db-configmap.yaml` - Set up environment variables for the pods
2. `kubectl apply -f deployment/db-secret.yaml` - Set up secrets for the pods
3. `kubectl apply -f deployment/postgres.yaml` - Set up a Postgres database running PostGIS
4. `kubectl apply -f deployment/udaconnect-zookeeper.yaml` - Set up the service and deployment for Zookeeper
5. `kubectl apply -f deployment/udaconnect-kafka.yaml` - Set up the service and deployment for the Kafka
6. `kubectl apply -f deployment/udaconnect-locationservice.yaml` - Set up the service and deployment for the LocationService
7. `kubectl apply -f deployment/udaconnect-locationprocessor.yaml` - Set up the service and deployment for the LocationProcessor
8. `kubectl apply -f deployment/udaconnect-personservice.yaml` - Set up the service and deployment for the PersonService
9. `kubectl apply -f deployment/udaconnect-connectionservice.yaml` - Set up the service and deployment for the ConnectionService 
10. `kubectl apply -f deployment/udaconnect-frontend.yaml` - Set up the service and deployment for the Frontend web app
11. `sh scripts/run_db_command.sh <POD_NAME>` - Seed your database against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`)

Manually applying each of the individual `yaml` files is cumbersome but going through each step provides some context on the content of the starter project. In practice, we would have reduced the number of steps by running the command against a directory to apply of the contents: `kubectl apply -f deployment/`.

### Method 2 : Using ArgoCD :

Install ArgoCD from the guide : [ArgoCD Installation guide](https://argo-cd.readthedocs.io/en/stable/getting_started/)

Create "NodePort" to expose the application to be accessible from the vagrant box to the Host machine

The YAML manifest for the NodePort service : [argocd-server-nodeport.yaml](https://raw.githubusercontent.com/khalil-Elf441/TechTrends-news-sharing-platform/master/argocd/argocd-server-nodeport.yaml)

```bash
kubectl apply -f https://raw.githubusercontent.com/khalil-Elf441/TechTrends-news-sharing-platform/master/argocd/argocd-server-nodeport.yaml
```

Deploy udaconnect Service using the yml file : [argocd-udaconnect.yaml](https://gist.githubusercontent.com/khalil-Elf441/fd2e80f7926f26d58b6de0bc28e44a82/raw/d8bf1bcd67f686a903fe913adeea28d90e358ccd/argocd-udaconnect.yaml)

```bash
kubectl apply -f https://gist.githubusercontent.com/khalil-Elf441/fd2e80f7926f26d58b6de0bc28e44a82/raw/d8bf1bcd67f686a903fe913adeea28d90e358ccd/argocd-udaconnect.yaml
```


### Note:
⚠ You must take this note into consideration regardless of the method you used.

The first time you run this project you will need to:

- :arrow_right: Seed the database with dummy data. Use the command `sh scripts/run_db_command.sh <POD_NAME>` against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`). Subsequent runs of `kubectl apply` for making changes to deployments or services shouldn't require you to seed the database again!

- :arrow_right: Create topic to Setup the messaging queue:
Use the command below against the `Kafka` pod

```
kubectl exec -it <POD_NAME> -- ./opt/bitnami/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 \
    --replication-factor 1 --partitions 1 \
    --topic locations
```

- :arrow_right: Run the `gRPC Server` in the `PersonService`:

Use the command below or run the HTTP query using ***postman > PS Run gRPC Server***

```
curl -X POST localhost:30001/admin/grpcstart
```

- :arrow_right: Run the `Kafka Consumer` in `LocationProcessor`:

Use the command below or run the HTTP query using ***postman > LP Start***

```
curl -X POST localhost:30010/admin/start
```

### Verifying it Works



Once the project is up and running, you should be able to see 8 deployments and 8 services in Kubernetes:

- `kubectl get pods` - should return as image below :

![pods](/docs/pods_screenshot.PNG "Pods")

- `kubectl get services` - should return as image below :

![services](/docs/services_screenshot.PNG "Services")

- If you are using ArgoCD (**optional**):

You should see in the [argoCD web interface](https://127.0.0.1:30007) as image below :

![Udaconnect ArgoCD](/docs/argocd_udaconnect.PNG "Udaconnect ArgoCD")

- To verify if `Kafka Consumer` is running in `LocationProcessor`:

Use the command below or run the HTTP query using ***postman > LP Status***

```
curl -X GET localhost:30010/admin/status
```

Should return message as `consumer is alive on $number`, where the $number is the number the Kafka consumer pid.

:information_source: If you get any another message error you can destroy the Kafka consumer : `curl -X POST localhost:30010/admin/destroy` and start it again.

-  Web app frontend <br/>

<img src="/docs/frontend-app.PNG" width="609" height="754" />

These pages should also load on your web browser:
* `http://localhost:30006/` - Frontend ReactJS Application
* `http://localhost:30001/` - OpenAPI Documentation for PersonsService API
* `http://localhost:30001/api/` - Base path for PersonsService API
* `http://localhost:30001/admin/` - Base admin interface for PersonsService
* `http://localhost:30002/` - OpenAPI Documentation for LocationService API
* `http://localhost:30002/api/` - Base path for LocationService API
* `http://localhost:30003/` - OpenAPI Documentation for ConnectionService API
* `http://localhost:30003/api/` - Base path for ConnectionService API
* `http://localhost:30010/admin/` - Base admin interface for LocationProcessor

#### Deployment Note
You may notice the odd port numbers being served to `localhost`. [By default, Kubernetes services are only exposed to one another in an internal network](https://kubernetes.io/docs/concepts/services-networking/service/). This means that `udaconnect` Services can talk to one another. For us to connect to the cluster as an "outsider", we need to a way to expose these services to `localhost`.

Connections to the Kubernetes services have been set up through a [NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport). (While we would use a technology like an [Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) to expose our Kubernetes services in deployment, a NodePort will suffice for development.)

## Development
### New Services
New services can be created inside of the `modules/` subfolder. You can choose to write something new with Flask, copy and rework the `modules/api` service into something new, or just create a very simple Python application.

As a reminder, each module should have:
1. `Dockerfile`
2. Its own corresponding DockerHub repository
3. `requirements.txt` for `pip` packages
4. `__init__.py`

### Docker Images

the built docker images are available in the dockerhub repository : [khalilelf441](https://hub.docker.com/repository/docker/khalilelf441 "khalilelf441 DockerHub") 

## Configs and Secrets
In `deployment/db-secret.yaml`, the secret variable is `d293aW1zb3NlY3VyZQ==`. The value is simply encoded and not encrypted -- this is ***not*** secure! Anyone can decode it to see what it is.
```bash
# Decodes the value into plaintext
echo "d293aW1zb3NlY3VyZQ==" | base64 -d

# Encodes the value to base64 encoding. K8s expects your secrets passed in with base64
echo "hotdogsfordinner" | base64
```
This is okay for development against an exclusively local environment and we want to keep the setup simple so that you can focus on the project tasks. However, in practice we should not commit our code with secret values into our repository. A CI/CD pipeline can help prevent that.

## PostgreSQL Database
The database uses a plug-in named PostGIS that supports geographic queries. It introduces `GEOMETRY` types and functions that we leverage to calculate distance between `ST_POINT`'s which represent latitude and longitude.

_You may find it helpful to be able to connect to the database_. In general, most of the database complexity is abstracted from you. The Docker container in the starter should be configured with PostGIS. Seed scripts are provided to set up the database table and some rows.
### Database Connection
While the Kubernetes service for `postgres` is running (you can use `kubectl get services` to check), you can expose the service to connect locally:
```bash
kubectl port-forward svc/postgres 5432:5432
```
This will enable you to connect to the database at `localhost`. You should then be able to connect to `postgresql://localhost:5432/geoconnections`. This is assuming you use the built-in values in the deployment config map.
### Software
To manually connect to the database, you will need software compatible with PostgreSQL.
* CLI users will find [psql](http://postgresguide.com/utilities/psql.html) to be the industry standard.
* GUI users will find [pgAdmin](https://www.pgadmin.org/) to be a popular open-source solution.

:congratulations:
