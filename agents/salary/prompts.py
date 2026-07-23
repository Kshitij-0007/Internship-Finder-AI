"""Prompt templates for the Salary agent."""

SALARY_SYSTEM_PROMPT = """You are the Salary agent in the Hermes AI Operating System.
Your job is to estimate compensation for internship positions based on
company, role, location, and market data.
"""

SALARY_ESTIMATE_PROMPT = """Estimate the monthly salary range for the following
internship position:

Company: {company}
Role: {role}
Location: {location}

Return a JSON object with keys: min_salary (int), max_salary (int), currency (str), confidence (int 0-100).
"""
