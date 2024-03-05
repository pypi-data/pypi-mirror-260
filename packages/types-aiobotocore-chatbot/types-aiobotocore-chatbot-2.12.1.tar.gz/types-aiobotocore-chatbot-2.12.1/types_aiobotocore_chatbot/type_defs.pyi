"""
Type annotations for chatbot service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/type_defs/)

Usage::

    ```python
    from types_aiobotocore_chatbot.type_defs import AccountPreferencesTypeDef

    data: AccountPreferencesTypeDef = ...
    ```
"""

import sys
from typing import Dict, List, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AccountPreferencesTypeDef",
    "ChimeWebhookConfigurationTypeDef",
    "ConfiguredTeamTypeDef",
    "CreateChimeWebhookConfigurationRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateSlackChannelConfigurationRequestRequestTypeDef",
    "SlackChannelConfigurationTypeDef",
    "CreateTeamsChannelConfigurationRequestRequestTypeDef",
    "TeamsChannelConfigurationTypeDef",
    "DeleteChimeWebhookConfigurationRequestRequestTypeDef",
    "DeleteMicrosoftTeamsUserIdentityRequestRequestTypeDef",
    "DeleteSlackChannelConfigurationRequestRequestTypeDef",
    "DeleteSlackUserIdentityRequestRequestTypeDef",
    "DeleteSlackWorkspaceAuthorizationRequestRequestTypeDef",
    "DeleteTeamsChannelConfigurationRequestRequestTypeDef",
    "DeleteTeamsConfiguredTeamRequestRequestTypeDef",
    "DescribeChimeWebhookConfigurationsRequestRequestTypeDef",
    "DescribeSlackChannelConfigurationsRequestRequestTypeDef",
    "DescribeSlackUserIdentitiesRequestRequestTypeDef",
    "SlackUserIdentityTypeDef",
    "DescribeSlackWorkspacesRequestRequestTypeDef",
    "SlackWorkspaceTypeDef",
    "GetTeamsChannelConfigurationRequestRequestTypeDef",
    "ListMicrosoftTeamsConfiguredTeamsRequestRequestTypeDef",
    "ListMicrosoftTeamsUserIdentitiesRequestRequestTypeDef",
    "TeamsUserIdentityTypeDef",
    "ListTeamsChannelConfigurationsRequestRequestTypeDef",
    "UpdateAccountPreferencesRequestRequestTypeDef",
    "UpdateChimeWebhookConfigurationRequestRequestTypeDef",
    "UpdateSlackChannelConfigurationRequestRequestTypeDef",
    "UpdateTeamsChannelConfigurationRequestRequestTypeDef",
    "CreateChimeWebhookConfigurationResultTypeDef",
    "DescribeChimeWebhookConfigurationsResultTypeDef",
    "GetAccountPreferencesResultTypeDef",
    "ListMicrosoftTeamsConfiguredTeamsResultTypeDef",
    "UpdateAccountPreferencesResultTypeDef",
    "UpdateChimeWebhookConfigurationResultTypeDef",
    "CreateSlackChannelConfigurationResultTypeDef",
    "DescribeSlackChannelConfigurationsResultTypeDef",
    "UpdateSlackChannelConfigurationResultTypeDef",
    "CreateTeamsChannelConfigurationResultTypeDef",
    "GetTeamsChannelConfigurationResultTypeDef",
    "ListTeamsChannelConfigurationsResultTypeDef",
    "UpdateTeamsChannelConfigurationResultTypeDef",
    "DescribeSlackUserIdentitiesResultTypeDef",
    "DescribeSlackWorkspacesResultTypeDef",
    "ListMicrosoftTeamsUserIdentitiesResultTypeDef",
)

AccountPreferencesTypeDef = TypedDict(
    "AccountPreferencesTypeDef",
    {
        "UserAuthorizationRequired": NotRequired[bool],
        "TrainingDataCollectionEnabled": NotRequired[bool],
    },
)
ChimeWebhookConfigurationTypeDef = TypedDict(
    "ChimeWebhookConfigurationTypeDef",
    {
        "WebhookDescription": str,
        "ChatConfigurationArn": str,
        "IamRoleArn": str,
        "SnsTopicArns": List[str],
        "ConfigurationName": NotRequired[str],
        "LoggingLevel": NotRequired[str],
    },
)
ConfiguredTeamTypeDef = TypedDict(
    "ConfiguredTeamTypeDef",
    {
        "TenantId": str,
        "TeamId": str,
        "TeamName": NotRequired[str],
    },
)
CreateChimeWebhookConfigurationRequestRequestTypeDef = TypedDict(
    "CreateChimeWebhookConfigurationRequestRequestTypeDef",
    {
        "WebhookDescription": str,
        "WebhookUrl": str,
        "SnsTopicArns": Sequence[str],
        "IamRoleArn": str,
        "ConfigurationName": str,
        "LoggingLevel": NotRequired[str],
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
CreateSlackChannelConfigurationRequestRequestTypeDef = TypedDict(
    "CreateSlackChannelConfigurationRequestRequestTypeDef",
    {
        "SlackTeamId": str,
        "SlackChannelId": str,
        "IamRoleArn": str,
        "ConfigurationName": str,
        "SlackChannelName": NotRequired[str],
        "SnsTopicArns": NotRequired[Sequence[str]],
        "LoggingLevel": NotRequired[str],
        "GuardrailPolicyArns": NotRequired[Sequence[str]],
        "UserAuthorizationRequired": NotRequired[bool],
    },
)
SlackChannelConfigurationTypeDef = TypedDict(
    "SlackChannelConfigurationTypeDef",
    {
        "SlackTeamName": str,
        "SlackTeamId": str,
        "SlackChannelId": str,
        "SlackChannelName": str,
        "ChatConfigurationArn": str,
        "IamRoleArn": str,
        "SnsTopicArns": List[str],
        "ConfigurationName": NotRequired[str],
        "LoggingLevel": NotRequired[str],
        "GuardrailPolicyArns": NotRequired[List[str]],
        "UserAuthorizationRequired": NotRequired[bool],
    },
)
CreateTeamsChannelConfigurationRequestRequestTypeDef = TypedDict(
    "CreateTeamsChannelConfigurationRequestRequestTypeDef",
    {
        "ChannelId": str,
        "TeamId": str,
        "TenantId": str,
        "IamRoleArn": str,
        "ConfigurationName": str,
        "ChannelName": NotRequired[str],
        "TeamName": NotRequired[str],
        "SnsTopicArns": NotRequired[Sequence[str]],
        "LoggingLevel": NotRequired[str],
        "GuardrailPolicyArns": NotRequired[Sequence[str]],
        "UserAuthorizationRequired": NotRequired[bool],
    },
)
TeamsChannelConfigurationTypeDef = TypedDict(
    "TeamsChannelConfigurationTypeDef",
    {
        "ChannelId": str,
        "TeamId": str,
        "TenantId": str,
        "ChatConfigurationArn": str,
        "IamRoleArn": str,
        "SnsTopicArns": List[str],
        "ChannelName": NotRequired[str],
        "TeamName": NotRequired[str],
        "ConfigurationName": NotRequired[str],
        "LoggingLevel": NotRequired[str],
        "GuardrailPolicyArns": NotRequired[List[str]],
        "UserAuthorizationRequired": NotRequired[bool],
    },
)
DeleteChimeWebhookConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteChimeWebhookConfigurationRequestRequestTypeDef",
    {
        "ChatConfigurationArn": str,
    },
)
DeleteMicrosoftTeamsUserIdentityRequestRequestTypeDef = TypedDict(
    "DeleteMicrosoftTeamsUserIdentityRequestRequestTypeDef",
    {
        "ChatConfigurationArn": str,
        "UserId": str,
    },
)
DeleteSlackChannelConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteSlackChannelConfigurationRequestRequestTypeDef",
    {
        "ChatConfigurationArn": str,
    },
)
DeleteSlackUserIdentityRequestRequestTypeDef = TypedDict(
    "DeleteSlackUserIdentityRequestRequestTypeDef",
    {
        "ChatConfigurationArn": str,
        "SlackTeamId": str,
        "SlackUserId": str,
    },
)
DeleteSlackWorkspaceAuthorizationRequestRequestTypeDef = TypedDict(
    "DeleteSlackWorkspaceAuthorizationRequestRequestTypeDef",
    {
        "SlackTeamId": str,
    },
)
DeleteTeamsChannelConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteTeamsChannelConfigurationRequestRequestTypeDef",
    {
        "ChatConfigurationArn": str,
    },
)
DeleteTeamsConfiguredTeamRequestRequestTypeDef = TypedDict(
    "DeleteTeamsConfiguredTeamRequestRequestTypeDef",
    {
        "TeamId": str,
    },
)
DescribeChimeWebhookConfigurationsRequestRequestTypeDef = TypedDict(
    "DescribeChimeWebhookConfigurationsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "ChatConfigurationArn": NotRequired[str],
    },
)
DescribeSlackChannelConfigurationsRequestRequestTypeDef = TypedDict(
    "DescribeSlackChannelConfigurationsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "ChatConfigurationArn": NotRequired[str],
    },
)
DescribeSlackUserIdentitiesRequestRequestTypeDef = TypedDict(
    "DescribeSlackUserIdentitiesRequestRequestTypeDef",
    {
        "ChatConfigurationArn": NotRequired[str],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
SlackUserIdentityTypeDef = TypedDict(
    "SlackUserIdentityTypeDef",
    {
        "IamRoleArn": str,
        "ChatConfigurationArn": str,
        "SlackTeamId": str,
        "SlackUserId": str,
        "AwsUserIdentity": NotRequired[str],
    },
)
DescribeSlackWorkspacesRequestRequestTypeDef = TypedDict(
    "DescribeSlackWorkspacesRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
SlackWorkspaceTypeDef = TypedDict(
    "SlackWorkspaceTypeDef",
    {
        "SlackTeamId": str,
        "SlackTeamName": str,
    },
)
GetTeamsChannelConfigurationRequestRequestTypeDef = TypedDict(
    "GetTeamsChannelConfigurationRequestRequestTypeDef",
    {
        "ChatConfigurationArn": str,
    },
)
ListMicrosoftTeamsConfiguredTeamsRequestRequestTypeDef = TypedDict(
    "ListMicrosoftTeamsConfiguredTeamsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
ListMicrosoftTeamsUserIdentitiesRequestRequestTypeDef = TypedDict(
    "ListMicrosoftTeamsUserIdentitiesRequestRequestTypeDef",
    {
        "ChatConfigurationArn": NotRequired[str],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
TeamsUserIdentityTypeDef = TypedDict(
    "TeamsUserIdentityTypeDef",
    {
        "IamRoleArn": str,
        "ChatConfigurationArn": str,
        "TeamId": str,
        "UserId": NotRequired[str],
        "AwsUserIdentity": NotRequired[str],
        "TeamsChannelId": NotRequired[str],
        "TeamsTenantId": NotRequired[str],
    },
)
ListTeamsChannelConfigurationsRequestRequestTypeDef = TypedDict(
    "ListTeamsChannelConfigurationsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "TeamId": NotRequired[str],
    },
)
UpdateAccountPreferencesRequestRequestTypeDef = TypedDict(
    "UpdateAccountPreferencesRequestRequestTypeDef",
    {
        "UserAuthorizationRequired": NotRequired[bool],
        "TrainingDataCollectionEnabled": NotRequired[bool],
    },
)
UpdateChimeWebhookConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateChimeWebhookConfigurationRequestRequestTypeDef",
    {
        "ChatConfigurationArn": str,
        "WebhookDescription": NotRequired[str],
        "WebhookUrl": NotRequired[str],
        "SnsTopicArns": NotRequired[Sequence[str]],
        "IamRoleArn": NotRequired[str],
        "LoggingLevel": NotRequired[str],
    },
)
UpdateSlackChannelConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateSlackChannelConfigurationRequestRequestTypeDef",
    {
        "ChatConfigurationArn": str,
        "SlackChannelId": str,
        "SlackChannelName": NotRequired[str],
        "SnsTopicArns": NotRequired[Sequence[str]],
        "IamRoleArn": NotRequired[str],
        "LoggingLevel": NotRequired[str],
        "GuardrailPolicyArns": NotRequired[Sequence[str]],
        "UserAuthorizationRequired": NotRequired[bool],
    },
)
UpdateTeamsChannelConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateTeamsChannelConfigurationRequestRequestTypeDef",
    {
        "ChatConfigurationArn": str,
        "ChannelId": str,
        "ChannelName": NotRequired[str],
        "SnsTopicArns": NotRequired[Sequence[str]],
        "IamRoleArn": NotRequired[str],
        "LoggingLevel": NotRequired[str],
        "GuardrailPolicyArns": NotRequired[Sequence[str]],
        "UserAuthorizationRequired": NotRequired[bool],
    },
)
CreateChimeWebhookConfigurationResultTypeDef = TypedDict(
    "CreateChimeWebhookConfigurationResultTypeDef",
    {
        "WebhookConfiguration": ChimeWebhookConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeChimeWebhookConfigurationsResultTypeDef = TypedDict(
    "DescribeChimeWebhookConfigurationsResultTypeDef",
    {
        "NextToken": str,
        "WebhookConfigurations": List[ChimeWebhookConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAccountPreferencesResultTypeDef = TypedDict(
    "GetAccountPreferencesResultTypeDef",
    {
        "AccountPreferences": AccountPreferencesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListMicrosoftTeamsConfiguredTeamsResultTypeDef = TypedDict(
    "ListMicrosoftTeamsConfiguredTeamsResultTypeDef",
    {
        "ConfiguredTeams": List[ConfiguredTeamTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAccountPreferencesResultTypeDef = TypedDict(
    "UpdateAccountPreferencesResultTypeDef",
    {
        "AccountPreferences": AccountPreferencesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateChimeWebhookConfigurationResultTypeDef = TypedDict(
    "UpdateChimeWebhookConfigurationResultTypeDef",
    {
        "WebhookConfiguration": ChimeWebhookConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateSlackChannelConfigurationResultTypeDef = TypedDict(
    "CreateSlackChannelConfigurationResultTypeDef",
    {
        "ChannelConfiguration": SlackChannelConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeSlackChannelConfigurationsResultTypeDef = TypedDict(
    "DescribeSlackChannelConfigurationsResultTypeDef",
    {
        "NextToken": str,
        "SlackChannelConfigurations": List[SlackChannelConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateSlackChannelConfigurationResultTypeDef = TypedDict(
    "UpdateSlackChannelConfigurationResultTypeDef",
    {
        "ChannelConfiguration": SlackChannelConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateTeamsChannelConfigurationResultTypeDef = TypedDict(
    "CreateTeamsChannelConfigurationResultTypeDef",
    {
        "ChannelConfiguration": TeamsChannelConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTeamsChannelConfigurationResultTypeDef = TypedDict(
    "GetTeamsChannelConfigurationResultTypeDef",
    {
        "ChannelConfiguration": TeamsChannelConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTeamsChannelConfigurationsResultTypeDef = TypedDict(
    "ListTeamsChannelConfigurationsResultTypeDef",
    {
        "NextToken": str,
        "TeamChannelConfigurations": List[TeamsChannelConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateTeamsChannelConfigurationResultTypeDef = TypedDict(
    "UpdateTeamsChannelConfigurationResultTypeDef",
    {
        "ChannelConfiguration": TeamsChannelConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeSlackUserIdentitiesResultTypeDef = TypedDict(
    "DescribeSlackUserIdentitiesResultTypeDef",
    {
        "SlackUserIdentities": List[SlackUserIdentityTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeSlackWorkspacesResultTypeDef = TypedDict(
    "DescribeSlackWorkspacesResultTypeDef",
    {
        "SlackWorkspaces": List[SlackWorkspaceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListMicrosoftTeamsUserIdentitiesResultTypeDef = TypedDict(
    "ListMicrosoftTeamsUserIdentitiesResultTypeDef",
    {
        "TeamsUserIdentities": List[TeamsUserIdentityTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
