# Terraform and Azure VM Setup with Docker, Elasticsearch, and Python Faker

## Project Description

This project is a basic example demonstrating the integration of Terraform, Azure VM, Docker, Elasticsearch, and Python Faker. The project includes:

- **Terraform** for infrastructure as code (IaC) to provision and manage an Azure Virtual Machine.
- **Azure VM** as the compute resource for running Docker and Elasticsearch.
- **Docker** for containerizing and managing Elasticsearch.
- **Elasticsearch** for search and analytics engine setup and management on the Azure VM.
- **Python Faker** for generating fake data to populate the Elasticsearch index for testing and demonstration purposes.

## Key Features

1. **Infrastructure as Code (IaC)**: Using Terraform scripts to provision an Azure Virtual Machine.
2. **Docker Setup**: Installing and configuring Docker on the Azure VM to containerize Elasticsearch.
3. **Elasticsearch Setup**: Installing and configuring Elasticsearch within Docker on the Azure VM.
4. **Data Generation**: Using Python Faker to generate realistic fake data for populating Elasticsearch.
5. **Monitoring and Management**: Instructions for monitoring Elasticsearch performance and logs using Azure tools.

## How to Use

1. Clone the repository.
2. Follow the instructions in the `README.md` to initialize Terraform and set up the Azure VM.
3. Install and configure Docker on the VM.
4. Set up Elasticsearch in a Docker container on the VM.
5. Use the Python scripts provided to generate and index fake data in Elasticsearch.
6. Monitor the Elasticsearch instance using the provided Azure monitoring tools and commands.

## Prerequisites

- Azure account
- Terraform installed
- SSH access to the Azure VM
- Docker installed on the Azure VM
- Basic knowledge of Elasticsearch and Python

## Getting Started


## Step 1: Set Up Azure Account and Prerequisites

Before starting with the setup of the Elasticsearch cluster on Azure, ensure you have the following prerequisites:

1. **Azure Account**: Ensure you have an active Azure subscription. The free tier should be sufficient for this exercise.

2. **Azure CLI**: Install the Azure CLI on your Mac.
    ```bash
    brew update && brew install azure-cli
    ```

3. **Terraform**: Install Terraform on your Mac.
    ```bash
    brew tap hashicorp/tap
    brew install hashicorp/tap/terraform
    ```

4. **Docker**: Install Docker Desktop for Mac.
    ```bash
    brew install --cask docker
    ```

### Login to Azure

1. Open your terminal and log in to Azure:
    ```bash
    az login
    ```

    This command will open a web browser window where you can log in with your Azure credentials. Once logged in, you can close the browser window.

### Create a Resource Group

1. Create a resource group where you will deploy your resources. Replace `myResourceGroup` and `eastus` with your preferred resource group name and location:
    ```bash
    az group create --name myResourceGroup --location eastus
    ```

    This command creates a resource group in the specified location.

Now, you have set up the necessary prerequisites and created a resource group for deploying the Elasticsearch cluster.

### Step 2: Initialize and Apply Terraform Configuration

1. **Initialize Terraform:**
    ```bash
    terraform init
    ```

2. **Apply the Configuration:**
    ```bash
    terraform apply
    ```
    Confirm the apply action by typing `yes` when prompted.
    It should start building the VM in your Azure Account.

### Step 3: Install and Configure Docker and Elasticsearch on the VM


If your virtual machine does not have a public IP address assigned, you will need to create and associate one. Here are the steps to assign a public IP address to your Azure VM
### Steps to Assign a Public IP Address
   1. **Create a Public IP Address:**
      
      ```bash 
      az network public-ip create --resource-group <RESOURCE_GROUP> --name <PUBLIC_IP_NAME> --allocation-method Dynamic
      ```
      Replace <RESOURCE_GROUP> with your resource group name and <PUBLIC_IP_NAME> with a name for your new public IP address.

   2. **Find the Network Interface of the VM:**
       ```bash
       NIC_ID=$(az vm show --resource-group <RESOURCE_GROUP> --name <VM_NAME> --query "networkProfile.networkInterfaces[0].id" --output tsv)
       ```
   3. **Find the Name of the Network Interface and IP Configuration:**
       ```bash
       NIC_NAME=$(az network nic show --ids $NIC_ID --query "name" --output tsv)
       IP_CONFIG_NAME=$(az network nic show --ids $NIC_ID --query "ipConfigurations[0].name" --output tsv)
       ```

   4. **Associate the Public IP Address with the Network Interface:**
       ```bash
       az network nic ip-config update --resource-group <RESOURCE_GROUP> --nic-name $NIC_NAME --name $IP_CONFIG_NAME --public-ip-address <PUBLIC_IP_NAME>
       ```

       You need to replace <RESOURCE_GROUP>, <NIC_NAME>, <IP_CONFIG_NAME>, and <PUBLIC_IP_NAME> with the appropriate values. You can find <NIC_NAME> and <IP_CONFIG_NAME> from the VM's network interface configuration in the Azure portal or by querying:

       ```bash 
       az network nic show --ids <NIC_ID> --query "{NICName:name, IPConfig:ipConfigurations[0].name}" --output json
       ```
    
   5. **Verify the Public IP Address:**
       
       ```bash
       az vm list-ip-addresses --name <VM_NAME> --resource-group <RESOURCE_GROUP> --output table
       ```
        This process will associate a new public IP address with your VM, allowing you to SSH into it using the new public IP address.
### Step 3: Continued to install and configure Docker and Elasticsearch    
             
1. **SSH in to Azure:**

    ```bash
    ssh azureuser@<public-ip>
    ```
 2. **Install Docker:**

    ```bash
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker ${USER}
    ```

 3. **Logout and Login to Apply Docker Group Changes:**

    ```bash
    exit
    ssh azureuser@<public-ip-of-your-vm>
    ```

 4. **Verify Docker Installation:**

    ```bash
    docker --version
    ```
    You should see the Docker version information, confirming that Docker is installed and running.

 5. **Install Docker Compose:**

    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```

    ```bash
    sudo chmod +x /usr/local/bin/docker-compose
    docker-compose --version
    ```
    This command downloads Docker Compose and makes it executable. The version command should confirm the installation.

 6. **Run Docker Compose File:**

    Ensure you are in the correct directory (e.g., /home/azureuser or wherever you want to store your configuration files).  Create the docker-compose.yml file on the VM which will set up the Elastic Search instance.

    ```bash
    sudo docker-compose.yml
    ```

 7. **Start the Docker container:**
    ```bash
    docker-compose up -d
    ```

 8. **Verify Elasticsearch is Running so check docker containers:**
    Check Docker Containers:

    ```bash
    docker ps
    ```
    You should see the Elasticsearch container running.

 9. **Verify Elasticsearch Access:**

    From the VM, you can test if Elasticsearch is running:

    ```bash
    curl -X GET "localhost:9200/"
    ```
    By following these steps, you should be able to successfully set up and run Elasticsearch on your Azure VM using Docker and Docker Compose.

### Step 4: Populate Elasticsearch with Fake Data via Faker
        
Use Python and Faker to generate fake data.

 1.  **SSH into the Azure VM (if not already connected):**

        ```bash
        ssh azureuser@<public-ip-of-your-vm>
        ```

2.   **Install Python and Required Libraries:**

        Ensure Python and pip are installed. If not, install them:

        ```bash
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip
        ```

3.  **Install the required Python libraries:**

    ```bash
    pip3 install faker elasticsearch
    ```

4.  **Create the Python Script to Generate Fake Data:**

    Add the content to populate_data.py

    ```bash
    nano populate_data.py
    ```

5. **Run the Python Script:**

    Execute the script to populate Elasticsearch with fake data

    ```bash
    python3 populate_data.py
    ```

6.  **Verify the Data in Elasticsearch:**

    You can verify that the data has been populated by querying Elasticsearch:

    ```bash
    curl -X GET "localhost:9200/people/_search?pretty"
    ```

    
<br>
<br>

**That should be it!!! Below are some things you can try and explore to learn more about Managment and Monitoring ElasticSearch instances.**

<br>
<br>




# Elasticsearch Management and Monitoring Guide
## 1. Updating Elasticsearch Instance on the VM

### SSH into the VM:
```bash
ssh azureuser@<public-ip>
```

### Stop the Elasticsearch service:
```bash
sudo systemctl stop elasticsearch
```

### Update Elasticsearch:
Follow the official Elasticsearch documentation for your specific update. For example, if using APT:
```bash
sudo apt-get update
sudo apt-get install elasticsearch
```

### Restart the Elasticsearch service:
```bash
sudo systemctl start elasticsearch
```

### Verify the update:
```bash
curl -X GET "localhost:9200"
```

## 2. Reverting to a Previous Terraform Configuration

### Initialize Terraform (if not already initialized):
```bash
terraform init
```

### Apply the previous configuration:
Make sure your Terraform configuration files reflect the desired state and then run:
```bash
terraform apply
```
Confirm the apply action by typing `yes` when prompted.

### If using version control:
Checkout the previous version of your Terraform files.
```bash
git checkout <previous-commit-id>
terraform apply
```

## 3. Managing Shards in Elasticsearch

### Check current shard allocation:
```bash
curl -X GET "localhost:9200/_cat/shards?v"
```

### Reallocate shards (example to move a shard):
```bash
curl -X POST "localhost:9200/_cluster/reroute" -H 'Content-Type: application/json' -d'
{
  "commands": [
    {
      "move": {
        "index": "index_name",
        "shard": 0,
        "from_node": "node1",
        "to_node": "node2"
      }
    }
  ]
}'
```

### Break up shards (increase number of primary shards):
This usually requires reindexing. You can use the `_reindex` API to copy data to a new index with more shards.

## 4. Checking Elasticsearch Status

### Check cluster health:
```bash
curl -X GET "localhost:9200/_cluster/health?pretty"
```
Status indicators:
- `green`: All primary and replica shards are active.
- `yellow`: All primary shards are active, but some/all replica shards are not allocated.
- `red`: Some/all primary shards are not active.

## 5. Monitoring Elasticsearch Performance and Logs in Azure

### Azure Monitor:
Use Azure Monitor to track the performance metrics of your Elasticsearch VM. Navigate to the Azure portal, go to your VM resource, and select "Metrics" to visualize CPU, memory, disk I/O, and network metrics.

### Azure Log Analytics:
Configure Azure Log Analytics to collect logs from your VM. Go to the Log Analytics workspace in the Azure portal, and set up log collection from your VM. Use queries in the workspace to analyze the logs.

### Setting up Diagnostic Settings:
Enable diagnostic settings for your VM to send performance counters, event logs, and other monitoring data to Azure Monitor.

### Check Elasticsearch logs:
```bash
sudo journalctl -u elasticsearch
```

### Check VM logs in Azure Log Analytics:
Use Kusto Query Language (KQL) in Azure Log Analytics to query logs:
```kql
Search "Elasticsearch" | where ResourceId == "<Your VM Resource ID>"
```
<br>
<br>
<br>

# Scenarios and Answers for Terraform and Elasticsearch

## Scenario 1: Increasing the Number of Elasticsearch Nodes

**Question:** You currently have a single Elasticsearch node set up using Terraform. Due to increased load, you need to add more nodes to your cluster. How would you modify your Terraform configuration to achieve this?

**Answer:**
You need to modify your Terraform configuration to add additional VM instances and configure them to join the Elasticsearch cluster. Here's a basic example of how you can scale from one to three nodes:

### Current Terraform Configuration (Single Node):
```hcl
resource "azurerm_virtual_machine" "es" {
  count                = 1
  name                 = "es-${count.index}"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  network_interface_ids = [azurerm_network_interface.es.id]
  vm_size              = "Standard_DS2_v2"

  # Other VM configuration...
}
```

### Modified Configuration (Multiple Nodes):
```hcl
resource "azurerm_virtual_machine" "es" {
  count                = 3
  name                 = "es-${count.index}"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  network_interface_ids = [azurerm_network_interface.es[count.index].id]
  vm_size              = "Standard_DS2_v2"

  # Other VM configuration...
}

resource "azurerm_network_interface" "es" {
  count               = 3
  name                = "es-nic-${count.index}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Other NIC configuration...
}
```

## Scenario 2: Handling a Failed Shard

**Question:** One of your Elasticsearch shards is failing, and you need to reallocate it to a different node. How would you approach this problem using both Elasticsearch API and Terraform?

**Answer:**

### Step 1: Using Elasticsearch API to Reallocate the Shard:

**Identify the Failed Shard:**
```bash
curl -X GET "localhost:9200/_cat/shards?v"
```

**Reallocate the Shard:**
```bash
curl -X POST "localhost:9200/_cluster/reroute" -H 'Content-Type: application/json' -d'
{
  "commands": [
    {
      "move": {
        "index": "index_name",
        "shard": 0,
        "from_node": "node1",
        "to_node": "node2"
      }
    }
  ]
}'
```

### Step 2: Using Terraform to Prevent Future Failures:

Modify your Terraform configuration to add more redundancy and improve fault tolerance. This might involve adding more nodes, increasing the number of replicas, or improving node specifications.

**Increase the Number of Replicas:**
```hcl
resource "elasticsearch_index" "example" {
  name = "example-index"

  settings = jsonencode({
    number_of_replicas = 2
  })
}
```

**Ensure High Availability by Distributing Nodes Across Availability Zones:**
```hcl
resource "azurerm_virtual_machine" "es" {
  count                = 3
  name                 = "es-${count.index}"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  network_interface_ids = [azurerm_network_interface.es[count.index].id]
  vm_size              = "Standard_DS2_v2"
  availability_zone    = count.index + 1

  # Other VM configuration...
}
```

## Scenario 3: Monitoring and Alerting

**Question:** How would you set up monitoring and alerting for your Elasticsearch cluster using Terraform and Azure Monitor?

**Answer:**

**Set Up Log Analytics Workspace:**
```hcl
resource "azurerm_log_analytics_workspace" "example" {
  name                = "loganalyticsworkspace"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}
```

**Enable Diagnostic Settings for Elasticsearch VM:**
```hcl
resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "example-diagnostics"
  target_resource_id = azurerm_virtual_machine.es[0].id

  log_analytics_workspace_id = azurerm_log_analytics_workspace.example.id

  logs {
    category = "AllLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days    = 7
    }
  }

  metrics {
    category = "AllMetrics"
    enabled  = true
    retention_policy {
      enabled = true
      days    = 7
    }
  }
}
```

**Create Alerts Based on Logs and Metrics:**
```hcl
resource "azurerm_monitor_metric_alert" "example" {
  name                = "example-metric-alert"
  resource_group_name = azurerm_resource_group.example.name
  scopes              = [azurerm_virtual_machine.es[0].id]
  description         = "Alerts when CPU usage is high"
  criteria {
    metric_namespace = "Microsoft.Compute/virtualMachines"
    metric_name      = "Percentage CPU"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 80
  }
  action {
    action_group_id = azurerm_monitor_action_group.example.id
  }
}
```
<br>
These scenarios and corresponding Terraform configurations should give you a solid foundation.




