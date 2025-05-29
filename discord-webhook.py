#!/usr/bin/env python3
# Discord Webhook

import os
import sys
import requests
import json


def GetPluginParams():
    webhook_url = os.environ.get("NOTIFY_PARAMETER_1")
    if not webhook_url or webhook_url == "None":
        print("Error: Webhook URL missing in NOTIFY_PARAMETER_1")
        return 2, ""
    return 0, webhook_url


def GetNotificationDetails():
    env = os.environ
    what = env.get("NOTIFY_WHAT", "SERVICE")
    
    hostname = env.get("NOTIFY_HOSTNAME", "Unknown")
    alias = env.get("NOTIFY_HOSTALIAS", "Unknown")
    address = env.get("NOTIFY_HOSTADDRESS", "Unknown")
    
    service = env.get("NOTIFY_SERVICEDESC", "N/A")
    output_service = env.get("NOTIFY_SERVICEOUTPUT", "No Output")
    long_output_service = env.get("NOTIFY_LONGSERVICEOUTPUT", "")
    perf_data = env.get("NOTIFY_SERVICEPERFDATA", "")
    state = env.get("NOTIFY_SERVICESTATE", "UNKNOWN")
    last_state = env.get("NOTIFY_LASTSERVICESTATE", "UNKNOWN")
    
    output_host = env.get("NOTIFY_HOSTOUTPUT", "No Output")
    long_output_host = env.get("NOTIFY_LONGHOSTOUTPUT", "")
    host_state = env.get("NOTIFY_HOSTSTATE", "UNKNOWN")
    last_host_state = env.get("NOTIFY_PREVIOUSHOSTHARDSTATE", "UNKNOWN")
    
    if what == "SERVICE":
        event = f"{last_state} -> {state}"
        title = f"🔔 CheckMK Alert: {hostname}/{service}"
        fields = [
            {"name": "Host", "value": hostname, "inline": True},
            {"name": "Service", "value": service, "inline": True},
            {"name": "Event", "value": event, "inline": False},
            {"name": "Output", "value": output_service or "No Output", "inline": False},
        ]
        color = 16711680 if state == "CRITICAL" else 16776960 if state == "WARNING" else 65280
    else:
        event = f"{last_host_state} → {host_state}"
        title = f"🔔 CheckMK Host Alert: {hostname}"
        fields = [
            {"name": "Host", "value": hostname, "inline": True},
            {"name": "State Change", "value": event, "inline": True},
            {"name": "Output", "value": output_host or "No Output", "inline": False},
        ]
        color = 16711680 if host_state == "DOWN" else 65280

    payload = {
        "embeds": [
            {
                "title": title,
                "color": color,
                "fields": fields
            }
        ]
    }
    return payload


def SendDiscordWebhook(webhook_url, data):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
        if response.status_code == 204:
            print("Discord webhook: Sent successfully.")
        else:
            print(f"Discord webhook: Failed with status {response.status_code}")
            print(response.text)
            return 2
    except Exception as e:
        print(f"Discord webhook: Error occurred: {e}")
        return 2
    return 0


def main():
    code, webhook_url = GetPluginParams()
    if code != 0:
        return code
    payload = GetNotificationDetails()
    return SendDiscordWebhook(webhook_url, payload)


if __name__ == '__main__':
    sys.exit(main())
