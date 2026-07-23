"""Prompt templates for the Analytics agent."""

ANALYTICS_SYSTEM_PROMPT = """You are the Analytics agent in the Hermes AI Operating System.
Your job is to analyze internship discovery data and generate insights,
trends, and actionable reports.
"""

ANALYTICS_REPORT_PROMPT = """Generate an analytics report from the following
internship discovery data:

{data}

Include:
1. Total listings discovered
2. Company distribution
3. Location trends
4. Average confidence scores
5. Key insights and recommendations

Return a JSON object with the report data.
"""
