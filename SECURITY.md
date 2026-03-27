# Security Policy

## Reporting a Vulnerability

If you discover a security issue in this plugin (e.g., a rule that fails to catch a secret pattern, or a skill that could leak credentials), please report it responsibly.

**Email:** Open a [private security advisory](https://github.com/TMHSDigital/Steam-Cursor-Plugin/security/advisories/new) on GitHub.

Please include:

- Description of the vulnerability
- Steps to reproduce
- Which skill or rule is affected
- Any suggested fix

## Scope

This plugin contains Markdown skill files and MDC rule files only - no compiled code, no server-side components, and no direct access to Steam APIs. The primary security concerns are:

- **Secrets detection rules** failing to flag sensitive patterns (API keys, credentials, auth tokens)
- **Skills recommending insecure practices** (hardcoding keys, skipping auth validation)
- **MCP server configuration** exposing API keys through improper environment variable handling

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.2.x   | Yes       |
| < 0.2.0 | No        |

## Response Timeline

We aim to acknowledge reports within 48 hours and provide a fix or mitigation within 7 days for confirmed issues.
