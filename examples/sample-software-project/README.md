# Isolated SoftwareFeature PoC

Bounded sample used to validate Architect → Coder → gates → independent Reviewer → Run Report.

Run:

```powershell
python -m unittest discover -s tests -v
python -m compileall -q .
```

No external services, credentials, Router changes or production state are involved.
