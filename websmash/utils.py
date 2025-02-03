#!/usr/bin/env python
"""Utility functions for websmash"""
from datetime import datetime

def generate_confirmation_mail(message):
    """Generate confirmation email message from template"""
    confirmation_template = """We have received your feedback to plantiSMASH and will reply to you as soon as possible.
Your message was:

%s
"""
    return confirmation_template % message
