"""Configuration and authentication for Databricks Apps."""
import os
from databricks.sdk import WorkspaceClient

# Detect environment
IS_DATABRICKS_APP = bool(os.environ.get("DATABRICKS_APP_NAME"))

def get_workspace_client() -> WorkspaceClient:
    """Get authenticated WorkspaceClient."""
    if IS_DATABRICKS_APP:
        # Remote: Uses auto-injected service principal credentials
        return WorkspaceClient()
    else:
        # Local: Uses Databricks CLI profile
        profile = os.environ.get("DATABRICKS_PROFILE", "DEFAULT")
        return WorkspaceClient(profile=profile)

def get_oauth_token() -> str:
    """Get OAuth token for API authentication."""
    client = get_workspace_client()
    auth_headers = client.config.authenticate()
    if auth_headers and "Authorization" in auth_headers:
        return auth_headers["Authorization"].replace("Bearer ", "")
    return ""

def get_workspace_host() -> str:
    """Get workspace host URL with https:// prefix."""
    if IS_DATABRICKS_APP:
        # IMPORTANT: DATABRICKS_HOST in Databricks Apps is just hostname, no scheme
        host = os.environ.get("DATABRICKS_HOST", "")
        if host and not host.startswith("http"):
            host = f"https://{host}"
        return host
    client = get_workspace_client()
    return client.config.host  # SDK includes https://
