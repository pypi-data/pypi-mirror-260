"""This module contains all the constants used in the Wiz SDK."""

INVENTORY_FILE_PATH = "artifacts/wiz_inventory.json"
CONTENT_TYPE = "application/json"
RATE_LIMIT_MSG = "Rate limit exceeded"
PROVIDER = "Provider ID"
RESOURCE = "Resource Type"
CHECK_INTERVAL_FOR_DOWNLOAD_REPORT = 7
MAX_RETRIES = 100
ASSET_TYPE_MAPPING = {
    "ACCESS_ROLE": "Other",
    "ACCESS_ROLE_BINDING": "Other",
    "ACCESS_ROLE_PERMISSION": "Other",
    "API_GATEWAY": "Other",
    "APPLICATION": "Other",
    "AUTHENTICATION_CONFIGURATION": "Other",
    "BACKUP_SERVICE": "Other",
    "BUCKET": "Other",
    "CDN": "Other",
    "CERTIFICATE": "Other",
    "CICD_SERVICE": "Other",
    "CLOUD_LOG_CONFIGURATION": "Other",
    "CLOUD_ORGANIZATION": "Other",
    "COMPUTE_INSTANCE_GROUP": "Other",
    "CONFIG_MAP": "Other",
    "CONTAINER": "Other",
    "CONTAINER_GROUP": "Other",
    "CONTAINER_IMAGE": "Other",
    "CONTAINER_REGISTRY": "Other",
    "CONTAINER_SERVICE": "Other",
    "DAEMON_SET": "Other",
    "DATABASE": "Other",
    "DATA_WORKLOAD": "Other",
    "DB_SERVER": "Physical Server",
    "DEPLOYMENT": "Other",
    "DNS_RECORD": "Other",
    "DNS_ZONE": "Other",
    "DOMAIN": "Other",
    "EMAIL_SERVICE": "Other",
    "ENCRYPTION_KEY": "Other",
    "ENDPOINT": "Other",
    "FILE_SYSTEM_SERVICE": "Other",
    "FIREWALL": "Firewall",
    "GATEWAY": "Other",
    "GOVERNANCE_POLICY": "Other",
    "GOVERNANCE_POLICY_GROUP": "Other",
    "HOSTED_APPLICATION": "Other",
    "IAM_BINDING": "Other",
    "IP_RANGE": "Other",
    "KUBERNETES_CLUSTER": "Other",
    "KUBERNETES_CRON_JOB": "Other",
    "KUBERNETES_INGRESS": "Other",
    "KUBERNETES_INGRESS_CONTROLLER": "Other",
    "KUBERNETES_JOB": "Other",
    "KUBERNETES_NETWORK_POLICY": "Other",
    "KUBERNETES_NODE": "Other",
    "KUBERNETES_PERSISTENT_VOLUME": "Other",
    "KUBERNETES_PERSISTENT_VOLUME_CLAIM": "Other",
    "KUBERNETES_POD_SECURITY_POLICY": "Other",
    "KUBERNETES_SERVICE": "Other",
    "KUBERNETES_STORAGE_CLASS": "Other",
    "KUBERNETES_VOLUME": "Other",
    "LOAD_BALANCER": "Other",
    "MANAGED_CERTIFICATE": "Other",
    "MANAGEMENT_SERVICE": "Other",
    "NETWORK_ADDRESS": "Other",
    "NETWORK_INTERFACE": "Other",
    "NETWORK_ROUTING_RULE": "Other",
    "NETWORK_SECURITY_RULE": "Other",
    "PEERING": "Other",
    "POD": "Other",
    "PORT_RANGE": "Other",
    "PRIVATE_ENDPOINT": "Other",
    "PROXY": "Other",
    "PROXY_RULE": "Other",
    "RAW_ACCESS_POLICY": "Other",
    "REGISTERED_DOMAIN": "Other",
    "REPLICA_SET": "Other",
    "RESOURCE_GROUP": "Other",
    "SEARCH_INDEX": "Other",
    "SUBNET": "Other",
    "SUBSCRIPTION": "Other",
    "SWITCH": "Network Switch",
    "VIRTUAL_DESKTOP": "Virtual Machine (VM)",
    "VIRTUAL_MACHINE": "Virtual Machine (VM)",
    "VIRTUAL_MACHINE_IMAGE": "Other",
    "VIRTUAL_NETWORK": "Other",
    "VOLUME": "Other",
    "WEB_SERVICE": "Other",
    "DATA_WORKFLOW": "Other",
}

INVENTORY_QUERY = """
    query CloudResourceSearch(
    $filterBy: CloudResourceFilters
    $first: Int
    $after: String
  ) {
    cloudResources(
      filterBy: $filterBy
      first: $first
      after: $after
    ) {
      nodes {
        ...CloudResourceFragment
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
  fragment CloudResourceFragment on CloudResource {
    id
    name
    type
    subscriptionId
    subscriptionExternalId
    graphEntity{
      id
      providerUniqueId
      name
      type
      projects {
        id
      }
      properties
      firstSeen
      lastSeen
    }
  }
"""
DATASOURCE = "Wiz"
SBOM_QUERY = """
    query ArtifactsGroupedByNameTable($filterBy: SBOMArtifactsGroupedByNameFilter, $first: Int, $after: String, $orderBy: SBOMArtifactsGroupedByNameOrder) {
      sbomArtifactsGroupedByName(
        filterBy: $filterBy
        first: $first
        after: $after
        orderBy: $orderBy
      ) {
        nodes {
          id
          type {
            group
            codeLibraryLanguage
            osPackageManager
          }
          name
          validatedInRuntime
          artifacts(first: 0) {
            totalCount
          }
          versions(first: 500) {
            nodes {
              version
            }
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
        totalCount
      }
    }
"""

TECHNOLOGIES_FILE_PATH = "./artifacts/technologies.json"
AUTH0_URLS = [
    "https://auth.wiz.io/oauth/token",
    "https://auth0.gov.wiz.io/oauth/token",
    "https://auth0.test.wiz.io/oauth/token",
    "https://auth0.demo.wiz.io/oauth/token",
]
COGNITO_URLS = [
    "https://auth.app.wiz.io/oauth/token",
    "https://auth.gov.wiz.io/oauth/token",
    "https://auth.test.wiz.io/oauth/token",
    "https://auth.demo.wiz.io/oauth/token",
    "https://auth.app.wiz.us/oauth/token",
]
CREATE_REPORT_QUERY = """
    mutation CreateReport($input: CreateReportInput!) {
    createReport(input: $input) {
        report {
        id
        }
    }
    }
"""
REPORTS_QUERY = """
        query ReportsTable($filterBy: ReportFilters, $first: Int, $after: String) {
          reports(first: $first, after: $after, filterBy: $filterBy) {
            nodes {
              id
              name
              type {
                id
                name
              }
              project {
                id
                name
              }
              emailTarget {
                to
              }
              parameters {
                query
                framework {
                  name
                }
                subscriptions {
                  id
                  name
                  type
                }
                entities {
                  id
                  name
                  type
                }
              }
              lastRun {
                ...LastRunDetails
              }
              nextRunAt
              runIntervalHours
            }
            pageInfo {
              hasNextPage
              endCursor
            }
            totalCount
          }
        }

            fragment LastRunDetails on ReportRun {
          id
          status
          failedReason
          runAt
          progress
          results {
            ... on ReportRunResultsBenchmark {
              errorCount
              passedCount
              failedCount
              scannedCount
            }
            ... on ReportRunResultsGraphQuery {
              resultCount
              entityCount
            }
            ... on ReportRunResultsNetworkExposure {
              scannedCount
              publiclyAccessibleCount
            }
            ... on ReportRunResultsConfigurationFindings {
              findingsCount
            }
            ... on ReportRunResultsVulnerabilities {
              count
            }
            ... on ReportRunResultsIssues {
              count
            }
          }
        }
    """
DOWNLOAD_QUERY = """
    query ReportDownloadUrl($reportId: ID!) {
        report(id: $reportId) {
            lastRun {
                url
                status
            }
        }
    }
    """
