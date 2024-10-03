# Django Application: Logging to Azure Log Analytics Workspace

This is a simple Django application designed to capture and send application logs to Azure Log Analytics Workspace.

# Key Features:
- **Azure Web App Integration**: Deployed to Azure as a web app with **Application Insights enabled**.
- **Azure Log Analytics Workspace**: Set up in Azure Monitor, complete with a **Data Collection Endpoint (DCE)** and **Data Collection Rules (DCR)** configured for telemetry write permissions.
- **Logging Mechanism**: Uses the ```azure-sdk-for-python``` to send logs to Azure Log Analytics. The logs are captured in the **Traces** table within the Log Analytics Workspace.
- **Log Verification**: Logs are verified via **Kusto queries** in the Azure Logs Query Editor, ensuring they are logged correctly in the **Traces** table.
