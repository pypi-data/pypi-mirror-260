# The settings below must match their equivalents, if applicable, in:
# * resemble/settings.h
# * <possibly other languages by the time you read this>

# gRPC max message size to transmit large actor state data.
MAX_SIDECAR_GRPC_MESSAGE_LENGTH_BYTES = 100 * 1024 * 1024

ENVOY_PROXY_IMAGE = 'envoyproxy/envoy:v1.24.0'

# The path to the directory where Resemble state is stored.
RESEMBLE_STATE_DIRECTORY = '/var/run/resemble/state'

# The names of environment variables that are present both in `rsm dev` and in Kubernetes.
# TODO: The API key should likely be provided by a file in production, to allow for rotation.
ENVVAR_RSM_CLOUD_API_KEY = 'RSM_CLOUD_API_KEY'
ENVVAR_RSM_CLOUD_GATEWAY_ADDRESS = 'RSM_CLOUD_GATEWAY_ADDRESS'
ENVVAR_RSM_CLOUD_GATEWAY_SECURE_CHANNEL = 'RSM_CLOUD_GATEWAY_SECURE_CHANNEL'

# The names of environment variables that are only present when running in `rsm dev`.
ENVVAR_RSM_DEV = 'RSM_DEV'
ENVVAR_RSM_DEV_NAME = 'RSM_DEV_NAME'
ENVVAR_RSM_DEV_SECRETS_DIRECTORY = 'RSM_DEV_SECRETS_DIRECTORY'
ENVVAR_RSM_DOT_RSM_DEV_DIRECTORY = 'RSM_DOT_RSM_DEV_DIRECTORY'
ENVVAR_RSM_DEV_LOCAL_ENVOY = 'RSM_DEV_LOCAL_ENVOY'
ENVVAR_RSM_DEV_LOCAL_ENVOY_PORT = 'RSM_DEV_LOCAL_ENVOY_PORT'
ENVVAR_RSM_DEV_INSPECT_PORT = 'RSM_DEV_INSPECT_PORT'

# The name of an environment variable that's only present when running on
# Kubernetes.
ENVVAR_KUBERNETES_SERVICE_HOST = 'KUBERNETES_SERVICE_HOST'

# When we set up servers we often need to listen on every addressable
# interface on the local machine. This is especially important in some
# circumstances where networks may be rather convoluted, e.g., when we
# have local Docker containers.
EVERY_LOCAL_NETWORK_ADDRESS = '0.0.0.0'

# Ports that Resemble is, by default, reachable on for gRPC and HTTP traffic
# from clients running outside the Resemble cluster. These are the ports that
# users will use in their configuration/code when they choose how to connect to
# a Resemble cluster.
#
# Note that these are defaults; some environments may override these settings.
# Furthermore, many environments may only have one of these ports exposed.
#
# The insecure port serves unencrypted traffic. The secure port serves traffic
# that uses TLS.
DEFAULT_INSECURE_PORT = 9990
DEFAULT_SECURE_PORT = 9991

# Normally, application IDs are not very human-readable - they're hashes derived
# from a human-readable name. However, we choose a hardcoded human-readable ID
# here, for two reasons:
# 1. We want a human-readable endpoint for the Resemble Cloud; e.g.:
#      cloud.some-cluster.resemble.cloud
# 2. If we need to debug a Kubernetes cluster, we're likely to need to interact
#    with the cloud app. Giving it a human-readable ID makes that easier.
CLOUD_APPLICATION_ID = "cloud"
CLOUD_USER_ID = "cloud"
CLOUD_SPACE_NAME = "cloud"
