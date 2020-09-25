import frappe
from .utils import get_sentry_dsn, sentry_enabled


def boot_session(bootinfo):
	bootinfo.sentry_dsn = get_sentry_dsn()
	bootinfo.sentry_enabled = sentry_enabled()