"""
Type annotations for chatbot service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_chatbot.client import ChatbotClient

    session = Session()
    client: ChatbotClient = session.client("chatbot")
    ```
"""

from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateChimeWebhookConfigurationResultTypeDef,
    CreateSlackChannelConfigurationResultTypeDef,
    CreateTeamsChannelConfigurationResultTypeDef,
    DescribeChimeWebhookConfigurationsResultTypeDef,
    DescribeSlackChannelConfigurationsResultTypeDef,
    DescribeSlackUserIdentitiesResultTypeDef,
    DescribeSlackWorkspacesResultTypeDef,
    GetAccountPreferencesResultTypeDef,
    GetTeamsChannelConfigurationResultTypeDef,
    ListMicrosoftTeamsConfiguredTeamsResultTypeDef,
    ListMicrosoftTeamsUserIdentitiesResultTypeDef,
    ListTeamsChannelConfigurationsResultTypeDef,
    UpdateAccountPreferencesResultTypeDef,
    UpdateChimeWebhookConfigurationResultTypeDef,
    UpdateSlackChannelConfigurationResultTypeDef,
    UpdateTeamsChannelConfigurationResultTypeDef,
)

__all__ = ("ChatbotClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    CreateChimeWebhookConfigurationException: Type[BotocoreClientError]
    CreateSlackChannelConfigurationException: Type[BotocoreClientError]
    CreateTeamsChannelConfigurationException: Type[BotocoreClientError]
    DeleteChimeWebhookConfigurationException: Type[BotocoreClientError]
    DeleteMicrosoftTeamsUserIdentityException: Type[BotocoreClientError]
    DeleteSlackChannelConfigurationException: Type[BotocoreClientError]
    DeleteSlackUserIdentityException: Type[BotocoreClientError]
    DeleteSlackWorkspaceAuthorizationFault: Type[BotocoreClientError]
    DeleteTeamsChannelConfigurationException: Type[BotocoreClientError]
    DeleteTeamsConfiguredTeamException: Type[BotocoreClientError]
    DescribeChimeWebhookConfigurationsException: Type[BotocoreClientError]
    DescribeSlackChannelConfigurationsException: Type[BotocoreClientError]
    DescribeSlackUserIdentitiesException: Type[BotocoreClientError]
    DescribeSlackWorkspacesException: Type[BotocoreClientError]
    GetAccountPreferencesException: Type[BotocoreClientError]
    GetTeamsChannelConfigurationException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ListMicrosoftTeamsConfiguredTeamsException: Type[BotocoreClientError]
    ListMicrosoftTeamsUserIdentitiesException: Type[BotocoreClientError]
    ListTeamsChannelConfigurationsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    UpdateAccountPreferencesException: Type[BotocoreClientError]
    UpdateChimeWebhookConfigurationException: Type[BotocoreClientError]
    UpdateSlackChannelConfigurationException: Type[BotocoreClientError]
    UpdateTeamsChannelConfigurationException: Type[BotocoreClientError]

class ChatbotClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChatbotClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#close)
        """

    def create_chime_webhook_configuration(
        self,
        *,
        WebhookDescription: str,
        WebhookUrl: str,
        SnsTopicArns: Sequence[str],
        IamRoleArn: str,
        ConfigurationName: str,
        LoggingLevel: str = ...,
    ) -> CreateChimeWebhookConfigurationResultTypeDef:
        """
        Creates Chime Webhook Configuration See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/CreateChimeWebhookConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.create_chime_webhook_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#create_chime_webhook_configuration)
        """

    def create_microsoft_teams_channel_configuration(
        self,
        *,
        ChannelId: str,
        TeamId: str,
        TenantId: str,
        IamRoleArn: str,
        ConfigurationName: str,
        ChannelName: str = ...,
        TeamName: str = ...,
        SnsTopicArns: Sequence[str] = ...,
        LoggingLevel: str = ...,
        GuardrailPolicyArns: Sequence[str] = ...,
        UserAuthorizationRequired: bool = ...,
    ) -> CreateTeamsChannelConfigurationResultTypeDef:
        """
        Creates MS Teams Channel Configuration See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/CreateMicrosoftTeamsChannelConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.create_microsoft_teams_channel_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#create_microsoft_teams_channel_configuration)
        """

    def create_slack_channel_configuration(
        self,
        *,
        SlackTeamId: str,
        SlackChannelId: str,
        IamRoleArn: str,
        ConfigurationName: str,
        SlackChannelName: str = ...,
        SnsTopicArns: Sequence[str] = ...,
        LoggingLevel: str = ...,
        GuardrailPolicyArns: Sequence[str] = ...,
        UserAuthorizationRequired: bool = ...,
    ) -> CreateSlackChannelConfigurationResultTypeDef:
        """
        Creates Slack Channel Configuration See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/CreateSlackChannelConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.create_slack_channel_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#create_slack_channel_configuration)
        """

    def delete_chime_webhook_configuration(self, *, ChatConfigurationArn: str) -> Dict[str, Any]:
        """
        Deletes a Chime Webhook Configuration See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/DeleteChimeWebhookConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.delete_chime_webhook_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#delete_chime_webhook_configuration)
        """

    def delete_microsoft_teams_channel_configuration(
        self, *, ChatConfigurationArn: str
    ) -> Dict[str, Any]:
        """
        Deletes MS Teams Channel Configuration See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/DeleteMicrosoftTeamsChannelConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.delete_microsoft_teams_channel_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#delete_microsoft_teams_channel_configuration)
        """

    def delete_microsoft_teams_configured_team(self, *, TeamId: str) -> Dict[str, Any]:
        """
        Deletes the Microsoft Teams team authorization allowing for channels to be
        configured in that Microsoft Teams
        team.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.delete_microsoft_teams_configured_team)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#delete_microsoft_teams_configured_team)
        """

    def delete_microsoft_teams_user_identity(
        self, *, ChatConfigurationArn: str, UserId: str
    ) -> Dict[str, Any]:
        """
        Deletes a Teams user identity See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/DeleteMicrosoftTeamsUserIdentity).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.delete_microsoft_teams_user_identity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#delete_microsoft_teams_user_identity)
        """

    def delete_slack_channel_configuration(self, *, ChatConfigurationArn: str) -> Dict[str, Any]:
        """
        Deletes Slack Channel Configuration See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/DeleteSlackChannelConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.delete_slack_channel_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#delete_slack_channel_configuration)
        """

    def delete_slack_user_identity(
        self, *, ChatConfigurationArn: str, SlackTeamId: str, SlackUserId: str
    ) -> Dict[str, Any]:
        """
        Deletes a Slack user identity See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/DeleteSlackUserIdentity).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.delete_slack_user_identity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#delete_slack_user_identity)
        """

    def delete_slack_workspace_authorization(self, *, SlackTeamId: str) -> Dict[str, Any]:
        """
        Deletes the Slack workspace authorization that allows channels to be configured
        in that
        workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.delete_slack_workspace_authorization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#delete_slack_workspace_authorization)
        """

    def describe_chime_webhook_configurations(
        self, *, MaxResults: int = ..., NextToken: str = ..., ChatConfigurationArn: str = ...
    ) -> DescribeChimeWebhookConfigurationsResultTypeDef:
        """
        Lists Chime Webhook Configurations optionally filtered by ChatConfigurationArn
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/DescribeChimeWebhookConfigurations).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.describe_chime_webhook_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#describe_chime_webhook_configurations)
        """

    def describe_slack_channel_configurations(
        self, *, MaxResults: int = ..., NextToken: str = ..., ChatConfigurationArn: str = ...
    ) -> DescribeSlackChannelConfigurationsResultTypeDef:
        """
        Lists Slack Channel Configurations optionally filtered by ChatConfigurationArn
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/DescribeSlackChannelConfigurations).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.describe_slack_channel_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#describe_slack_channel_configurations)
        """

    def describe_slack_user_identities(
        self, *, ChatConfigurationArn: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeSlackUserIdentitiesResultTypeDef:
        """
        Lists all Slack user identities with a mapped role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.describe_slack_user_identities)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#describe_slack_user_identities)
        """

    def describe_slack_workspaces(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeSlackWorkspacesResultTypeDef:
        """
        Lists all authorized Slack Workspaces for AWS Account See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/DescribeSlackWorkspaces).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.describe_slack_workspaces)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#describe_slack_workspaces)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#generate_presigned_url)
        """

    def get_account_preferences(self) -> GetAccountPreferencesResultTypeDef:
        """
        Get Chatbot account level preferences See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/GetAccountPreferences).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.get_account_preferences)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#get_account_preferences)
        """

    def get_microsoft_teams_channel_configuration(
        self, *, ChatConfigurationArn: str
    ) -> GetTeamsChannelConfigurationResultTypeDef:
        """
        Get a single MS Teams Channel Configurations See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/GetMicrosoftTeamsChannelConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.get_microsoft_teams_channel_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#get_microsoft_teams_channel_configuration)
        """

    def list_microsoft_teams_channel_configurations(
        self, *, MaxResults: int = ..., NextToken: str = ..., TeamId: str = ...
    ) -> ListTeamsChannelConfigurationsResultTypeDef:
        """
        Lists MS Teams Channel Configurations optionally filtered by TeamId See also:
        [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/ListMicrosoftTeamsChannelConfigurations).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.list_microsoft_teams_channel_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#list_microsoft_teams_channel_configurations)
        """

    def list_microsoft_teams_configured_teams(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListMicrosoftTeamsConfiguredTeamsResultTypeDef:
        """
        Lists all authorized MS teams for AWS Account See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/ListMicrosoftTeamsConfiguredTeams).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.list_microsoft_teams_configured_teams)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#list_microsoft_teams_configured_teams)
        """

    def list_microsoft_teams_user_identities(
        self, *, ChatConfigurationArn: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListMicrosoftTeamsUserIdentitiesResultTypeDef:
        """
        Lists all Microsoft Teams user identities with a mapped role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.list_microsoft_teams_user_identities)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#list_microsoft_teams_user_identities)
        """

    def update_account_preferences(
        self, *, UserAuthorizationRequired: bool = ..., TrainingDataCollectionEnabled: bool = ...
    ) -> UpdateAccountPreferencesResultTypeDef:
        """
        Update Chatbot account level preferences See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/UpdateAccountPreferences).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.update_account_preferences)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#update_account_preferences)
        """

    def update_chime_webhook_configuration(
        self,
        *,
        ChatConfigurationArn: str,
        WebhookDescription: str = ...,
        WebhookUrl: str = ...,
        SnsTopicArns: Sequence[str] = ...,
        IamRoleArn: str = ...,
        LoggingLevel: str = ...,
    ) -> UpdateChimeWebhookConfigurationResultTypeDef:
        """
        Updates a Chime Webhook Configuration See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/UpdateChimeWebhookConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.update_chime_webhook_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#update_chime_webhook_configuration)
        """

    def update_microsoft_teams_channel_configuration(
        self,
        *,
        ChatConfigurationArn: str,
        ChannelId: str,
        ChannelName: str = ...,
        SnsTopicArns: Sequence[str] = ...,
        IamRoleArn: str = ...,
        LoggingLevel: str = ...,
        GuardrailPolicyArns: Sequence[str] = ...,
        UserAuthorizationRequired: bool = ...,
    ) -> UpdateTeamsChannelConfigurationResultTypeDef:
        """
        Updates MS Teams Channel Configuration See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/UpdateMicrosoftTeamsChannelConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.update_microsoft_teams_channel_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#update_microsoft_teams_channel_configuration)
        """

    def update_slack_channel_configuration(
        self,
        *,
        ChatConfigurationArn: str,
        SlackChannelId: str,
        SlackChannelName: str = ...,
        SnsTopicArns: Sequence[str] = ...,
        IamRoleArn: str = ...,
        LoggingLevel: str = ...,
        GuardrailPolicyArns: Sequence[str] = ...,
        UserAuthorizationRequired: bool = ...,
    ) -> UpdateSlackChannelConfigurationResultTypeDef:
        """
        Updates Slack Channel Configuration See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/chatbot-2017-10-11/UpdateSlackChannelConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client.update_slack_channel_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chatbot/client/#update_slack_channel_configuration)
        """
