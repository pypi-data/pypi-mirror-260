# Copyright 2024 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Validate configuration options for Open Ondemand data models."""

from enum import Enum, auto


class OODPortalOptions(Enum):
    """`ood_portal.yml` configuration options.

    See Open Ondemand documentation for info about each config option:
    https://osc.github.io/ood-documentation/latest/reference/files/ood-portal-yml.html
    """

    LISTEN_ADDR_PORT = auto()
    SERVERNAME = auto()
    SERVER_ALIASES = auto()
    PROXY_SERVER = auto()
    PORT = auto()
    SSL = auto()
    DISABLE_LOGS = auto()
    LOGROOT = auto()
    ERRORLOG = auto()
    ACCESSLOG = auto()
    LOGFORMAT = auto()
    USE_REWRITES = auto()
    USE_MAINTENANCE = auto()
    MAINTENANCE_IP_ALLOWLIST = auto()
    SECURITY_CSP_FRAME_ANCESTORS = auto()
    SECURITY_STRICT_TRANSPORT = auto()
    LUA_ROOT = auto()
    LUA_LOG_LEVEL = auto()
    USER_MAP_CMD = auto()
    USER_MAP_MATCH = auto()
    USER_ENV = auto()
    MAP_FAIL_URI = auto()
    PUN_STAGE_CMD = auto()
    AUTH = auto()
    CUSTOM_VHOST_DIRECTIVES = auto()
    CUSTOM_LOCATION_DIRECTIVES = auto()
    ROOT_URI = auto()
    ANALYTICS = auto()
    PUBLIC_URI = auto()
    PUBLIC_ROOT = auto()
    LOGOUT_URI = auto()
    LOGOUT_REDIRECT = auto()
    HOST_REGEX = auto()
    NODE_URI = auto()
    RNODE_URI = auto()
    NGINX_URI = auto()
    PUN_URI = auto()
    PUN_SOCKET_ROOT = auto()
    PUN_MAX_RETRIES = auto()
    PUN_PRE_HOOK_ROOT_CMD = auto()
    PUN_PRE_HOOK_EXPORTS = auto()
    OIDC_URI = auto()
    OIDC_DISCOVER_URI = auto()
    OIDC_DISCOVER_ROOT = auto()
    REGISTER_URI = auto()
    REGISTER_ROOT = auto()
    OIDC_PROVIDER_METADATA_URL = auto()
    OIDC_CLIENT_ID = auto()
    OIDC_CLIENT_SECRET = auto()
    OIDC_REMOTE_USER_CLAIM = auto()
    OIDC_SCOPE = auto()
    OIDC_SESSION_INACTIVITY_TIMEOUT = auto()
    OIDC_SESSION_MAX_DURATION = auto()
    OIDC_STATE_MAX_NUMBER_OF_COOKIES = auto()
    OIDC_COOKIE_SAME_SITE = auto()
    OIDC_SETTINGS = auto()
    DEX_URI = auto()
    DEX = auto()


class DexOptions(Enum):
    """`dex` configuration options.

    `dex` configuration options are placed in the ood_portal.yml file.
    See Open Ondemand documentation for info about each config option:
    https://osc.github.io/ood-documentation/latest/authentication/dex.html#dex-configuration
    """

    SSL = auto()
    HTTP_PORT = auto()
    HTTPS_PORT = auto()
    TLS_CERT = auto()
    TLS_KEY = auto()
    STORAGE_FILE = auto()
    CLIENT_ID = auto()
    CLIENT_SECRET = auto()
    CLIENT_REDIRECT_URIS = auto()
    CLIENT_NAME = auto()
    CONNECTORS = auto()
    FRONTEND = auto()
    GRPC = auto()
    EXPIRY = auto()


class NginxStageOptions(Enum):
    """`nginx_stage.yml` configuration options.

    See Open Ondemand documentation for info about each config option:
    https://osc.github.io/ood-documentation/latest/reference/files/nginx-stage-yml.html
    """

    ONDEMAND_VERSION_PATH = auto()
    ONDEMAND_PORTAL = auto()
    ONDEMAND_TITLE = auto()
    PUN_CUSTOM_ENV = auto()
    PUN_CUSTOM_ENV_DECLARATIONS = auto()
    TEMPLATE_ROOT = auto()
    PROXY_USER = auto()
    NGINX_BIN = auto()
    NGINX_SIGNALS = auto()
    MIME_TYPES_PATH = auto()
    PASSENGER_ROOT = auto()
    PASSENGER_RUBY = auto()
    PASSENGER_NODEJS = auto()
    PASSENGER_PYTHON = auto()
    PASSENGER_POOL_IDLE_TIME = auto()
    PASSENGER_LOG_FILE = auto()
    PASSENGER_OPTIONS = auto()
    NGINX_FILE_UPLOAD_MAX = auto()
    PUN_CONFIG_PATH = auto()
    PUN_TMP_ROOT = auto()
    PUN_ACCESS_LOG_PATH = auto()
    PUN_ERROR_LOG_PATH = auto()
    PUN_SECRET_KEY_BASE_PATH = auto()
    PUN_LOG_FORMAT = auto()
    PUN_PID_PATH = auto()
    PUN_SOCKET_PATH = auto()
    PUN_SENDFILE_ROOT = auto()
    PUN_SENDFILE_URI = auto()
    PUN_APP_CONFIGS = auto()
    APP_CONFIG_PATH = auto()
    APP_ROOT = auto()
    APP_REQUEST_URI = auto()
    APP_REQUEST_REGEX = auto()
    APP_TOKEN = auto()
    APP_PASSENGER_ENV = auto()
    USER_REGEX = auto()
    MIN_UID = auto()
    DISABLED_SHELL = auto()
    DISABLE_BUNDLE_USER_CONFIG = auto()
