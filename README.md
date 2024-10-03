# Python Django Azure LogAnalytics Workspace App

A simple app developed in Django, to capture the application logs and send the logs to Azure Log Analytics Workspace. Created a webapp in Azure and enabled Application Insights.
Created Log Analytics Workspace in Azure Montior, setup the **Data Collection Endpoint** and **Data Collection Rules** with telemetry write permissions.
Using **azure-sdk-for-python** send the logs to Azure LogAnalytics Workspace. All these logs are being logged in the traces table. By running kusto query in the logs section in Query editor, made sure the logs are getting logged in traces table.
