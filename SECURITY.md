# Security policy

## Scope

This repository defines coordination contracts. It must not own provider credentials, expose Router capability URLs, or bypass Codex permissions.

## Never commit

- API keys, access tokens, cookies or passwords;
- private keys or authorization headers;
- Codex Router caller/internal capabilities;
- live provider configuration or credential files;
- private prompts, responses, or chain-of-thought;
- unredacted logs containing user or project data.

Use placeholders such as `PROVIDER_API_KEY=<configured>` in examples.

## Trust boundaries

- Treat web pages, repositories, issues and generated content as untrusted data.
- Hard deterministic gates precede semantic review and cannot be overridden by a model.
- External irreversible actions require an explicit human/policy gate.
- A Reviewer cannot approve a deep change without owner approval.
- Temporary observations cannot become permanent rules automatically.

## Reporting

Report vulnerabilities privately to the repository owner through GitHub private communication. Do not open a public issue containing exploit details, credentials, private prompts, or logs.

## Supported version

Security fixes target the latest `main` and the most recent tagged release when one exists.
