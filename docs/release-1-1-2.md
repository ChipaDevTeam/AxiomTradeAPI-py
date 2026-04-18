---
layout: guide
title: "Release Notes 1.1.2"
description: "Release notes for AxiomTradeAPI-py 1.1.2 including trending endpoint migration and reliability fixes."
permalink: /release-1-1-2/
---

# Release Notes 1.1.2

## Highlights

Version 1.1.2 improves trending token reliability and compatibility with Axiom's current API.

### Included fixes

- migrated trending requests to the new trending v2 endpoint
- normalized the array response into a dictionary-friendly structure
- added automatic retries for transient server failures
- added safe fallback between time periods when upstream endpoints return 500 errors
- preserved compatibility with existing code expecting result tokens in a dictionary payload

---

## Upgrade

```bash
pip install -U axiomtradeapi
```

---

## Recommended action for users

If users report trending errors, ask them to upgrade first. The latest release includes the stability fixes needed for the current live endpoint behavior.

---

## Links

- PyPI: https://pypi.org/project/axiomtradeapi/1.1.2/
- Docs: https://chipadevteam.github.io/AxiomTradeAPI-py/
