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
    brew tap hashicorptap
    brew install hashicorptapterraform
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
    sudo curl -L "https:github.comdockercomposereleasesdownload1.29.2docker-compose-$(uname -s)-$(uname -m)" -o usrlocalbindocker-compose
    ```

    ```bash
    sudo chmod +x usrlocalbindocker-compose
    docker-compose --version
    ```
    This command downloads Docker Compose and makes it executable. The version command should confirm the installation.

 6. **Run Docker Compose File:**

    Ensure you are in the correct directory (e.g., homeazureuser or wherever you want to store your configuration files).  Create the docker-compose.yml file on the VM which will set up the Elastic Search instance.

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
    curl -X GET "localhost:9200"
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
    curl -X GET "localhost:9200people_search?pretty"
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
curl -X GET "localhost:9200_catshards?v"
```

### Reallocate shards (example to move a shard):
```bash
curl -X POST "localhost:9200_clusterreroute" -H 'Content-Type: applicationjson' -d'
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
curl -X GET "localhost:9200_clusterhealth?pretty"
```
Status indicators:
- `green`: All primary and replica shards are active.
- `yellow`: All primary shards are active, but someall replica shards are not allocated.
- `red`: Someall primary shards are not active.

## 5. Monitoring Elasticsearch Performance and Logs in Azure

### Azure Monitor:
Use Azure Monitor to track the performance metrics of your Elasticsearch VM. Navigate to the Azure portal, go to your VM resource, and select "Metrics" to visualize CPU, memory, disk IO, and network metrics.

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
curl -X GET "localhost:9200_catshards?v"
```

**Reallocate the Shard:**
```bash
curl -X POST "localhost:9200_clusterreroute" -H 'Content-Type: applicationjson' -d'
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
    metric_namespace = "Microsoft.ComputevirtualMachines"
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

### Rebalance the Cluster:
Once the new nodes are added, you can use the Elasticsearch API to rebalance the shards across the new nodes:
```bash
curl -X POST "localhost:9200_clusterreroute?retry_failed"
```

## Scenario 2: Removing Nodes from the Cluster

**Question:** You need to decommission some of your Elasticsearch nodes to reduce costs. How would you modify your Terraform configuration to remove these nodes, and what steps would you take to ensure the shards are safely reallocated?

**Answer:**

### Current Terraform Configuration (Multiple Nodes):
```hcl
resource "azurerm_virtual_machine" "es" {
  count                = 5
  name                 = "es-${count.index}"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  network_interface_ids = [azurerm_network_interface.es[count.index].id]
  vm_size              = "Standard_DS2_v2"

  # Other VM configuration...
}

resource "azurerm_network_interface" "es" {
  count               = 5
  name                = "es-nic-${count.index}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Other NIC configuration...
}
```

### Modified Configuration (Reduced Nodes):
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

### Reallocate Shards:
Before applying the changes, reallocate shards away from the nodes you plan to remove:
```bash
curl -X POST "localhost:9200_clusterreroute" -H 'Content-Type: applicationjson' -d'
{
  "commands": [
    {
      "move": {
        "index": "index_name",
        "shard": 0,
        "from_node": "node4",
        "to_node": "node1"
      }
    },
    {
      "move": {
        "index": "index_name",
        "shard": 1,
        "from_node": "node4",
        "to_node": "node2"
      }
    }
  ]
}'
```

### Apply Terraform Changes:
```bash
terraform apply
```

## Scenario 3: Calculating Shards Based on Node Memory

**Question:** You need to calculate the optimal number of shards for your Elasticsearch cluster based on the memory allocated to each node. Each node has 32GB of RAM, and you want to allocate 50% of the memory to the heap. How would you determine the number of shards?

**Answer:**

### Determine Heap Size:
- Total RAM per node: 32GB
- Heap size per node: 50% of 32GB = 16GB

### Shard Size Recommendations:
- Recommended shard size: 10-40GB

### Calculate Number of Shards:
- Assuming an average shard size of 30GB, calculate the total number of shards the cluster can handle based on the available heap size.

### Example Calculation:
- Number of nodes: 5
- Total heap size: 5 nodes * 16GB = 80GB
- Average shard size: 30GB
- Total shards: 80GB  30GB ≈ 2.67 shards per node

### Final Number of Shards:
To simplify, allocate 2 shards per node initially, adjusting based on actual data size and performance:
```hcl
resource "elasticsearch_index" "example" {
  name = "example-index"

  settings = jsonencode({
    number_of_shards   = 10
    number_of_replicas = 1
  })
}
```

## Scenario 4: Monitoring and Alerting

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
    metric_namespace = "Microsoft.ComputevirtualMachines"
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


# Advanced Scenarios and Answers for Terraform and Elasticsearch

## Scenario 1: Calculating Additional Nodes for Increased Data Volume

**Question:** Your Elasticsearch cluster is currently handling 2TB of data with 10 nodes. Each node has 32GB of RAM and 16GB of heap allocated. Your data volume is expected to double to 4TB in the next month. How many additional nodes will you need to handle this increased data volume while maintaining the same shard size?

**Answer:**

1. **Current Setup:**
   - Data volume: 2TB
   - Number of nodes: 10
   - RAM per node: 32GB
   - Heap size per node: 16GB
   - Current shard size: Assume 200GB per node (2TB  10 nodes)

2. **Expected Data Volume:**
   - New data volume: 4TB
   - Desired shard size: 200GB per node

3. **Calculate Number of Nodes:**
   - Total data volume: 4TB (4000GB)
   - Shard size per node: 200GB
   - Number of nodes required: 4000GB  200GB per node = 20 nodes

4. **Additional Nodes Needed:**
   - Current nodes: 10
   - Additional nodes: 20 - 10 = 10 nodes

**Terraform Configuration (Scaling to 20 Nodes):**
```hcl
resource "azurerm_virtual_machine" "es" {
  count                = 20
  name                 = "es-${count.index}"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  network_interface_ids = [azurerm_network_interface.es[count.index].id]
  vm_size              = "Standard_DS2_v2"

  # Other VM configuration...
}

resource "azurerm_network_interface" "es" {
  count               = 20
  name                = "es-nic-${count.index}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Other NIC configuration...
}
```

## Scenario 2: Handling Uneven Shard Distribution

**Question:** You notice that some nodes in your Elasticsearch cluster are underutilized while others are overloaded. How would you rebalance the shards to achieve a more even distribution?

**Answer:**

1. **Check Current Shard Distribution:**
```bash
curl -X GET "localhost:9200_catshards?v"
```

2. **Rebalance Shards Using Elasticsearch API:**
```bash
curl -X POST "localhost:9200_clusterreroute" -H 'Content-Type: applicationjson' -d'
{
  "commands": [
    {
      "allocate_replica": {
        "index": "index_name",
        "shard": 0,
        "node": "underutilized_node"
      }
    },
    {
      "cancel": {
        "index": "index_name",
        "shard": 0,
        "node": "overloaded_node",
        "allow_primary": true
      }
    }
  ]
}'
```

3. **Monitor the Cluster:**
```bash
curl -X GET "localhost:9200_clusterhealth?pretty"
```

## Scenario 3: Advanced Monitoring and Auto-Scaling

**Question:** How would you set up auto-scaling for your Elasticsearch cluster using Terraform and Azure Monitor, ensuring that the cluster scales up or down based on CPU usage?

**Answer:**

1. **Set Up Log Analytics Workspace:**
```hcl
resource "azurerm_log_analytics_workspace" "example" {
  name                = "loganalyticsworkspace"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}
```

2. **Enable Diagnostic Settings for Elasticsearch VM:**
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

3. **Set Up Auto-Scaling Rules:**
```hcl
resource "azurerm_monitor_autoscale_setting" "example" {
  name                = "example-autoscale"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  target_resource_id  = azurerm_virtual_machine_scale_set.example.id

  profile {
    name = "defaultProfile"
    capacity {
      minimum = 1
      maximum = 10
      default = 3
    }

    rule {
      metric_trigger {
        metric_name        = "Percentage CPU"
        metric_resource_id = azurerm_virtual_machine_scale_set.example.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "GreaterThan"
        threshold          = 75
      }

      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = 1
        cooldown  = "PT5M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "Percentage CPU"
        metric_resource_id = azurerm_virtual_machine_scale_set.example.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "LessThan"
        threshold          = 25
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = 1
        cooldown  = "PT5M"
      }
    }
  }
}
```



## Scenario 4: Adjusting Shard Allocation for Indexing and Query Performance

**Question:** Your cluster is experiencing slow query performance due to the high load on certain indices. How would you adjust shard allocation to improve query performance?

**Answer:**

1. **Analyze Current Shard Allocation:**
```bash
curl -X GET "localhost:9200/_cat/shards?v"
```

2. **Adjust Index Settings:**
Increase the number of replicas for better query performance:
```bash
curl -X PUT "localhost:9200/index_name/_settings" -H 'Content-Type: application/json' -d'
{
  "index": {
    "number_of_replicas": 2
  }
}'
```

3. **Use the Reroute API to Rebalance Shards:**
```bash
curl -X POST "localhost:9200/_cluster/reroute" -H 'Content-Type: application/json' -d'
{
  "commands": [
    {
      "allocate_replica": {
        "index": "index_name",
        "shard": 0,
        "node": "node1"
      }
    },
    {
      "allocate_replica": {
        "index": "index_name",
        "shard": 1,
        "node": "node2"
      }
    }
  ]
}'
```

## Scenario 5: Handling Node Failure and Recovery

**Question:** One of your Elasticsearch nodes has failed, causing some primary shards to become unavailable. How would you handle this situation to recover the failed shards and ensure high availability?

**Answer:**

1. **Identify the Failed Shards:**
```bash
curl -X GET "localhost:9200/_cat/shards?v"
```

2. **Promote Replica Shards to Primary:**
```bash
curl -X POST "localhost:9200/_cluster/reroute" -H 'Content-Type: application/json' -d'
{
  "commands": [
    {
      "allocate_replica": {
        "index": "index_name",
        "shard": 0,
        "node": "node2"
      }
    }
  ]
}'
```

3. **Replace the Failed Node:**
   - Remove the failed node from the cluster configuration.
   - Add a new node to replace the failed one using Terraform.

**Terraform Configuration (Replacing a Node):**
```hcl
resource "azurerm_virtual_machine" "es" {
  count                = 10
  name                 = "es-${count.index}"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  network_interface_ids = [azurerm_network_interface.es[count.index].id]
  vm_size              = "Standard_DS2_v2"

  # Other VM configuration...
}

resource "azurerm_network_interface" "es" {
  count               = 10
  name                = "es-nic-${count.index}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Other NIC configuration...
}
```

name                = "es-nic-${count.index}"
<br>
location            = azurerm_resource_group.main.location
<br>
  resource_group_name = azurerm_resource_group.main.name

  # Other NIC configuration...


## Scenario 6: Checking Cluster Health and Status with cURL

**Question:** How do you check the health and status of your Elasticsearch cluster using cURL commands?

**Answer:**

1. **Check Cluster Health:**
```bash
curl -X GET "localhost:9200/_cluster/health?pretty"
```

2. **Check Cluster State:**
```bash
curl -X GET "localhost:9200/_cluster/state?pretty"
```

3. **Check Node Information:**
```bash
curl -X GET "localhost:9200/_nodes?pretty"
```

4. **Check Shard Allocation:**
```bash
curl -X GET "localhost:9200/_cat/shards?v"
```

5. **Check Index Health:**
```bash
curl -X GET "localhost:9200/_cat/indices?v"
```

6. **Check Pending Tasks:**
```bash
curl -X GET "localhost:9200/_cat/pending_tasks?v"
```

## Common cURL Commands for Elasticsearch

```bash
# Check cluster health
curl -X GET "localhost:9200/_cluster/health?pretty"

# Check cluster state
curl -X GET "localhost:9200/_cluster/state?pretty"

# Check node information
curl -X GET "localhost:9200/_nodes?pretty"

# Check shard allocation
curl -X GET "localhost:9200/_cat/shards?v"

# Check index health
curl -X GET "localhost:9200/_cat/indices?v"

# Check pending tasks
curl -X GET "localhost:9200/_cat/pending_tasks?v"

# Rebalance shards
curl -X POST "localhost:9200/_cluster/reroute" -H 'Content-Type: application/json' -d'
{
  "commands": [
    {
      "allocate_replica": {
        "index": "index_name",
        "shard": 0,
        "node": "target_node"
      }
    },
    {
      "cancel": {
        "index": "index_name",
        "shard": 0,
        "node": "source_node",
        "allow_primary": true
      }
    }
  ]
}'
```

## Commonly Used Fields and Terms

- **from_node**: The source node in shard allocation and reallocation.
- **to_node**: The target node in shard allocation and reallocation.
- **count.index**: Used in Terraform to index resources.
- **_cat API**: Elasticsearch API endpoint for quick access to cluster information.
- **cache**: Used to cache shards for faster access.
- **replica**: Copies of the primary shard used for fault tolerance and increased search throughput.
- **primary**: The original shard responsible for indexing and updating documents.

### Common Fields in Terraform
- **name**: The name of the resource.
- **location**: The geographic location of the resource.
- **resource_group_name**: The name of the resource group.
- **network_interface_ids**: The IDs of the network interfaces associated with the VM.
- **vm_size**: The size of the virtual machine.

### Common Terms in Elasticsearch
- **shard**: A basic unit of storage in Elasticsearch. Each index is divided into shards.
- **replica shard**: A copy of a primary shard. Provides redundancy and improves search performance.
- **primary shard**: The original shard that handles indexing operations.
- **allocation**: The process of assigning shards to nodes.
- **rebalancing**: The process of redistributing shards across the nodes in a cluster to ensure even distribution.

### Useful cURL Commands
```bash
# Check Elasticsearch version
curl -X GET "localhost:9200"

# Check all indices
curl -X GET "localhost:9200/_cat/indices?v"

# Check all shards
curl -X GET "localhost:9200/_cat/shards?v"

# Check cluster settings
curl -X GET "localhost:9200/_cluster/settings?pretty"

# Update cluster settings
curl -X PUT "localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "cluster.routing.allocation.enable": "all"
  }
}'
```


## Scenario 4: Adjusting Shard Allocation for Indexing and Query Performance

**Question:** Your cluster is experiencing slow query performance due to the high load on certain indices. How would you adjust shard allocation to improve query performance?

**Answer:**

1. **Analyze Current Shard Allocation:**
```bash
curl -X GET "localhost:9200/_cat/shards?v"
```

2. **Adjust Index Settings:**
Increase the number of replicas for better query performance:
```bash
curl -X PUT "localhost:9200/index_name/_settings" -H 'Content-Type: application/json' -d'
{
  "index": {
    "number_of_replicas": 2
  }
}'
```

3. **Use the Reroute API to Rebalance Shards:**
```bash
curl -X POST "localhost:9200/_cluster/reroute" -H 'Content-Type: application/json' -d'
{
  "commands": [
    {
      "allocate_replica": {
        "index": "index_name",
        "shard": 0,
        "node": "node1"
      }
    },
    {
      "allocate_replica": {
        "index": "index_name",
        "shard": 1,
        "node": "node2"
      }
    }
  ]
}'
```

## Scenario 5: Handling Node Failure and Recovery

**Question:** One of your Elasticsearch nodes has failed, causing some primary shards to become unavailable. How would you handle this situation to recover the failed shards and ensure high availability?

**Answer:**

1. **Identify the Failed Shards:**
```bash
curl -X GET "localhost:9200/_cat/shards?v"
```

2. **Promote Replica Shards to Primary:**
```bash
curl -X POST "localhost:9200/_cluster/reroute" -H 'Content-Type: application/json' -d'
{
  "commands": [
    {
      "allocate_replica": {
        "index": "index_name",
        "shard": 0,
        "node": "node2"
      }
    }
  ]
}'
```

3. **Replace the Failed Node:**
   - Remove the failed node from the cluster configuration.
   - Add a new node to replace the failed one using Terraform.

**Terraform Configuration (Replacing a Node):**
```hcl
resource "azurerm_virtual_machine" "es" {
  count                = 10
  name                 = "es-${count.index}"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  network_interface_ids = [azurerm_network_interface.es[count.index].id]
  vm_size              = "Standard_DS2_v2"

  # Other VM configuration...
}

resource "azurerm_network_interface" "es" {
  count               = 10
  name                = "es-nic-${count.index}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Other NIC configuration...
}
```

## Scenario 6: Checking Cluster Health and Status with cURL

**Question:** How do you check the health and status of your Elasticsearch cluster using cURL commands?

**Answer:**

1. **Check Cluster Health:**
```bash
curl -X GET "localhost:9200/_cluster/health?pretty"
```

2. **Check Cluster State:**
```bash
curl -X GET "localhost:9200/_cluster/state?pretty"
```

3. **Check Node Information:**
```bash
curl -X GET "localhost:9200/_nodes?pretty"
```

4. **Check Shard Allocation:**
```bash
curl -X GET "localhost:9200/_cat/shards?v"
```

5. **Check Index Health:**
```bash
curl -X GET "localhost:9200/_cat/indices?v"
```

6. **Check Pending Tasks:**
```bash
curl -X GET "localhost:9200/_cat/pending_tasks?v"
```

## Common cURL Commands for Elasticsearch

```bash
# Check cluster health
curl -X GET "localhost:9200/_cluster/health?pretty"

# Check cluster state
curl -X GET "localhost:9200/_cluster/state?pretty"

# Check node information
curl -X GET "localhost:9200/_nodes?pretty"

# Check shard allocation
curl -X GET "localhost:9200/_cat/shards?v"

# Check index health
curl -X GET "localhost:9200/_cat/indices?v"

# Check pending tasks
curl -X GET "localhost:9200/_cat/pending_tasks?v"

# Rebalance shards
curl -X POST "localhost:9200/_cluster/reroute" -H 'Content-Type: application/json' -d'
{
  "commands": [
    {
      "allocate_replica": {
        "index": "index_name",
        "shard": 0,
        "node": "target_node"
      }
    },
    {
      "cancel": {
        "index": "index_name",
        "shard": 0,
        "node": "source_node",
        "allow_primary": true
      }
    }
  ]
}'
```

## Commonly Used Fields and Terms

- **from_node**: The source node in shard allocation and reallocation.
- **to_node**: The target node in shard allocation and reallocation.
- **count.index**: Used in Terraform to index resources.
- **_cat API**: Elasticsearch API endpoint for quick access to cluster information.
- **cache**: Used to cache shards for faster access.
- **replica**: Copies of the primary shard used for fault tolerance and increased search throughput.
- **primary**: The original shard responsible for indexing and updating documents.

### Common Fields in Terraform
- **name**: The name of the resource.
- **location**: The geographic location of the resource.
- **resource_group_name**: The name of the resource group.
- **network_interface_ids**: The IDs of the network interfaces associated with the VM.
- **vm_size**: The size of the virtual machine.

### Common Terms in Elasticsearch
- **shard**: A basic unit of storage in Elasticsearch. Each index is divided into shards.
- **replica shard**: A copy of a primary shard. Provides redundancy and improves search performance.
- **primary shard**: The original shard that handles indexing operations.
- **allocation**: The process of assigning shards to nodes.
- **rebalancing**: The process of redistributing shards across the nodes in a cluster to ensure even distribution.

### Useful cURL Commands
```bash
# Check Elasticsearch version
curl -X GET "localhost:9200"

# Check all indices
curl -X GET "localhost:9200/_cat/indices?v"

# Check all shards
curl -X GET "localhost:9200/_cat/shards?v"

# Check cluster settings
curl -X GET "localhost:9200/_cluster/settings?pretty"

# Update cluster settings
curl -X PUT "localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "cluster.routing.allocation.enable": "all"
  }
}'
```
