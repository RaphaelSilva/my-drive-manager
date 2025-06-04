---
created: 2025-05-27T13:27:02.362Z
updated: 2025-05-27T13:45:05.908Z
assigned: Raphael
progress: 0.25
tags: []
due: 2025-06-01T00:00:00.000Z
started: 2025-05-25T00:00:00.000Z
---

# Backup Photos from Cloud Drives.

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

## Scenarios

### Scenario: Backup photos with basic functionality

- Given a mounted cloud drive at "/path/to/cloud/drive"
- And a local drive at "/path/to/destination/drive"
- And the user set "/path/to/cloud/drive" as the source in environment 
- And the user set "/path/to/destination/drive" as the destination in environment
- When the user starts the backup process     
- Then the system should copy all supported photo files from "/path/to/cloud/drive" to "/path/to/destination/drive"
- And the system should organize the copied photos into folders by YEAR/MONTH/DAY
- And the system should provide progress feedback to the user
- And the system should handle any errors during the copy process

### Scenario: Backup photos with file filtering

- Given a mounted cloud drive at "/path/to/cloud/drive"
- And a local drive at "/path/to/destination/drive"
- And the user selects "/path/to/cloud/drive" as the source
- And the user selects "/path/to/destination/drive" as the destination
- And the user filters for files with extension ".jpg"
- When the user starts the backup process
- Then the system should copy only .jpg files from "/path/to/cloud/drive" to "/path/to/destination/drive"
- And the system should organize the copied photos into folders by YEAR/MONTH/DAY
- And the system should provide progress feedback to the user
- And the system should handle any errors during the copy process

### Scenario: Backup photos with file overwrite

- Given a mounted cloud drive at "/path/to/cloud/drive"
- And a local drive at "/path/to/destination/drive"
- And the user selects "/path/to/cloud/drive" as the source
- And the user selects "/path/to/destination/drive" as the destination
- And a file "photo.jpg" exists in both the source and destination
- And the user selects the "overwrite" option
- When the user starts the backup process
- Then the system should overwrite the existing "photo.jpg" in the destination
- And the system should organize the copied photos into folders by YEAR/MONTH/DAY
- And the system should provide progress feedback to the user
- And the system should handle any errors during the copy process

### Scenario: Backup photos with file skip

- Given a mounted cloud drive at "/path/to/cloud/drive"
- And a local drive at "/path/to/destination/drive"
- And the user selects "/path/to/cloud/drive" as the source
- And the user selects "/path/to/destination/drive" as the destination
- And a file "photo.jpg" exists in both the source and destination
- And the user selects the "skip" option
- When the user starts the backup process
- Then the system should skip copying the existing "photo.jpg" in the destination
- And the system should organize the copied photos into folders by YEAR/MONTH/DAY
- And the system should provide progress feedback to the user
- And the system should handle any errors during the copy process

### Scenario: Handle insufficient disk space

- Given a mounted cloud drive at "/path/to/cloud/drive"
- And a local drive at "/path/to/destination/drive" with insufficient space
- And the user selects "/path/to/cloud/drive" as the source
- And the user selects "/path/to/destination/drive" as the destination
- When the user starts the backup process
- Then the system should detect the insufficient disk space
- And the system should display an error message to the user
- And the system should stop the backup process

### Scenario: Handle file access issues

- Given a mounted cloud drive at "/path/to/cloud/drive"
- And a local drive at "/path/to/destination/drive"
- And a file at "/path/to/cloud/drive/protected.jpg" that cannot be read
- And the user selects "/path/to/cloud/drive" as the source
- And the user selects "/path/to/destination/drive" as the destination
- When the user starts the backup process
- Then the system should detect the file access issue for "/path/to/cloud/drive/protected.jpg"
- And the system should display an error message to the user
- And the system should continue the backup for other files

## Sub-tasks

- [ ] Scenario: Backup photos with basic functionality
- [ ] Scenario: Backup photos with file filtering
- [ ] Scenario: Backup photos with file overwrite
- [ ] Scenario: Backup photos with file skip
- [ ] Scenario: Handle insufficient disk space
- [ ] Scenario: Handle file access issues
