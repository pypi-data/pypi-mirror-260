# msgraph-py

## Description

This package contains API wrappers to simplify interaction with Microsoft Graph API through Python functions.

Some of the benefits of `msgraph-py` are:

- Automatic caching and renewal of access tokens, avoiding unnecessary API-calls.
- Sets the correct headers and parameters for you when required (advanced queries).
- Pages results automatically when retrieving large datasets.
- Useful logging and error messages with the Python logging module.
- Optional integration with Django settings.py for reading environment variables.

> [!NOTE]  
> The latest published version of this package can be found at [pypi.org/project/msgraph-py](https://pypi.org/project/msgraph-py/)

### List of available functions

#### Identity

- [`get_user()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/identity.py#L12-L36)
- [`get_user_risk()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/identity.py#L260-L285)
- [`revoke_refresh_tokens()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/identity.py#L98-L107)
- [`list_auth_methods()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/identity.py#L133-L142)
- [`delete_auth_method()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/identity.py#L170-L182)
- [`reset_strong_auth()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/identity.py#L227-L237)
- [`get_signin()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/identity.py#L347-L370)

#### Groups

- [`get_group()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/groups.py#L12-L36)
- [`list_group_members()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/groups.py#L100-L124)
- [`add_group_member()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/groups.py#L183-L199)
- [`remove_group_member()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/groups.py#L245-L258)

#### Devices

- [`get_device()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/devices.py#L13-L37)
- [`delete_device()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/devices.py#L101-L110)
- [`list_owned_devices()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/devices.py#L136-L159)
- [`get_laps_password()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/devices.py#L218-L231)

#### Mail

- [`send_mail()`](https://github.com/fedamerd/msgraph-py/blob/main/msgraph/mail.py#L18-L47)

## Getting Started

1. Create an app registration in Entra ID with the necessary Graph application permissions for the functions you intend to use:  
[Authentication and authorization steps](https://learn.microsoft.com/en-us/graph/auth-v2-service?tabs=http#authentication-and-authorization-steps)

2. Install the latest version of the package:

    ```console
    python3 -m pip install msgraph-py
    ```

3. Configure environment variables:
    - If used within a Django project, `msgraph-py` will by default first attempt to load the following variables from the project's `settings.py`:

        ```python
        # project/settings.py

        AAD_TENANT_ID = "00000000-0000-0000-0000-000000000000"
        AAD_CLIENT_ID = "00000000-0000-0000-0000-000000000000"
        AAD_CLIENT_SECRET = "client-secret-value"
        ```

    - Alternatively you will need to set the following key-value pairs in `os.environ`:

        ```python
        import os

        os.environ["AAD_TENANT_ID"] = "00000000-0000-0000-0000-000000000000"
        os.environ["AAD_CLIENT_ID"] = "00000000-0000-0000-0000-000000000000"
        os.environ["AAD_CLIENT_SECRET"] = "client-secret-value"
        ```

> [!WARNING]  
> You should **never** store sensitive credentials or secrets in production code or commit them to your repository. Always load them at runtime from a secure location or from a local file excluded from the repository.

## Usage examples

### Get a single user by objectId or userPrincipalName

```python
from msgraph import get_user

user = get_user("user@example.com")
```

List of returned properties for [user resource type](https://learn.microsoft.com/en-us/graph/api/resources/user#properties).

### Get a list of users using advanced query parameters

```python
from msgraph import get_user

filtered_users = get_user(
    filter="startsWith(department, 'sales')",
    select=[
        "displayName",
        "department",
        "createdDateTime",
    ],
    orderby="createdDateTime desc",
    all=True,
)
```

List of returned properties for [user resource type](https://learn.microsoft.com/en-us/graph/api/resources/user#properties).

### Get a users Entra ID joined devices

```python
from msgraph import list_owned_devices

user_devices = list_owned_devices(
    user_id="user@example.com",
    filter="isManaged eq true and trustType eq 'AzureAd'",
    select=[
        "deviceId",
        "displayName",
        "isCompliant",
        "approximateLastSignInDateTime",
    ],
    orderby="approximateLastSignInDateTime desc",
)
```

List of returned properties for [device resource type](https://learn.microsoft.com/en-us/graph/api/resources/device#properties).

### Send an e-mail with attachments

```python
from msgraph import send_mail

send_mail(
    sender_id="noreply@example.com",
    recipients=[
        "john.doe@example.com",
        "jane.doe@example.com",
    ],
    subject="Mail from Graph API",
    body="<h1>Content of the mail body</h1>",
    is_html=True,
    priority="high",
    attachments=[
        "/path/to/file1.txt",
        "/path/to/file2.txt",
    ],
)
```

## API documentation

- [Authentication and authorization basics](https://learn.microsoft.com/en-us/graph/auth/auth-concepts)
- [Use query parameters to customize responses](https://learn.microsoft.com/en-us/graph/query-parameters)
- [Microsoft Entra authentication methods API overview](https://learn.microsoft.com/en-us/graph/api/resources/authenticationmethods-overview)

### Resource types and properties

- [authenticationMethod resource type](https://learn.microsoft.com/en-us/graph/api/resources/authenticationmethod)
- [device resource type](https://learn.microsoft.com/en-us/graph/api/resources/device#properties)
- [directoryObject resource type](https://learn.microsoft.com/en-us/graph/api/resources/directoryobject)
- [group resource type](https://learn.microsoft.com/en-us/graph/api/resources/group#properties)
- [riskyUser resource type](https://learn.microsoft.com/en-us/graph/api/resources/riskyuser#properties)
- [signIn resource type](https://learn.microsoft.com/en-us/graph/api/resources/signin#properties)
- [user resource type](https://learn.microsoft.com/en-us/graph/api/resources/user#properties)
