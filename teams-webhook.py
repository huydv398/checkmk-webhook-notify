#!/usr/bin/env python3
# Teams-Webhook-modify

import os
import sys
import requests
import json


def GetPluginParams():
    WebHookURL = os.environ.get("NOTIFY_PARAMETER_1")
    if not WebHookURL or WebHookURL == "None":
        print("Teams-plugin: Mandatory first parameter is missing: Webhook URL")
        return 2, ""
    return 0, WebHookURL


def GetNotificationDetails():
    env_vars = os.environ
    HOSTNAME = env_vars.get("NOTIFY_HOSTNAME", "Unknown")
    HOSTALIAS = env_vars.get("NOTIFY_HOSTALIAS", "")
    ADDRESS = env_vars.get("NOTIFY_HOSTADDRESS", "")
    SERVICE = env_vars.get("NOTIFY_SERVICEDESC", "")
    OUTPUT_HOST = env_vars.get("NOTIFY_HOSTOUTPUT", "")
    OUTPUT_SERVICE = env_vars.get("NOTIFY_SERVICEOUTPUT", "")
    LONG_OUTPUT_HOST = env_vars.get("NOTIFY_LONGHOSTOUTPUT", "")
    LONG_OUTPUT_SERVICE = env_vars.get("NOTIFY_LONGSERVICEOUTPUT", "")
    PERF_DATA = env_vars.get("NOTIFY_SERVICEPERFDATA", "")
    STATE = env_vars.get("NOTIFY_SERVICESTATE", "")
    LAST_STATE = env_vars.get("NOTIFY_PREVIOUSSERVICEHARDSTATE", "")
    HOST_STATE = env_vars.get("NOTIFY_HOSTSTATE", "")
    LAST_HOST_STATE = env_vars.get("NOTIFY_LASTHOSTSHORTSTATE", "")
    WHAT = env_vars.get("NOTIFY_WHAT", "SERVICE")

    if WHAT == "SERVICE":
        summary = f"CheckMK {HOSTNAME}/{SERVICE} - {LAST_STATE} -> {STATE}"
        text = f"**Host**: {HOSTNAME}  \n" \
               f"**Service**: {SERVICE}  \n" \
               f"**Event**: {LAST_STATE} → {STATE}  \n" \
               f"**Output**: {OUTPUT_SERVICE or 'N/A'}"
        if PERF_DATA:
            text += f"\n**PerfData**: {PERF_DATA}"
        color = "FF0000" if STATE == "CRITICAL" else "FFA500" if STATE == "WARNING" else "00FF00"
    else:
        summary = f"CheckMK {HOSTNAME} - {HOST_STATE} -> {LAST_HOST_STATE}"
        text = f"**Host**: {HOSTNAME}  \n" \
               f"**Event**: {HOST_STATE} → {LAST_HOST_STATE}  \n" \
               f"**Output**: {OUTPUT_HOST or 'N/A'}"
        color = "FF0000" if HOST_STATE == "DOWN" else "00FF00"

    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": summary,
        "themeColor": color,
        "title": summary,
        "text": text
    }

    return payload


def SendTeamsWebhook(WebHookURL, data):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(WebHookURL, headers=headers, data=json.dumps(data))
        if response.status_code in (200, 204):
            print("Teams-plugin: Notification sent successfully.")
        else:
            print(f"Teams-plugin: Failed to send. Status code: {response.status_code}")
            print(response.text)
            return 2
    except Exception as e:
        print(f"Teams-plugin: Error sending webhook: {e}")
        return 2
    return 0


def main():
    return_code, WebHookURL = GetPluginParams()
    if return_code != 0:
        return return_code

    data = GetNotificationDetails()
    return SendTeamsWebhook(WebHookURL, data)


if __name__ == '__main__':
    sys.exit(main())
