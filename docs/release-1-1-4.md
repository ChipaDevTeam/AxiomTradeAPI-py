---
layout: guide
title: "Release Notes 1.1.4"
description: "Release notes for AxiomTradeAPI-py 1.1.4 with automatic browser-session bootstrap and stronger trending recovery handling."
permalink: /release-1-1-4/
---

# Release Notes 1.1.4

## Highlights

Version 1.1.4 improves reliability again for environments where Axiom requires a browser-like initialized session before trending requests succeed.

### Included improvements

- automatic browser-session bootstrap before trending requests
- better recovery guidance in returned error payloads
- improved fallback behavior when the service is unstable across multiple hosts and periods
- safer non-throwing behavior by default for production bots

---

## Upgrade

pip install -U axiomtradeapi

---

## New behavior

The SDK now tries to initialize the same session flow normally triggered by client.connect, which helps users who previously got repeated 500 errors even on both 1h and 5m.

If the live service is still unavailable, the returned payload now includes clear diagnostics and suggested next steps.
