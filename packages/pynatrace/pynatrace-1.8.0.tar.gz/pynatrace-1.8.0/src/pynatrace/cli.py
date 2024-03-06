""" Core module with cli """
import os
from pprint import pprint
import socket
import sys
import click
#import json
#import requests
from datetime import datetime, timedelta
from dynatrace import Dynatrace
#from dynatrace import TOO_MANY_REQUESTS_WAIT
from dynatrace.environment_v2.tokens_api import SCOPE_METRICS_READ, SCOPE_METRICS_INGEST
#from termcolor import cprint
#from requests.api import get, head
#from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
# requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
# Set `verify=False` on `requests.post`.
# requests.post(url='https://example.com', data={'bar':'baz'}, verify=False)


@click.group()
def main():
    """
    pynatrace is a cli for the Dynatrace API\n
    It is based on https://github.com/dynatrace-oss/api-client-python\n
    Set the following environment variables\n
    DT_API_KEY = 'API-YOURAPIKEY'\n
    DT_SERVER_URI = 'https://activegate.example.com:9999/e/tenant_id'

    Example Usage: pynatrace send-log "SMB VERIFICATION FAILED" --severity "ERROR"
    """


@main.command("check-env", short_help="Check required environment variables")
def check_env():
    """Prints out the current necessary environment variables"""
    dt_api_key = os.getenv("DT_API_KEY")
    dt_server_uri = os.getenv("DT_SERVER_URI")
    print(f"Your environment has {dt_api_key} for the variable DT_API_KEY")
    print(f"Your environment has {dt_server_uri} for the variable DT_SERVER_URI")


@main.command("create-maintenance-window", short_help="Create a maintenance window")
@click.argument("window-name")
@click.argument("window-description")
@click.argument("duration-in-hours")
def create_maintenance_window(window_name, window_description, duration_in_hours):
    """ Create a maintenance window that starts immediately
    arguments:
        window-name: The name of the maintenance window.
        window-description: The maintenance window description.
        duration-in-hours: The number of hours before expiration.
    """
    dt_api_key = os.getenv("DT_API_KEY")
    dt_server_uri = os.getenv("DT_SERVER_URI")
    dt = Dynatrace(dt_server_uri, dt_api_key)
    zone_id = "America/Chicago"
    now = datetime.now()
    end = (now + timedelta(hours=int(duration_in_hours))).strftime("%Y-%m-%d %H:%M")
    now = now.strftime("%Y-%m-%d %H:%M")
    sch = dt.maintenance_windows.create_schedule('ONCE', now, end, zone_id)
    window = dt.maintenance_windows.create(window_name,
            window_description, 'PLANNED', 'DETECT_PROBLEMS_DONT_ALERT', sch)
    return window


@main.command(
    "create-token", short_help="Create a new token with read/ingest metric scopes"
)
def create_token():
    """Create a new token"""
    dt_api_key = os.getenv("DT_API_KEY")
    dt_server_uri = os.getenv("DT_SERVER_URI")
    dt = Dynatrace(dt_server_uri, dt_api_key)
    new_token = dt.tokens.create(
        "metrics_token", scopes=[SCOPE_METRICS_READ, SCOPE_METRICS_INGEST]
    )
    print(new_token.token)


@main.command("get-alerts", short_help="Get a list of alerting profiles")
@click.option("--details", is_flag=True)
def get_alerts(details):
    """Get a list of alerting profiles

    parameters:
        details: boolean flag, show details for each profile
    """
    dt_api_key = os.getenv("DT_API_KEY")
    dt_server_uri = os.getenv("DT_SERVER_URI")
    dt = Dynatrace(dt_server_uri, dt_api_key)
    for item in dt.alerting_profiles.list():
        print(item)
        if details:
            pprint(item.get_full_configuration())


@main.command("get-hosts", short_help="Get all hosts with some properties")
def get_hosts():
    """Get a list of monitored hosts"""
    dt_api_key = os.getenv("DT_API_KEY")
    dt_server_uri = os.getenv("DT_SERVER_URI")
    dt = Dynatrace(dt_server_uri, dt_api_key)
    for entity in dt.entities.list(
        'type("HOST")', fields="properties.memoryTotal,properties.monitoringMode"
    ):
        print(entity.entity_id, entity.display_name, entity.properties)


@main.command("get-maintenance-windows", short_help="Get a list of maintenance windows")
@click.option("--details", is_flag=True)
def get_maintenace_windows(details):
    """Get a list of defined maintenance windows"""
    dt_api_key = os.getenv("DT_API_KEY")
    dt_server_uri = os.getenv("DT_SERVER_URI")
    dt = Dynatrace(dt_server_uri, dt_api_key)
    for item in dt.maintenance_windows.list():
        print(item)
        if details:
            pprint(item.get_full_maintenance_window())


@main.command("get-management-zones", short_help="Get a list of management zones")
@click.option("--details", is_flag=True)
def get_management_zones(details):
    """Get a list of defined management zones"""
    dt_api_key = os.getenv("DT_API_KEY")
    dt_server_uri = os.getenv("DT_SERVER_URI")
    dt = Dynatrace(dt_server_uri, dt_api_key)
    for item in dt.management_zones.list():
        print(item)
        if details:
            pprint(item.get_full_configuration())

@main.command("get-management-zone-id", short_help="Get a management zone ID")
@click.argument("zone-name")
def get_management_zone_id(zone_name):
    """Get a management zone ID
    arguments:
        zone-name: The case insensitive zone name
    """
    zone_id = ''
    dt_api_key = os.getenv("DT_API_KEY")
    dt_server_uri = os.getenv("DT_SERVER_URI")
    dt = Dynatrace(dt_server_uri, dt_api_key)
    for item in dt.management_zones.list():
        if zone_name.lower() == (item.name).lower():
            zone_id = item.id
        if zone_id != '':
            print(zone_id)
            return zone_id
    print(f"Management zone {zone_name} was not found")

@main.command("get-notifications", short_help="Get a list of configured notifications")
@click.option("--details", is_flag=True)
def get_notifications(details):
    """Get enabled problem notificaitons"""
    dt_api_key = os.getenv("DT_API_KEY")
    dt_server_uri = os.getenv("DT_SERVER_URI")
    dt = Dynatrace(dt_server_uri, dt_api_key)
    for item in dt.notifications.list():
        print(item)
        if details:
            pprint(item.get_full_configuration())


@main.command("get-problems", short_help="Get a list of open problems")
def get_problems():
    """Get a list of open problems"""
    dt_api_key = os.getenv("DT_API_KEY")
    dt_server_uri = os.getenv("DT_SERVER_URI")
    dt = Dynatrace(dt_server_uri, dt_api_key)
    for item in dt.problems.list():
        status = str(item.status)
        if status == "Status.OPEN":
            pprint(item)


@main.command("search-hosts", short_help="Find hosts with string in display name")
@click.argument("search-string")
def search_hosts(search_string):
    """Search the monitored hosts and return matches

    parameters:
        search-string: string, the string to search for
    """
    dt_api_key = os.getenv("DT_API_KEY")
    dt_server_uri = os.getenv("DT_SERVER_URI")
    dt = Dynatrace(dt_server_uri, dt_api_key)
    for entity in dt.entities.list(
        'type("HOST")', fields="properties.memoryTotal,properties.monitoringMode"
    ):
        if search_string in entity.display_name:
            print(entity.entity_id, entity.display_name, entity.properties)


@main.command("send-log", short_help="Upload a log entry to Dynatrace")
@click.argument("message")
@click.option(
    "--severity",
    default="INFO",
    type=click.Choice(["INFO", "WARN", "ERROR"], case_sensitive=False),
)
def send_log(message, severity):
    """Send a log via the API

    parameters:
        message: The log message to send
        severity: The severity of the log event
    """
    dt_api_key = os.getenv("DT_API_KEY")
    dt_server_uri = os.getenv("DT_SERVER_URI")
    dt = Dynatrace(dt_server_uri, dt_api_key)
    hostname = socket.gethostname()
    log_event = {"host.name": hostname, "severity": severity, "content": message}
    resp = dt.logs.ingest(log_event)
    print(resp)
