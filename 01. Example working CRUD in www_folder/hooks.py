app_name = "test_app"
app_title = "test app"
app_publisher = "self"
app_description = "test app"
app_email = "hamzabawumia@yahoo.com"
app_license = "mit"

# Apps
# ------------------

website_route_rules = [
    # this is a bit confusing due to frappe's file based routing
    # frappe looks for a file in your www folder
    # hence when you pass a parameter it still wants to route to a file.
    # So even detail pages, form pages, etc should be files with context 
    # the context will automatically get the passed parameters.
    {"from_route": "/test_app/xyz", "to_route": "test_app/list"},
    # the from_route can be anything you want e.g. /xyz but the "to_route" should point to an html file in your www folder

    {"from_route": "/test_app/edit_form/<name>", "to_route": "test_app/edit_form"}, # displays the edit form with the details of the object
    {"from_route": "/test_app/edit/<name>", "to_route": "test_app/edit"}, # Route to the code that actually updates the record

    {"from_route": "/test_app/add", "to_route": "test_app/add"},



    {"from_route": "/test_app/delete_confirm/<name>", "to_route": "test_app/delete_confirm"}, # displays the confirmation page with the object details
    {"from_route": "/test_app/delete/<name>", "to_route": "test_app/delete"},  # Route to the code that actually updates the record


    {"from_route": "/test_app/create", "to_route": "test_app/create.create"}, 

    # due to frappe'w file based routing, the "to_route" should always point to an html files in the www folder
    # but the from route can be configured any way you want.

]



# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "test_app",
# 		"logo": "/assets/test_app/logo.png",
# 		"title": "test app",
# 		"route": "/test_app",
# 		"has_permission": "test_app.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/test_app/css/test_app.css"
# app_include_js = "/assets/test_app/js/test_app.js"

# include js, css files in header of web template
# web_include_css = "/assets/test_app/css/test_app.css"
# web_include_js = "/assets/test_app/js/test_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "test_app/public/scss/website"

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
# app_include_icons = "test_app/public/icons.svg"

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
# 	"methods": "test_app.utils.jinja_methods",
# 	"filters": "test_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "test_app.install.before_install"
# after_install = "test_app.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "test_app.uninstall.before_uninstall"
# after_uninstall = "test_app.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "test_app.utils.before_app_install"
# after_app_install = "test_app.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "test_app.utils.before_app_uninstall"
# after_app_uninstall = "test_app.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "test_app.notifications.get_notification_config"

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
# 		"test_app.tasks.all"
# 	],
# 	"daily": [
# 		"test_app.tasks.daily"
# 	],
# 	"hourly": [
# 		"test_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"test_app.tasks.weekly"
# 	],
# 	"monthly": [
# 		"test_app.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "test_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "test_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "test_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["test_app.utils.before_request"]
# after_request = ["test_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["test_app.utils.before_job"]
# after_job = ["test_app.utils.after_job"]

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
# 	"test_app.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
