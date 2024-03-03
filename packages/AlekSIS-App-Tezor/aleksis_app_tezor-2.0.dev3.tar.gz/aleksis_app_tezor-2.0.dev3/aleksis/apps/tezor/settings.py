from aleksis.core.settings import _settings

INSTALLED_APPS = ["payments", "djp_sepa"]

PAYMENT_HOST = _settings.get("payment.host", "localhost:8000")
PAYMENT_MODEL = "tezor.Invoice"
PAYMENT_VARIANT_FACTORY = "aleksis.apps.tezor.util.invoice.provider_factory"

overrides = ["PAYMENT_HOST", "PAYMENT_MODEL", "PAYMENT_VARIANT_FACTORY"]
