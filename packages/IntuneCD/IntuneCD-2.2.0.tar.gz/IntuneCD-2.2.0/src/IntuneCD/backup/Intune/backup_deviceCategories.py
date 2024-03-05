#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module backs up Device Categories in Intune.
"""

from ...intunecdlib.check_prefix import check_prefix_match
from ...intunecdlib.clean_filename import clean_filename
from ...intunecdlib.graph_request import makeapirequest, makeAuditRequest
from ...intunecdlib.process_audit_data import process_audit_data
from ...intunecdlib.process_scope_tags import get_scope_tags_name
from ...intunecdlib.remove_keys import remove_keys
from ...intunecdlib.save_output import save_output

# Set MS Graph endpoint
ENDPOINT = "https://graph.microsoft.com/beta/deviceManagement/deviceCategories"


# Get Device Categories information and save in specified path
def savebackup(path, output, token, prefix, append_id, audit, scope_tags):
    """
    Save Device Categories to a JSON or YAML file.

    :param path: Path to save the backup to
    :param output: Format the backup will be saved as
    :param token: Token to use for authenticating the request
    """

    results = {"config_count": 0, "outputs": []}
    audit_data = None
    configpath = path + "/" + "Device Categories/"
    data = makeapirequest(ENDPOINT, token)
    if audit:
        graph_filter = "componentName eq 'Enrollment'"
        audit_data = makeAuditRequest(graph_filter, token)

    if data["value"]:
        for item in data["value"]:
            if prefix and not check_prefix_match(item["displayName"], prefix):
                continue

            results["config_count"] += 1
            if scope_tags:
                item = get_scope_tags_name(item, scope_tags)
            graph_id = item["id"]
            item = remove_keys(item)
            print("Backing up Device Category: " + item["displayName"])

            # Get filename without illegal characters
            fname = clean_filename(item["displayName"])
            if append_id:
                fname = f"{fname}__{graph_id}"
            # Save Device Categories as JSON or YAML depending on configured value in "-o"
            save_output(output, configpath, fname, item)

            results["outputs"].append(fname)

            if audit_data:
                compare_data = {"type": "resourceId", "value": graph_id}
                process_audit_data(
                    audit_data, compare_data, path, f"{configpath}{fname}.{output}"
                )

    return results
