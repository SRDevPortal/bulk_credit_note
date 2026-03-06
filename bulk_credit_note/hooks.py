app_name = "bulk_credit_note"
app_title = "Bulk Credit Note"
app_publisher = "SRIAAS"
app_description = "Bulk creation of Sales Invoice Credit Notes in ERPNext"
app_email = "webdevelopersriaas@gmail.com"
app_license = "mit"

# Installation
before_install = "bulk_credit_note.install.before_install"
after_install = "bulk_credit_note.install.after_install"
after_migrate = "bulk_credit_note.install.after_migrate"

# Uninstallation
before_uninstall = "bulk_credit_note.uninstall.before_uninstall"
after_uninstall = "bulk_credit_note.uninstall.after_uninstall"

doc_events = {
    "Bulk Credit Note": {
        "on_submit": "bulk_credit_note.api.bulk_credit_note.create_credit_notes_on_submit"
    }
}

doctype_js = {
    "Bulk Credit Note": "public/js/bulk_credit_note.js"
}

fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Bulk Credit Note"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "Bulk Credit Note"]]},
    {"dt": "Client Script", "filters": [["module", "=", "Bulk Credit Note"]]},
    {"dt": "Server Script", "filters": [["module", "=", "Bulk Credit Note"]]},
    {"dt": "Workspace", "filters": [["module", "=", "Bulk Credit Note"]]},
    {"dt": "Print Format", "filters": [["module", "=", "Bulk Credit Note"]]},
    {"dt": "Report", "filters": [["module", "=", "Bulk Credit Note"]]},
    {"dt": "Dashboard Chart", "filters": [["module", "=", "Bulk Credit Note"]]},
    {"dt": "Notification", "filters": [["module", "=", "Bulk Credit Note"]]},
    {"dt": "Web Template", "filters": [["module", "=", "Bulk Credit Note"]]},
    {"dt": "Form Tour", "filters": [["module", "=", "Bulk Credit Note"]]},
    {"dt": "Form Tour Step", "filters": [["module", "=", "Bulk Credit Note"]]}
]

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "bulk_credit_note",
# 		"logo": "/assets/bulk_credit_note/logo.png",
# 		"title": "Bulk Credit Note",
# 		"route": "/bulk_credit_note",
# 		"has_permission": "bulk_credit_note.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bulk_credit_note/css/bulk_credit_note.css"
# app_include_js = "/assets/bulk_credit_note/js/bulk_credit_note.js"

# include js, css files in header of web template
# web_include_css = "/assets/bulk_credit_note/css/bulk_credit_note.css"
# web_include_js = "/assets/bulk_credit_note/js/bulk_credit_note.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bulk_credit_note/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "bulk_credit_note/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "bulk_credit_note.utils.jinja_methods",
# 	"filters": "bulk_credit_note.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "bulk_credit_note.install.before_install"
# after_install = "bulk_credit_note.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "bulk_credit_note.uninstall.before_uninstall"
# after_uninstall = "bulk_credit_note.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "bulk_credit_note.utils.before_app_install"
# after_app_install = "bulk_credit_note.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "bulk_credit_note.utils.before_app_uninstall"
# after_app_uninstall = "bulk_credit_note.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bulk_credit_note.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"bulk_credit_note.tasks.all"
# 	],
# 	"daily": [
# 		"bulk_credit_note.tasks.daily"
# 	],
# 	"hourly": [
# 		"bulk_credit_note.tasks.hourly"
# 	],
# 	"weekly": [
# 		"bulk_credit_note.tasks.weekly"
# 	],
# 	"monthly": [
# 		"bulk_credit_note.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "bulk_credit_note.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "bulk_credit_note.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "bulk_credit_note.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["bulk_credit_note.utils.before_request"]
# after_request = ["bulk_credit_note.utils.after_request"]

# Job Events
# ----------
# before_job = ["bulk_credit_note.utils.before_job"]
# after_job = ["bulk_credit_note.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"bulk_credit_note.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

