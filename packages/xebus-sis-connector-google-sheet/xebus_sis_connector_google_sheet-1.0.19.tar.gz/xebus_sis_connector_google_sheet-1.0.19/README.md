# Xebus Google Sheet SIS Connector
Connector to fetch family data from a school's Google Sheet document.

## Google Service Account

Xebus Google Sheet SIS Connector needs to use the [service account `xebus-family-list-google-sheet@xebus-323504.iam.gserviceaccount.com`](https://console.cloud.google.com/iam-admin/serviceaccounts?project=xebus-323504&supportedpurview=project) to get access to the Google sheet that contains the families data of a school organization.

A [service account](https://cloud.google.com/iam/docs/service-account-overview?_ga=2.62432492.-1545215353.1708747589) is a special kind of account typically used by an application, rather than a person. A service account is identified by its email address, which is unique to the account.  Applications use service accounts to make authorized API calls by authenticating as either the service account itself. When an application authenticates as a service account, it has access to all resources that the service account has permission to access.


