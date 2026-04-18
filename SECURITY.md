# Security Policy

The VYOM team takes the security of our ecosystem seriously. We are committed to providing a safe, reliable platform and appreciate the efforts of the security community in helping us maintain that standard.

---

## Supported Versions

We actively provide security patches for the following versions:

| Version | Status |
| :--- | :--- |
| 1.x.x | Supported |
| < 1.0.0 | EOL (End of Life) |

---

## Safe Harbor
To encourage security research and rewarded disclosure, we promise not to initiate legal action against researchers who:
* Engage in "Good Faith" testing and do not intentionally harm VYOM or its users.
* Give us a **reasonable amount of time** to fix the issue before public disclosure.
* Avoid privacy violations, destruction of data, or interruption of our services.

---

## Scope

Please focus your efforts on the core VYOM logic and APIs.

| In-Scope | Out-of-Scope |
| :--- | :--- |
| VYOM Core Logic & Components | Third-party dependencies (npm/yarn packages) |
| API Endpoints & Authentication | Hosting infrastructure (Vercel, GitHub) |
| Data Privacy & Encryption | Social Engineering / Phishing |

---

## How to Report a Vulnerability

**Do not open a Public Issue.** Please follow this process:

1. **Email:** Send your report to `dreamyshivam01@gmail.com`.
2. **Format:** Use the subject line `[SECURITY VULNERABILITY] <Short Description>`.
3. **Details:** Include a PoC (Proof of Concept), steps to reproduce, and the potential impact (CVSS rating if possible).

### Our Response Timeline (SLA)
* **Acknowledgment:** Within 48 hours of receipt.
* **Initial Evaluation:** Within 5 business days.
* **Status Updates:** Every 2 weeks until the vulnerability is patched.
* **Public Disclosure:** We follow a **90-day Coordinated Disclosure** policy.

---

## Acknowledgments
Legitimate security researchers who help us strengthen VYOM will be recognized in our **Security Hall of Fame** (if requested) upon successful mitigation of the reported bug.

---

> [!IMPORTANT]
> Always ensure you are running the latest stable release to benefit from the most recent security hardening.
