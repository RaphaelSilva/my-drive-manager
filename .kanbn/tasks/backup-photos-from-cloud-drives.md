---
created: 2025-05-27T13:27:02.362Z
updated: 2025-05-27T13:45:05.908Z
assigned: Raphael
progress: 0.25
tags: []
due: 2025-06-01T00:00:00.000Z
started: 2025-05-25T00:00:00.000Z
---

# Backup Photos and Videos.

This task is to implement a feature that allows users to backup photos from their cloud drives to a local or other cloud drive.

The feature should allow users to:
- Specify source (cloud drive) and destination (local or other cloud drive) paths.
- Filter files by extension (e.g., .jpg).
- Choose to overwrite or skip files that already exist in the destination.
- Be informed about insufficient disk space in the destination drive.
- Be informed if a file cannot be read from the source.
- Have the backup process use a queue for resilience and restart capabilities.
- See progress feedback during the backup.
- Have photos organized into folders by YEAR/MONTH/DAY in the destination.

[Relative document](../../src/feature/backup_photos_from/.feature)

## Sub-tasks

- [ ] Scenario: Backup photos with basic functionality
- [ ] Scenario: Backup photos with file filtering
- [ ] Scenario: Backup photos with file overwrite
- [ ] Scenario: Backup photos with file skip
- [ ] Scenario: Handle insufficient disk space
- [ ] Scenario: Handle file access issues
