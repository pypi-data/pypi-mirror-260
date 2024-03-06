# Define Terraform backend configuration here
terraform {
  backend "azurerm" {
    
    storage_account_name = var.storage_account_name
    container_name       = var.container_name
    key                  = var.key

  }
}
