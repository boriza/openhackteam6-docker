# setup Azure Container Registry (docker hub is an option as well)

az group create --name openhackRG --location westus2
az acr create --resource-group openhackRG --name ohACR --sku Basic
az acr login --name ohACR
#gear is the name of the docker image on the local machine
docker tag gear ohacr.azurecr.io/gear:v1

az acr login --name ohACR --username
docker push ohacr.azurecr.io/gear:v1

az acr repository list --name <acrName> --output table
az acr repository show-tags --name <acrName> --repository azure-vote-front --output table


# deploy to Azure App Service - Container
