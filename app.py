from flask import Flask, request, jsonify, send_from_directory, url_for
from flask_cors import CORS
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.analytics import AnalysisServices, DataExplorerClusters, DataFactories, DataLakeAnalytics, DataLakeStoreGen1, Databricks, EventHubClusters, EventHubs, Hdinsightclusters, LogAnalyticsWorkspaces, StreamAnalyticsJobs, SynapseAnalytics
from diagrams.azure.compute import AppServices, AutomanagedVM, AvailabilitySets, BatchAccounts, CitrixVirtualDesktopsEssentials, CloudServicesClassic, CloudServices, CloudsimpleVirtualMachines, ContainerInstances, ContainerRegistries, DiskEncryptionSets, DiskSnapshots, Disks, FunctionApps, ImageDefinitions, ImageVersions, KubernetesServices, MeshApplications, OsImages, SAPHANAOnAzure, ServiceFabricClusters, SharedImageGalleries, SpringCloud, VMClassic, VMImages, VMLinux, VMScaleSet, VMWindows, VM, Workspaces
from diagrams.azure.database import BlobStorage, CacheForRedis, CosmosDb, DataExplorerClusters as DbDataExplorerClusters, DataFactory as DbDataFactory, DataLake as DbDataLake, DatabaseForMariadbServers, DatabaseForMysqlServers, DatabaseForPostgresqlServers, ElasticDatabasePools, ElasticJobAgents, InstancePools, ManagedDatabases, SQLDatabases, SQLDatawarehouse, SQLManagedInstances, SQLServerStretchDatabases, SQLServers, SQLVM, SQL, SsisLiftAndShiftIr, SynapseAnalytics as DbSynapseAnalytics, VirtualClusters, VirtualDatacenter
from diagrams.azure.devops import ApplicationInsights, Artifacts, Boards, Devops, DevtestLabs, LabServices, Pipelines, Repos, TestPlans
from diagrams.azure.general import Allresources, Azurehome, Developertools, Helpsupport, Information, Managementgroups, Marketplace, Quickstartcenter, Recent, Reservations, Resource, Resourcegroups, Servicehealth, Shareddashboard, Subscriptions, Support, Supportrequests, Tag, Tags, Templates, Twousericon, Userhealthicon, Usericon, Userprivacy, Userresource, Whatsnew
from diagrams.azure.identity import AccessReview, ActiveDirectoryConnectHealth, ActiveDirectory, ADB2C, ADDomainServices, ADIdentityProtection, ADPrivilegedIdentityManagement, AppRegistrations, ConditionalAccess, EnterpriseApplications, Groups, IdentityGovernance, InformationProtection, ManagedIdentities, Users
from diagrams.azure.integration import APIForFhir, APIManagement, AppConfiguration, DataCatalog, EventGridDomains, EventGridSubscriptions, EventGridTopics, IntegrationAccounts, IntegrationServiceEnvironments, LogicAppsCustomConnector, LogicApps, PartnerTopic, SendgridAccounts, ServiceBusRelays, ServiceBus, ServiceCatalogManagedApplicationDefinitions, SoftwareAsAService, StorsimpleDeviceManagers, SystemTopic
from diagrams.azure.iot import DeviceProvisioningServices, DigitalTwins, IotCentralApplications, IotHubSecurity, IotHub, Maps, Sphere, TimeSeriesInsightsEnvironments, TimeSeriesInsightsEventsSources, Windows10IotCoreServices
from diagrams.azure.migration import DataBoxEdge, DataBox, DatabaseMigrationServices, MigrationProjects, RecoveryServicesVaults
from diagrams.azure.ml import BatchAI, BotServices, CognitiveServices, GenomicsAccounts, MachineLearningServiceWorkspaces, MachineLearningStudioWebServicePlans, MachineLearningStudioWebServices, MachineLearningStudioWorkspaces
from diagrams.azure.mobile import AppServiceMobile, MobileEngagement, NotificationHubs
from diagrams.azure.network import ApplicationGateway, ApplicationSecurityGroups, CDNProfiles, Connections, DDOSProtectionPlans, DNSPrivateZones, DNSZones, ExpressrouteCircuits, Firewall, FrontDoors, LoadBalancers, LocalNetworkGateways, NetworkInterfaces, NetworkSecurityGroupsClassic, NetworkWatcher, OnPremisesDataGateways, PublicIpAddresses, ReservedIpAddressesClassic, RouteFilters, RouteTables, ServiceEndpointPolicies, Subnets, TrafficManagerProfiles, VirtualNetworkClassic, VirtualNetworkGateways, VirtualNetworks, VirtualWans
from diagrams.azure.security import ApplicationSecurityGroups as SecApplicationSecurityGroups, ConditionalAccess as SecConditionalAccess, Defender, ExtendedSecurityUpdates, KeyVaults, SecurityCenter, Sentinel
from diagrams.azure.storage import ArchiveStorage, Azurefxtedgefiler, BlobStorage as StorageBlobStorage, DataBoxEdgeDataBoxGateway, DataBox as StorageDataBox, DataLakeStorage, GeneralStorage, NetappFiles, QueuesStorage, StorageAccountsClassic, StorageAccounts, StorageExplorer, StorageSyncServices, StorsimpleDataManagers, StorsimpleDeviceManagers, TableStorage
from diagrams.azure.web import APIConnections, AppServiceCertificates, AppServiceDomains, AppServiceEnvironments, AppServicePlans, AppServices as WebAppServices, MediaServices, NotificationHubNamespaces, Search, Signalr
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS

# Mapa de recursos actualizado
RESOURCE_MAP = {
    "analysis-services": AnalysisServices,
    "data-explorer-clusters": DataExplorerClusters,
    "data-factories": DataFactories,
    "data-lake-analytics": DataLakeAnalytics,
    "data-lake-store-gen1": DataLakeStoreGen1,
    "databricks": Databricks,
    "event-hub-clusters": EventHubClusters,
    "event-hubs": EventHubs,
    "hdinsightclusters": Hdinsightclusters,
    "log-analytics-workspaces": LogAnalyticsWorkspaces,
    "stream-analytics-jobs": StreamAnalyticsJobs,
    "synapse-analytics": SynapseAnalytics,
    "app-services": AppServices,
    "automanaged-vm": AutomanagedVM,
    "availability-sets": AvailabilitySets,
    "batch-accounts": BatchAccounts,
    "citrix-virtual-desktops-essentials": CitrixVirtualDesktopsEssentials,
    "cloud-services-classic": CloudServicesClassic,
    "cloud-services": CloudServices,
    "cloudsimple-virtual-machines": CloudsimpleVirtualMachines,
    "container-instances": ContainerInstances,
    "container-registries": ContainerRegistries,
    "disk-encryption-sets": DiskEncryptionSets,
    "disk-snapshots": DiskSnapshots,
    "disks": Disks,
    "function-apps": FunctionApps,
    "image-definitions": ImageDefinitions,
    "image-versions": ImageVersions,
    "kubernetes-services": KubernetesServices,
    "mesh-applications": MeshApplications,
    "os-images": OsImages,
    "sap-hana-on-azure": SAPHANAOnAzure,
    "service-fabric-clusters": ServiceFabricClusters,
    "shared-image-galleries": SharedImageGalleries,
    "spring-cloud": SpringCloud,
    "vm-classic": VMClassic,
    "vm-images": VMImages,
    "vm-linux": VMLinux,
    "vm-scale-set": VMScaleSet,
    "vm-windows": VMWindows,
    "vm": VM,
    "workspaces": Workspaces,
    "blob-storage": BlobStorage,
    "cache-for-redis": CacheForRedis,
    "cosmos-db": CosmosDb,
    "data-explorer-clusters": DbDataExplorerClusters,
    "data-factory": DbDataFactory,
    "data-lake": DbDataLake,
    "database-for-mariadb-servers": DatabaseForMariadbServers,
    "database-for-mysql-servers": DatabaseForMysqlServers,
    "database-for-postgresql-servers": DatabaseForPostgresqlServers,
    "elastic-database-pools": ElasticDatabasePools,
    "elastic-job-agents": ElasticJobAgents,
    "instance-pools": InstancePools,
    "managed-databases": ManagedDatabases,
    "sql-databases": SQLDatabases,
    "sql-datawarehouse": SQLDatawarehouse,
    "sql-managed-instances": SQLManagedInstances,
    "sql-server-stretch-databases": SQLServerStretchDatabases,
    "sql-servers": SQLServers,
    "sql-vm": SQLVM,
    "sql": SQL,
    "ssis-lift-and-shift-ir": SsisLiftAndShiftIr,
    "synapse-analytics": DbSynapseAnalytics,
    "virtual-clusters": VirtualClusters,
    "virtual-datacenter": VirtualDatacenter,
    "application-insights": ApplicationInsights,
    "artifacts": Artifacts,
    "boards": Boards,
    "devops": Devops,
    "devtest-labs": DevtestLabs,
    "lab-services": LabServices,
    "pipelines": Pipelines,
    "repos": Repos,
    "test-plans": TestPlans,
    "allresources": Allresources,
    "azurehome": Azurehome,
    "developertools": Developertools,
    "helpsupport": Helpsupport,
    "information": Information,
    "managementgroups": Managementgroups,
    "marketplace": Marketplace,
    "quickstartcenter": Quickstartcenter,
    "recent": Recent,
    "reservations": Reservations,
    "resource": Resource,
    "resourcegroups": Resourcegroups,
    "servicehealth": Servicehealth,
    "shareddashboard": Shareddashboard,
    "subscriptions": Subscriptions,
    "support": Support,
    "supportrequests": Supportrequests,
    "tag": Tag,
    "tags": Tags,
    "templates": Templates,
    "twousericon": Twousericon,
    "userhealthicon": Userhealthicon,
    "usericon": Usericon,
    "userprivacy": Userprivacy,
    "userresource": Userresource,
    "whatsnew": Whatsnew,
    "access-review": AccessReview,
    "active-directory-connect-health": ActiveDirectoryConnectHealth,
    "active-directory": ActiveDirectory,
    "adb2c": ADB2C,
    "ad-domain-services": ADDomainServices,
    "ad-identity-protection": ADIdentityProtection,
    "ad-privileged-identity-management": ADPrivilegedIdentityManagement,
    "app-registrations": AppRegistrations,
    "conditional-access": ConditionalAccess,
    "enterprise-applications": EnterpriseApplications,
    "groups": Groups,
    "identity-governance": IdentityGovernance,
    "information-protection": InformationProtection,
    "managed-identities": ManagedIdentities,
    "users": Users,
    "api-for-fhir": APIForFhir,
    "api-management": APIManagement,
    "app-configuration": AppConfiguration,
    "data-catalog": DataCatalog,
    "event-grid-domains": EventGridDomains,
    "event-grid-subscriptions": EventGridSubscriptions,
    "event-grid-topics": EventGridTopics,
    "integration-accounts": IntegrationAccounts,
    "integration-service-environments": IntegrationServiceEnvironments,
    "logic-apps-custom-connector": LogicAppsCustomConnector,
    "logic-apps": LogicApps,
    "partner-topic": PartnerTopic,
    "sendgrid-accounts": SendgridAccounts,
    "service-bus-relays": ServiceBusRelays,
    "service-bus": ServiceBus,
    "service-catalog-managed-application-definitions": ServiceCatalogManagedApplicationDefinitions,
    "software-as-a-service": SoftwareAsAService,
    "storsimple-device-managers": StorsimpleDeviceManagers,
    "system-topic": SystemTopic,
    "device-provisioning-services": DeviceProvisioningServices,
    "digital-twins": DigitalTwins,
    "iot-central-applications": IotCentralApplications,
    "iot-hub-security": IotHubSecurity,
    "iot-hub": IotHub,
    "maps": Maps,
    "sphere": Sphere,
    "time-series-insights-environments": TimeSeriesInsightsEnvironments,
    "time-series-insights-events-sources": TimeSeriesInsightsEventsSources,
    "windows-10-iot-core-services": Windows10IotCoreServices,
    "data-box-edge": DataBoxEdge,
    "data-box": DataBox,
    "database-migration-services": DatabaseMigrationServices,
    "migration-projects": MigrationProjects,
    "recovery-services-vaults": RecoveryServicesVaults,
    "batch-ai": BatchAI,
    "bot-services": BotServices,
    "cognitive-services": CognitiveServices,
    "genomics-accounts": GenomicsAccounts,
    "machine-learning-service-workspaces": MachineLearningServiceWorkspaces,
    "machine-learning-studio-web-service-plans": MachineLearningStudioWebServicePlans,
    "machine-learning-studio-web-services": MachineLearningStudioWebServices,
    "machine-learning-studio-workspaces": MachineLearningStudioWorkspaces,
    "app-service-mobile": AppServiceMobile,
    "mobile-engagement": MobileEngagement,
    "notification-hubs": NotificationHubs,
    "application-gateway": ApplicationGateway,
    "application-security-groups": ApplicationSecurityGroups,
    "cdn-profiles": CDNProfiles,
    "connections": Connections,
    "ddos-protection-plans": DDOSProtectionPlans,
    "dns-private-zones": DNSPrivateZones,
    "dns-zones": DNSZones,
    "expressroute-circuits": ExpressrouteCircuits,
    "firewall": Firewall,
    "front-doors": FrontDoors,
    "load-balancers": LoadBalancers,
    "local-network-gateways": LocalNetworkGateways,
    "network-interfaces": NetworkInterfaces,
    "network-security-groups-classic": NetworkSecurityGroupsClassic,
    "network-watcher": NetworkWatcher,
    "on-premises-data-gateways": OnPremisesDataGateways,
    "public-ip-addresses": PublicIpAddresses,
    "reserved-ip-addresses-classic": ReservedIpAddressesClassic,
    "route-filters": RouteFilters,
    "route-tables": RouteTables,
    "service-endpoint-policies": ServiceEndpointPolicies,
    "subnets": Subnets,
    "traffic-manager-profiles": TrafficManagerProfiles,
    "virtual-network-classic": VirtualNetworkClassic,
    "virtual-network-gateways": VirtualNetworkGateways,
    "virtual-networks": VirtualNetworks,
    "virtual-wans": VirtualWans,
    "application-security-groups": SecApplicationSecurityGroups,
    "conditional-access": SecConditionalAccess,
    "defender": Defender,
    "extended-security-updates": ExtendedSecurityUpdates,
    "key-vaults": KeyVaults,
    "security-center": SecurityCenter,
    "sentinel": Sentinel,
    "archive-storage": ArchiveStorage,
    "azurefxtedgefiler": Azurefxtedgefiler,
    "blob-storage": StorageBlobStorage,
    "data-box-edge-data-box-gateway": DataBoxEdgeDataBoxGateway,
    "data-box": StorageDataBox,
    "data-lake-storage": DataLakeStorage,
    "general-storage": GeneralStorage,
    "netapp-files": NetappFiles,
    "queues-storage": QueuesStorage,
    "storage-accounts-classic": StorageAccountsClassic,
    "storage-accounts": StorageAccounts,
    "storage-explorer": StorageExplorer,
    "storage-sync-services": StorageSyncServices,
    "storsimple-data-managers": StorsimpleDataManagers,
    "storsimple-device-managers": StorsimpleDeviceManagers,
    "table-storage": TableStorage,
    "api-connections": APIConnections,
    "app-service-certificates": AppServiceCertificates,
    "app-service-domains": AppServiceDomains,
    "app-service-environments": AppServiceEnvironments,
    "app-service-plans": AppServicePlans,
    "app-services": WebAppServices,
    "media-services": MediaServices,
    "notification-hub-namespaces": NotificationHubNamespaces,
    "search": Search,
    "signalr": Signalr
}
@app.route('/')
def index():
    return "Azure Diagram Backend API is running."

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/generate-diagram', methods=['POST'])
def generate_diagram():
    data = request.json
    resources = data.get('resources', [])
    relationships = data.get('relationships', [])
    clusters = data.get('clusters', [])

    if not resources and not clusters:
        return jsonify({"message": "No resources or clusters provided", "image_url": ""}), 400

    resource_map = {}

    graph_attr = {"fontsize": "45", "bgcolor": "transparent"}
    with Diagram("Azure Infrastructure", show=False, filename="static/diagram", outformat="png", graph_attr=graph_attr):
        for cluster in clusters:
            with Cluster(cluster['name']):
                for resource in cluster['resources']:
                    rtype = resource['type']
                    rname = resource['name']
                    if rtype in RESOURCE_MAP:
                        resource_map[rname] = RESOURCE_MAP[rtype](rname)

        for resource in resources:
            rtype = resource['type']
            rname = resource['name']
            if rtype in RESOURCE_MAP:
                resource_map[rname] = RESOURCE_MAP[rtype](rname)

        for relationship in relationships:
            source = relationship['source']
            target = relationship['target']
            if source in resource_map and target in resource_map:
                resource_map[source] >> resource_map[target]

    image_url = url_for('static', filename='diagram.png', _external=True)
    return jsonify({"message": "Diagram generated successfully", "image_url": image_url}), 200

@app.route('/download-diagram')
def download_diagram():
    return send_from_directory(directory='static', filename='diagram.png')

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
    