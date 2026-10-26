# Security boundary

This repository is a portfolio demonstration, not a hardened code-execution service. The local grader imports candidate files into the current Python process and should only be used with trusted examples.

Do not run untrusted submissions with this demo harness. A production evaluator should execute submissions in disposable, least-privilege containers or microVMs with:

- network egress disabled;
- read-only task inputs and an isolated writable directory;
- strict CPU, memory, process and wall-clock limits;
- no host credentials, environment secrets or hidden-test source access;
- controlled output capture and audit logging.

Please report security concerns privately rather than publishing exploit details.

