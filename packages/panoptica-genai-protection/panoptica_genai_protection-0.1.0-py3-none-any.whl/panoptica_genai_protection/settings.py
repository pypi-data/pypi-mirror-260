# auth settings
ESCHER_TOKEN_URL = '/apisec/escher/token_management/serviceapi/apisec_token_management/token'
SCOPE = 'global/services/portshift_request'
SIGN_URL = '/api/serviceMe'  # we sign a fixed endpoint serviceME rather than the explicit request
JWT_TIMEOUT_MS = 1800000  # 30 minutes

DEFAULT_BASE_URL = "https://inspection.marvin-staging-1.staging.eticloud.io"
DEFAULT_AUTH_HOST = "https://production.demo.panoptica.app"