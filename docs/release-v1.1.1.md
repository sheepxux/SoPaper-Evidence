# Sopaper Evidence v1.1.1

Security-focused maintenance release.

## Changes

- Add public URL safety checks before external fetches.
- Reject localhost, private-network, link-local, multicast, reserved, unspecified, non-HTTP(S), and credential-bearing URLs.
- Revalidate redirect targets before following them.
- Filter search results through the same public URL guard before writing source lists.

## Verification

- Python compilation passes for root scripts and packaged scripts.
- Localhost fetch smoke test is blocked before any network request.
- Topic search smoke test still returns public arXiv/GitHub results.
