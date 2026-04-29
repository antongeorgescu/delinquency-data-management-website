#!/usr/bin/env pwsh
<#
.SYNOPSIS
  Deploy delinquency-website to Azure Container Apps.

.DESCRIPTION
  Builds both Docker images, pushes to Azure Container Registry, then
  creates/updates Azure Container Apps (API + Web) with a shared Azure
  Files volume for the SQLite database.

.PARAMETER ResourceGroup
  Azure resource group name (created if it doesn't exist).

.PARAMETER Location
  Azure region, e.g. canadacentral, eastus.

.PARAMETER AcrName
  Azure Container Registry name (globally unique, lowercase, 5-50 chars).

.EXAMPLE
  .\deploy-azure.ps1 -ResourceGroup "delinquency-rg" -Location "canadacentral" -AcrName "delinquencyacr"
#>
param(
    [string]$ResourceGroup = "alvaz-poc-rg",
    [Parameter(Mandatory)][string]$Location,
    [Parameter(Mandatory)][string]$AcrName
)

$ErrorActionPreference = "Stop"

$APP_ENV      = "delinquency-env"
$API_APP      = "delinquency-api"
$WEB_APP      = "delinquency-web"
$STORAGE_NAME = "delinquencydb"
$FILE_SHARE   = "dbshare"
$MOUNT_NAME   = "dbvolume"

Write-Host "`n=== 1. Login check ===" -ForegroundColor Cyan
$TENANT_ID       = "31a83df6-b522-46ac-bcbe-85c3d12e2232"
$SUBSCRIPTION_ID = "bfb59099-69db-4d2b-887e-abcf6ccdb5c4"

$savedPref = $ErrorActionPreference
$ErrorActionPreference = "Continue"

# Only login if not already on the correct tenant
$currentAccount = az account show --only-show-errors 2>$null | ConvertFrom-Json
if (-not $currentAccount -or $currentAccount.tenantId -ne $TENANT_ID) {
    Write-Host "Logging in to tenant $TENANT_ID ..." -ForegroundColor Yellow
    az login --tenant $TENANT_ID --only-show-errors
    if ($LASTEXITCODE -ne 0) {
        $ErrorActionPreference = $savedPref
        Write-Error "Login failed."
        exit 1
    }
} else {
    Write-Host "Already logged in as $($currentAccount.user.name)" -ForegroundColor Green
}

$ErrorActionPreference = $savedPref

Write-Host "Setting subscription to sandbox ($SUBSCRIPTION_ID) ..." -ForegroundColor Yellow
az account set --subscription $SUBSCRIPTION_ID --only-show-errors
$activeName = az account show --query "name" -o tsv --only-show-errors
Write-Host "Active subscription: $activeName" -ForegroundColor Green

Write-Host "`n=== 2. Resource group ===" -ForegroundColor Cyan
$rgExists = (az group exists --name $ResourceGroup --subscription $SUBSCRIPTION_ID)
if ($rgExists -eq "true") {
    Write-Host "Using existing resource group: $ResourceGroup"
} else {
    az group create --name $ResourceGroup --location $Location --subscription $SUBSCRIPTION_ID | Out-Null
    Write-Host "Created resource group: $ResourceGroup"
}

Write-Host "`n=== 3. Azure Container Registry ===" -ForegroundColor Cyan
az acr create --name $AcrName --resource-group $ResourceGroup --sku Basic --admin-enabled true --subscription $SUBSCRIPTION_ID | Out-Null
$ACR_SERVER = (az acr show --name $AcrName --query loginServer -o tsv --subscription $SUBSCRIPTION_ID)
Write-Host "ACR: $ACR_SERVER"

Write-Host "`n=== 4. Build & push images ===" -ForegroundColor Cyan
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

az acr build --registry $AcrName --image "${API_APP}:latest" "$SCRIPT_DIR\src\api" --subscription $SUBSCRIPTION_ID
az acr build --registry $AcrName --image "${WEB_APP}:latest" "$SCRIPT_DIR\src\web" --subscription $SUBSCRIPTION_ID

Write-Host "`n=== 5. Azure Storage (SQLite volume) ===" -ForegroundColor Cyan
az storage account create `
    --name $STORAGE_NAME `
    --resource-group $ResourceGroup `
    --location $Location `
    --sku Standard_LRS `
    --subscription $SUBSCRIPTION_ID | Out-Null

$STORAGE_KEY = (az storage account keys list --account-name $STORAGE_NAME --query "[0].value" -o tsv --subscription $SUBSCRIPTION_ID)

az storage share create `
    --name $FILE_SHARE `
    --account-name $STORAGE_NAME `
    --account-key $STORAGE_KEY | Out-Null
Write-Host "File share: $FILE_SHARE"

Write-Host "`n=== 6. Container Apps Environment ===" -ForegroundColor Cyan
az containerapp env create `
    --name $APP_ENV `
    --resource-group $ResourceGroup `
    --location $Location `
    --subscription $SUBSCRIPTION_ID | Out-Null

az containerapp env storage set `
    --name $APP_ENV `
    --resource-group $ResourceGroup `
    --storage-name $MOUNT_NAME `
    --azure-file-account-name $STORAGE_NAME `
    --azure-file-account-key $STORAGE_KEY `
    --azure-file-share-name $FILE_SHARE `
    --access-mode ReadWrite `
    --subscription $SUBSCRIPTION_ID | Out-Null
Write-Host "Storage mount configured"

Write-Host "`n=== 7. Deploy API Container App ===" -ForegroundColor Cyan
$ACR_PASS = (az acr credential show --name $AcrName --query "passwords[0].value" -o tsv --subscription $SUBSCRIPTION_ID)

az containerapp create `
    --name $API_APP `
    --resource-group $ResourceGroup `
    --environment $APP_ENV `
    --image "${ACR_SERVER}/${API_APP}:latest" `
    --registry-server $ACR_SERVER `
    --registry-username $AcrName `
    --registry-password $ACR_PASS `
    --target-port 5000 `
    --ingress internal `
    --cpu 1 --memory 2Gi `
    --min-replicas 1 --max-replicas 3 `
    --env-vars "DB_PATH=/data/student_loan_data.db" `
    --subscription $SUBSCRIPTION_ID | Out-Null

Write-Host "`n=== 8. Deploy Web Container App ===" -ForegroundColor Cyan
$API_FQDN = (az containerapp show --name $API_APP --resource-group $ResourceGroup --query "properties.configuration.ingress.fqdn" -o tsv --subscription $SUBSCRIPTION_ID)

az containerapp create `
    --name $WEB_APP `
    --resource-group $ResourceGroup `
    --environment $APP_ENV `
    --image "${ACR_SERVER}/${WEB_APP}:latest" `
    --registry-server $ACR_SERVER `
    --registry-username $AcrName `
    --registry-password $ACR_PASS `
    --target-port 80 `
    --ingress external `
    --cpu 0.5 --memory 1Gi `
    --min-replicas 1 --max-replicas 5 `
    --subscription $SUBSCRIPTION_ID | Out-Null

$WEB_URL = (az containerapp show --name $WEB_APP --resource-group $ResourceGroup --query "properties.configuration.ingress.fqdn" -o tsv --subscription $SUBSCRIPTION_ID)

Write-Host "`n=== Deployment complete! ===" -ForegroundColor Green
Write-Host "Web UI:  https://$WEB_URL" -ForegroundColor Cyan
Write-Host "API:     internal only (proxied via nginx in the web container)" -ForegroundColor Yellow
Write-Host "`nShare this URL with your team: https://$WEB_URL`n"
