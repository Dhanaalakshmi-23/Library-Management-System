# Copyright (c) 2026, Dhanaa Lakshmi and contributors
# For license information, please see license.txt

import frappe
from collections import defaultdict


def execute(filters=None):
    columns = [
        {
            "label": "Library Member",
            "fieldname": "library_member",
            "fieldtype": "Link",
            "options": "Library Member"
        },
        {
            "label": "Article",
            "fieldname": "article",
            "fieldtype": "Link",
            "options": "Article"
        },
        {
            "label": "Access Count",
            "fieldname": "access_count",
            "fieldtype": "Int"
        },
        {
            "label": "Reading Frequency",
            "fieldname": "reading_frequency",
            "fieldtype": "Data"
        },
        {
            "label": "Engagement Trend",
            "fieldname": "engagement_trend",
            "fieldtype": "Data"
        }
    ]

    # Fetch only ISSUE transactions
    transactions = frappe.get_all(
        "Library Transaction",
        filters={"type": "Issue"},
        fields=["library_member", "article"]
    )

    # Calculate access count per member per article
    access_map = defaultdict(int)
    for tx in transactions:
        key = (tx.library_member, tx.article)
        access_map[key] += 1

    # Prepare final report data
    data = []
    for (library_member, article), count in access_map.items():
        data.append({
            "library_member": library_member,
            "article": article,
            "access_count": count,
            "reading_frequency": get_reading_frequency(count),
            "engagement_trend": get_engagement_trend(count)
        })

    return columns, data


def get_reading_frequency(count):
    if count >= 10:
        return "High"
    elif count >= 5:
        return "Medium"
    else:
        return "Low"


def get_engagement_trend(count):
    if count >= 10:
        return "Highly Engaged"
    elif count >= 5:
        return "Moderately Engaged"
    else:
        return "Low Engagement"
