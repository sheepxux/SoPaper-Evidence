# Sopaper Evidence v0.6.1

## Summary

Packaging and registry consistency release for ClawHub.

## Highlights

- bundled all referenced helper scripts inside `sopaper-evidence/scripts/`
- added a canonical upstream source reference to the skill package and marketplace copy
- aligned the published bundle with the runtime instructions in `SKILL.md`
- verified that the bundled topic-driven pipeline runs directly from the published skill package

## Why this release matters

This release removes the main consistency issue that caused ClawHub to flag the skill package as suspicious. The published bundle is now self-contained: the helper scripts referenced by the skill instructions are included in the package, and the upstream repository is explicitly identified.

## Notes

- no trust assumptions were weakened
- the GitHub repository remains the public source of truth
- local `output/` test artifacts were not included in the release
