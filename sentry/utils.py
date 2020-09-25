import gzip
import io
import json
from datetime import datetime, timedelta

import requests
import sentry_sdk
from sentry_sdk import Transport, capture_exception, configure_scope
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.rq import RqIntegration
from sentry_sdk.utils import capture_internal_exceptions, logger

import frappe

def init_sentry():
	sentry_dsn = get_sentry_dsn()
	if not sentry_dsn:
		return

	enabled = True
	if frappe.conf.get("developer_mode"):
		# You can set this in site_config.json
		# ... enable_sentry_developer_mode: 1 ...
		enabled = frappe.conf.get("enable_sentry_developer_mode", False)

	if enabled:
		sentry_sdk.init(sentry_dsn, integrations=[RqIntegration(), RedisIntegration()])

def handle():
	init_sentry()
	with configure_scope() as scope:
		scope.user = {"email": frappe.session.user}
		scope.set_tag("site", frappe.local.site)
	capture_exception()

@frappe.whitelist(allow_guest=True)
def get_sentry_dsn():
	sentry_dsn = frappe.conf.get("sentry_dsn")
	if not sentry_dsn:
		sentry_dsn = frappe.db.get_single_value("Sentry Settings", "sentry_dsn")
	return sentry_dsn
