# Security Policy

The `agent-undo` team takes security seriously. As a tool designed to record, audit, and rollback autonomous AI agent operations, maintaining the integrity and confidentiality of your system and operational journals is a top priority.

---

## Supported Versions

Security updates, patches, and fixes are provided for the following versions:

| Version | Supported | Notes |
| :--- | :---: | :--- |
| `0.1.x` | :white_check_mark: | Current active release branch |
| `< 0.1.0` | :x: | Unsupported / pre-release development |

---

## Reporting a Vulnerability

If you discover a security vulnerability in `agent-undo`, please report it responsibly and privately. **Do not create public GitHub issues or forum posts for security vulnerabilities.**

### Disclosure Channels

You can report vulnerabilities through either of the following methods:

1. **GitHub Private Security Advisory (Preferred):**  
   Submit a private advisory report directly via [GitHub Security Advisories](https://github.com/yunaremaia/agent-undo/security/advisories/new).

2. **Email Disclosure:**  
   Send an email to the project maintainer:
   - **Recipient:** `yunare@gmail.com`
   - **Subject Line:** `[SECURITY] [agent-undo] Vulnerability Report - <Brief Description>`

### What to Include in Your Report

To help us investigate and triage the issue quickly, please provide:
- A clear description of the vulnerability and its potential impact.
- Affected `agent-undo` versions and Python environment details (OS, Python version).
- Minimal, reproducible steps or a Proof of Concept (PoC) demonstration.
- Any suggested mitigation, patch, or workaround (if available).

### Response Timeline

- **Acknowledgment:** Within 48 to 72 hours of receiving your initial report.
- **Triage & Assessment:** We will assess the severity, reproduce the findings, and provide regular status updates.
- **Remediation & Advisory:** Once resolved, a patched version will be published. With your permission, we will gladly acknowledge and credit your contribution in the security release notes.

---

## Security Considerations for Users & Integrators

Because `agent-undo` interfaces directly with AI agent execution loops, file system operations, and shell environments, please keep the following security considerations in mind:

### 1. Journal Data & Sensitive Information
- The SQLite journal database records file writes, command invocations, and metadata.
- Ensure that agent workflows involving sensitive API tokens, passwords, or private keys either exclude those commands or restrict read permissions on the journal database (`chmod 600`).
- Do not publicly share journal database files, SARIF dumps, or timeline exports without redacting sensitive environment variables or credentials.

### 2. Reviewing Generated Rollback Scripts
- The `agent-undo rollback` command generates bash scripts (`undo.sh`) to revert recorded operations.
- Always inspect the generated script or run `agent-undo preview` before executing `bash undo.sh`, especially when operating with elevated privileges.

### 3. Agent Hook Execution Environment
- Ensure hooks (`preToolUse`, `postToolUse`) run with the principle of least privilege.
- Avoid passing untrusted or unvalidated external inputs into shell execution wrappers.
