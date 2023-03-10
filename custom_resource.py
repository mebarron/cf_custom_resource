import json
import boto3
import datetime
import redis

client = boto3.client('elasticache')

def checkIfExists(MyCacheClusterId):
    try: 
        response = client.describe_cache_clusters(
        CacheClusterId=MyCacheClusterId,
        MaxRecords=99,
        ShowCacheNodeInfo=True, 
        ShowCacheClustersNotInReplicationGroups=True 
        )
        return True
    except Exception as e:
        print(e)
        return False

def createCluster(ClusterInfo):
    try:
        response = client.create_cache_cluster(
        CacheClusterId=ClusterInfo['CacheClusterId'],
        ReplicationGroupId=ClusterInfo['ReplicationGroupId'],
        AZMode=ClusterInfo['AZMode'],
        PreferredAvailabilityZones=ClusterInfo['PreferredAvailabilityZones'],
        NumCacheNodes=int(ClusterInfo['NumCacheNodes']),
        CacheNodeType=ClusterInfo['CacheNodeType'],
        Engine=ClusterInfo['Engine'],
        EngineVersion=ClusterInfo['EngineVersion'],
        CacheParameterGroupName=ClusterInfo['CacheParameterGroupName'],
        CacheSubnetGroupName=ClusterInfo['CacheSubnetGroupName'],
        CacheSecurityGroupNames=ClusterInfo['CacheSecurityGroupNames'],
        PreferredMaintenanceWindow=ClusterInfo['PreferredMaintenanceWindow'],
        Port=8004,
        AutoMinorVersionUpgrade=False,
        AuthToken=ClusterInfo['AuthToken']
        )
        status = "SUCCESS" # in practice, this could return JSON with desired outputs from the creation event
        return status
    except Exception as e:
        print(e)
        status = "FAILURE"
        return status

def updateCluster(ClusterInfo):
    try:
        response = client.modify_cache_cluster(
        CacheClusterId=ClusterInfo['CacheClusterId'],
        NumCacheNodes=ClusterInfo['NumCacheNodes'],
        AZMode=ClusterInfo['AZMode'],
        NewAvailabilityZones=ClusterInfo['PreferredAvailabilityZones'],
        CacheSecurityGroupNames=ClusterInfo['CacheSecurityGroupNames'],
        SecurityGroupIds=ClusterInfo['SecurityGroupIds'],
        PreferredMaintenanceWindow=ClusterInfo['PreferredMaintenanceWindow'],
        CacheParameterGroupName=ClusterInfo['CacheParameterGroupName'],
        ApplyImmediately=True,
        EngineVersion=ClusterInfo['EngineVersion'],
        AutoMinorVersionUpgrade=False,
        CacheNodeType=ClusterInfo['CacheNodeType'],
        AuthToken=ClusterInfo['AuthToken']
        )
        status = "SUCCESS"
        return status
    except:
        print(response)
        status = "FAILURE"
        return status

def deleteCluster(CacheClusterId):
    response = client.delete_cache_cluster(
    CacheClusterId=CacheClusterId,
    FinalSnapshotIdentifier='final-shapshot' + '-' + str(datetime.now())
    )

def loadData(ClusterInfo, ConfigData):
    r = redis.Redis(
    host=ClusterInfo['hostname'],
    port=123,
    
    # Use AWS Secrets Manager and retrieve these values instead
     
    password=ClusterInfo['password']) 

    # Seed cluster with a pre-set dictionary of key/value pairs

    r.set(ConfigData)

def lambda_handler(event, context):
    ClusterInfo = event['ResourceProperties']['ClusterInfo']
    ConfigData = event['ResourceProperties']['ConfigData']
    
    # Handle each event, create, update, delete with different logic    
    # Use status check to ensure the cluster exists first, then seed data    

    if (event['RequestType'] == "Create"):
        if (checkIfExists(ClusterInfo['CacheClusterId']) == False):
            status = createCluster(ClusterInfo)
            loadData(ConfigData)
            return status
        else:
            status = "SUCCESS"
            loadData(ConfigData)
            return status

    if (event['RequestType'] == "Update"):
        if (checkIfExists(ClusterInfo['CacheClusterId']) == True):
            status = updateCluster(ClusterInfo)
            loadData(ConfigData)
            return status
        else:
            status = createCluster(ClusterInfo)
            loadData(ConfigData)
            return status

    if (event['RequestType'] == "Delete"):
            status = "SUCCESS"
            deleteCluster(ClusterInfo)
            return status
