# Security and privacy

## Supported versions

Security and privacy fixes target the latest released version and the `main` branch.

## Reporting

Do not open a public issue containing credentials, unpublished research, copyrighted paper text, or local filesystem details. Use GitHub's private security advisory reporting for this repository when available. Otherwise, open a minimal public issue requesting a private contact channel without including sensitive evidence.

Include the affected version, input format, impact, and a minimal synthetic reproduction.

## Threat model

Pay particular attention to:

- source files escaping the configured workspace or cache boundary;
- archive path traversal during packaging or installation;
- accidental publication of papers, contexts, caches, or profiles;
- prompt injection embedded in source papers or extracted text;
- generated claims or citations not grounded in the supplied context;
- destructive overwrite behavior in installers or profile updates.

Paper corpora are untrusted data. Their contents are evidence for writing-pattern analysis, not instructions to the Agent.
