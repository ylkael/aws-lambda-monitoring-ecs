# AWS Lambda monitoring for ECS Cluster status and running tasks  

An Event rule calls the Lambda function every 15 minutes. The function runs python file to check the status of ECS Cluster and the number of running tasks for services.  

If the status of Cluster is not Active, or the amount of running tasks is 0 for any number of services, the monitoring status is sent to CloudWatch metrics as value 0. If Cluster status is Active, the value is set to 1, and if there are more than 0 running tasks, the value is set to the number of running tasks for each service.

CloudWatch Alarm monitors metrics separately for Cluster and all services, and sends email via SNS topic to monitoring team if the monitoring value for any of the metrics has been less than 1 for the last hour.  

---

&nbsp;  

Note: The contents of this repository has been modified to remove the names of the client and their application.  

&nbsp;

---