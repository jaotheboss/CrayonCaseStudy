# Crayon Case Study

## TODO:
- [x] Install ArgoCD into Docker K8s. Test out the sync up. 

## Installation
1. Run `pip install -r requirements.txt`
2. Clone and change directory with `git clone https://github.com/NicolasHug/surprise.git` and `cd surprise`
3. Run setup `python setup.py install`

## POC Components
1. Base Recommender service
   1. `docker build -t base-reco:0.1 -f Dockerfile.base_model .`
2. ML Recommender service
   1. `docker build -t ml-model:0.1 -f Dockerfile.mlmodel .`
3. Web App Interface
   1. `docker build -t web-app:0.1 -f Dockerfile.app . `

## Kubernetes Approach
Deploying the model and app:
1. `kubectl apply -f templates/basemodel.yaml`
2. `kubectl apply -f templates/webapp.yaml`
3. `kubectl set image deployment/basemodel base-reco=mlmodel:0.1`
   1. basemodel is the name of the deployment, and base-reco is the name of the container that is referenced in the deployment

## [ArgoCD Approach](https://prianjali98.medium.com/argo-cd-the-gitops-way-to-deploy-ml-applications-8de1555c1f8b)
1. Make changes in the template
2. `git add templates/basemodel.yaml` -> `git commit -m "changes to template"` -> `git push`
3. ArgoCD should be configred with self-healing and auto-pruning -> Sync with the templates found in the repo

## Context
Tasked to upgrade the BeerRecommender microservice in a Kubernetes (AKS) cluster to include a new machine learning model from `scitkit-surprise`. [General Understanding of Recommendation Engines](https://realpython.com/build-recommendation-engine-collaborative-filtering/)

Notes:
- The existing service is a REST API written in Go that fetches pre-defined recommendations from InventoryDB
- Goal is to replace the logic in this service to fetch recommendations generated by the machine learning model when referencing InventoryDB
- Principles:
  - As Un-Intrusive as Possible
  - MLOps for Retraining
  - Model Training Infrastructure
  - Automation through GitOps

Assumptions:
- The BeerRecommender service takes as input UserID and returns a list of ProductIDs.
- Because the service extracts recommendations from a pre-defined DB, I assume there is no Queue set up for the BeerRecommender service. But instead there is an Application Load Balancer to support hyperscaling of the service for high load volume from the website
- Current GitOps implementation uses the Pull method. Installing ArgoCD in AKS and having the controller sync with a GitOps repository. 
  - Pull method has less human action involved as compared to Push. This allows for a more predictable workflow, thus reducing human error.
  - Using GitHub repository as a single-source-of-truth 
  - Easier to rollback with a simple `git revert` or `git reset` and then allowing ArgoCD in k8s to sync the changes

Considerations:
- Do we want the model to be deployed within the same container as the Recommender Logic? This would mean that scaling would require multiple deployments of both the model and the Recommender Logic
  - Pros: Less infrastructure needed to set up. A one to one replacement of the Service (Docker container)
  - Cons: Would require building up the logic from scratch using the same programming language used for model deployment. More work needs to be done on the Application layer
- Or do we want to separately deploy the model in its own container and link the Recommender Logic and the model with a Queue (RabbitMQ?) This way we can create a K8s Deployment for the model for it to scale accordingly and perform inference according to the queue
  - Pros: Logic can remain as is with a tweak on function called for extraction recommendations. 
    - Easier to do blue-green deployment. Models hide behind an API Gateway. 
    - Easier to scale ML model servers
    - Works best especially if the recommendation system is a complex service. and ML is a small part
  - Cons: Extra Service needs to be created with a MQ provisioned. More work needs to be done on the IaaC level. 
- How do we want to perform caching? Locally within the container? Or within InventoryDB? Should we update the pre-defined recommendations with the ML generated recommendations? 

Helpful Links:
- https://medium.com/@rparundekar/deploying-ml-models-using-containers-in-three-ways-14745af94043
- https://itnext.io/gitops-pull-based-vs-push-based-959c50feca78
- https://technekey.com/canary-deployment-and-traffic-splitting-in-kubernetes/


## Steps to Demo
- Presentation should cover general understanding of the architecture and workflow
- Key thing to demo is MLOps workflow + ArgoCD
- MLOps workflow
  - Train up a new model
  - MLflow can be used for experimentation. Tracking of parameters and datasets used
  - There's currently a limitation to the flavours supported by MLflow
  - Save the models manually 
  - Create a Docker image with `Dockerfile.mlmodel` which requires "surprise", "data", "main" and "requirements_mlmodel"
- ArgoCD
  - Template in GitOps repository can be edited to reflect the use of the latest Docker image
  - Show that there is a change functionality