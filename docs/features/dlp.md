# DLP & guardrails

!!! warning "Enterprise tier feature"
    Requires an Enterprise or higher license key.

DLP (Data Loss Prevention) is the org-wide policy layer on top of the [Privacy Shield](privacy-shield.md). Where the Privacy Shield redacts, DLP can **block** or **alert**.

## What you can do

- Block prompts containing certain content (e.g. specific project codenames, internal classification labels).
- Alert org admins on policy hits via mail / Talk / webhook.
- Export an audit log of every blocked or redacted message for compliance review.
- Per-group exceptions: legal team can mention contract numbers, others can't.

## Policy editor

Policies are defined as a list of rules. Each rule has:

- A pattern (regex, dictionary list, or named entity).
- An action: `redact`, `block`, `alert`.
- A scope: org-wide, specific groups, or specific agents.

![DLP policy editor](../img/screenshots/dlp-policy.png)

## Audit log

Every match is recorded with:

- Timestamp + user + agent
- Rule that fired
- Action taken
- Hash of the redacted snippet (no plaintext)

Export as CSV or stream to your SIEM via webhook.
