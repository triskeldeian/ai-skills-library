---
name: update-changelog
description: Use when recording completed changes in a project's changelog or verifying and finalizing its unreleased entries before a version bump.
---

# Updating the changelog

Record completed, user-visible changes in the changelog's unreleased section, then verify and finalize that section when a version is prepared for release. Version selection, version files, commits, tags, and publishing belong to the project's release workflow; this skill only edits the changelog.

## Locate the changelog and its conventions

Use project guidance to identify the changelog and any rules about its audience, categories, breaking changes, and release format. Otherwise, look for `CHANGELOG.md`. If no changelog exists, ask the user for permission to create it unless creation is already authorized. If several files could apply, resolve which component or package the change belongs to before editing.

Preserve the existing format and released history. If the project has no established format, use `## [Unreleased]` above the released versions, with category headings such as `### Added`, `### Changed`, `### Fixed`, and `### Removed` only when they contain entries. Create the unreleased section if it is missing.

## Choose the workflow

Read the reference for the current task:

- When a change is ready to commit or has just been committed, read [Recording completed work](references/record-changes.md) to add or update its unreleased entry.
- When preparing a specific release, read [Updating the changelog before a version bump](references/prepare-release.md) to reconcile unreleased entries and finalize the version section.
