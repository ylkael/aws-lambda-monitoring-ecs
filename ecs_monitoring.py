"""ECS Monitoring Module"""
import boto3

def lambda_handler(event, context):
  client = boto3.client('ecs', region_name='eu-north-1')
  
  # Check cluster status
  describecluster = client.describe_clusters(clusters=['Cluster'])
  cluster = describecluster['clusters'][0]
  clustername = cluster['clusterName']
  clusterstatus = cluster['status']
  if clusterstatus == 'ACTIVE':
    monitor_status(clustername, clusterstatus = 1)
  elif clusterstatus != 'ACTIVE':
    monitor_trigger(clustername, clusterstatus = 0)

  # Check running tasks for services
  listservices = client.list_services(cluster='Cluster')
  service_arns = listservices['serviceArns']
  for service in service_arns:
    servicename = service.split('/')[-1]
    describeservices = client.describe_services(cluster='Cluster', services=[service])
    service = describeservices['services'][0]
    taskcount = service['runningCount']
    if taskcount > 0:
      monitor_status(servicename, runningtasks = taskcount)
    elif taskcount == 0:
      monitor_trigger(servicename, runningtasks = 0)

# CloudWatch Metrics for Trigger values
def monitor_trigger(*args, **kwargs):
  name = args[0] # the name of the cluster / service
  for key,value in kwargs.items():
    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.put_metric_data(
      MetricData = [
        {
          'MetricName': ('ECSMonitoring-' + key),
          'Dimensions': [
            {
              'Name': 'ECSMonitoring',
              'Value': name
            }
          ],
          'Unit': 'Count',
          'Value': value
        },
      ],
      Namespace = 'Monitoring'
    )

# CloudWatch Metrics for OK values
def monitor_status(*args, **kwargs):
  name = args[0] # the name of the cluster / service
  for key,value in kwargs.items():
    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.put_metric_data(
      MetricData = [
        {
          'MetricName': ('ECSMonitoring-' + key),
          'Dimensions': [
            {
              'Name': 'ECSMonitoring',
              'Value': name
            }
          ],
          'Unit': 'Count',
          'Value': value
        },
      ],
      Namespace = 'Monitoring'
    )
