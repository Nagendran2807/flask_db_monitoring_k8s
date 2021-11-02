### Running Flask and Postgres on Kubernetes

~~Making a Flask app using a Postgresql database and deploying to Minikube~~

#### Prereq's
1. docker
2. docker-compose
3. minikube

### Tools Used
1. docker & docker-compose
2. Python Flask
3. Postgres
4. Minikube - To deploy apps in K8s

### Docker (Test the application locally)

Build the images and spin up the containers:

```sh
$ docker-compose up -d --build
```


### CRUD operation done 
1. Create New Team (CREATE)
2. Get the Team details (READ)
3. Edit existing Team (UPDATE)
4. Delete the team (DELETE)


1. [http://localhost:5010](http://localhost:5010)
2. [http://localhost:hello/DevOpsGuy](http://localhost:5010/hello/DevOpsGuy)

Note:
-------
TeamName & players box support string

### Kubernetes

#### Minikube

Install and run [Minikube](https://kubernetes.io/docs/setup/minikube/):

1. Install a [Hypervisor](https://kubernetes.io/docs/tasks/tools/install-minikube/#install-a-hypervisor) (like [VirtualBox](https://www.virtualbox.org/wiki/Downloads) or [HyperKit](https://github.com/moby/hyperkit)) to manage virtual machines
1. Install and Set Up [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to deploy and manage apps on Kubernetes
1. Install [Minikube](https://github.com/kubernetes/minikube/releases)

Start the cluster:

```sh
$ minikube start
$ minikube dashboard
```

#### Volume

Create the volume, Volume Claim & Secret 

```sh
$ kubectl apply -f ./kubernetes/postgres/postgres_storage_config.yml
```

#### Postgres

Create deployment & Service 

```sh
$ kubectl apply -f ./kubernetes/postgres/postgres.yml
```

Create the database:

```sh
$ kubectl get pods
$ pod_name=$(kubectl get po -l db=postgres -o jsonpath="{.items[0].metadata.name}")
$ kubectl exec -it $pod_name -it -- createdb -U postgres demo_db
$ kubectl exec -it $pod_name -it -- psql -U postgres
kubectl exec -it $pod_name -i -- psql -U postgres <<EOF
ALTER USER postgres WITH PASSWORD 'admin123';
EOF
```

#### Flask

Build and push the image to Docker Hub:

```sh
$ docker build -t <hub-user>/<repo-name>[:<tag>] ./services/flask
$ docker push <hub-user>/<repo-name>[:<tag>]

$ docker build -t crazy28/flask-kubernetes:1.0 ./services/flask
$ docker push crazy28/flask-kubernetes:1.0
```

Create the deployment & service :

```sh
$ kubectl apply -f ./kubernetes/flask/flask.yml
```

Add entry to */etc/hosts* file:

```
<MINIKUBE_IP> hello.world
```



###### Monitoring  #############

### prereq's
1. helm 

``` sh
$ kubectl create ns monitoring
$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
$ helm repo add grafana https://grafana.github.io/helm-charts
```

```sh
helm install prometheus prometheus-community/prometheus
helm install grafana stable/grafana
```

```sh
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

bootstrap
6417
```sh
```

![Promethus Architecture](images/prometheus_intro.png)

####  Cheat Commands ####
``` sh
minikube image load  <image-nme>  #### push local docker images to minikube 

psql -h localhost -U postgres -d postgres -p 5432   ### connect ppostgresql

```

#### Theoretical part ####
Why SQLAlchemy...?
SQLAlchemy offers several benefits over the raw SQL approach, including:

Cleaner code: Having SQL code as Python strings gets messy pretty quickly,
More secure code: Using SQLAlchemy's ORM functionalities can help mitigate against vulnerabilities such as SQL injection,
Simpler logic: SQLAlchemy allows us to abstract all of our database logic into Python objects. Instead of having to think on a table, row, and column level, we can consider everything on a class, instance, and attribute level.

Helm should be used when involve CI/CD in k8s...
Helm allows us to bundle related Kubernetes objects into charts and treat them as a single unit of deployment referred to as release 
## helm benefits ##
1. We can rollback to a previous release with a single helm command.
2. It makes the deployment highly configurable.
3. we can use the same chart for deploying on multiple environments like stag/prod or multiple cloud providers.


## continuous delivery ##
Either use Argo CD (or) GitLab

![High Level Process Flow](images/CI-CD-k8s.png)

## Argo CD ##
Argo uses git repositories as a reference for the target state of your app and the target deployment environments. It will synchronize your desired app state with each of the target environments that you’ll define.
Why Argo CD...?
Application deployment and lifecycle management should be automated, auditable and easy to understand...

Top features
1. it provides continuous monitoring of your deployed apps
2. rollback/roll-anywhere-in-the-git-repository features
3. it ships with webhook support (BitBucket, GitLab, GitHub)
4. it provides sync, presync and postsync hooks for complex app rollouts
5. it provides SSO integration (GitLab, OIDC, Microsoft, LinkedIn, SAML 2.0, LDAP)
6. you can use it alone or as a component of an existing setup of pipeline tools

## GitLab ##
Auto DevOps provides you with pre-built CI/CD configuration, so you can automatically identify, build, test, deploy and further monitor your Kubernetes apps
1. it works with any Kubernetes cluster (you won’t depend on GitLab’s infrastructure)
2. it allows you to use Containers as a Service or a self-hosted Kubernetes cluster on any public cloud
3. it provides you with CI support out of the box
4. it allows you to choose between its auto-deploy component for Kubernetes and Helm charts
Overall: GitLab will simplify and streamline your entire Kubernerted app development cycle

## Should follow branching strategies ##


##### How we deploy and run application across multiple regions #####

## Tools Required
Gitlab
Terraform


Step 1: Modularized our components such as VPC, EC2, lambda, S3 etc using terraform as much as possible to meet our demands...
Step 2: Provisioning Gitlab runner auto scaling with AWS Spot instances to reduce the cost... Configure the Gitlab Runner either make it as a template and use service catalog to deploy multiple regions & account wherever required
Step 3: Create a repo in Gitlab
Step 4: For backend, either we can use Gitlab Backend or AWS S3 backend 
Note to remember when select Gitlab Backend...:  People can trigger the pipline but able to execute terraform apply command who have maintainer access role in gitlab

Step 5: In s3, state file could then be located at <bucket>/<workspace_key_prefix>/<workspace>/<key>. If we substitute workspace with ap-southeast-1 or ap-southeast-2, if we substitute the variables workspace_key_prefix with product-a and key with terraform.tfstate, we end up with state files stored as:

This sets up grouping infrastructure states at a product/project level while establishing isolation between deployments to different regions while storing all those states conveniently in one place

## Approach ##
Using the terraform module and backend systems, the infrastructure-as-source code repository layout & Terraform backend configuration snippet described in the section provides us with a way to:

establish a structure in which common or a product/project's infrastructure is templatised for reuse across various enviroments
fine tune product/project's infrastructure at an environment level while even adding environment specific infrastructure for those non-ideal cases
Maintain state at a region level so that we could have better isolation, canary deploy, etc

![Sample Tree Structure](images/s3_structure.png)

working with the setup
```sh
terraform init
terraform workspace list  # list workspaces
terraform workspace new ap-southeast-2  ## create new workspace if not exist
terraform workspace select ap-southeast-2   ## select a workspace
terraform plan -var-file=ap-southeast-2.tfvars
terraform apply -var-file=ap-southeast-2.tfvars
```

Repeat for other regions
---------------------------
```sh
terraform workspace new ap-southeast-1
terraform workspace select ap-southeast-1 
terraform plan -var-file=ap-southeast-1.tfvars
terraform apply -var-file=ap-southeast-1.tfvars
```

