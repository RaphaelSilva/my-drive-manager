Feature: Backup Photos from Cloud Drives.

    As a user, I want to backup my photos from cloud drives to a local drive.
    As a user, I want to filter files by extension.
    As a user, I want to overwrite files or skip.
    As a user, I want to be informed if there is not enough space in the destination drive.
    As a user, I want to be informed if some file can not be read.
    As a user, I want the system to use a queue to organize each file copy operation to maintain resilience and allow for a restart if an error occurs.


    Scenario: Backup photos with basic functionality
        Given a mounted cloud drive at "/path/to/cloud/drive"
        And a local drive at "/path/to/destination/drive"
        And the user set "/path/to/cloud/drive" as the source in environment 
        And the user set "/path/to/destination/drive" as the destination in environment
        When the user starts the backup process     
        Then the system should copy all supported photo files from "/path/to/cloud/drive" to "/path/to/destination/drive"
        And the system should organize the copied photos into folders by YEAR/MONTH/DAY
        And the system should provide progress feedback to the user
        And the system should handle any errors during the copy process

    Scenario: Backup photos with file filtering
        Given a mounted cloud drive at "/path/to/cloud/drive"
        And a local drive at "/path/to/destination/drive"
        And the user selects "/path/to/cloud/drive" as the source
        And the user selects "/path/to/destination/drive" as the destination
        And the user filters for files with extension ".jpg"
        When the user starts the backup process
        Then the system should copy only .jpg files from "/path/to/cloud/drive" to "/path/to/destination/drive"
        And the system should organize the copied photos into folders by YEAR/MONTH/DAY
        And the system should provide progress feedback to the user
        And the system should handle any errors during the copy process
        
    Scenario: Backup photos with file overwrite
        Given a mounted cloud drive at "/path/to/cloud/drive"
        And a local drive at "/path/to/destination/drive"
        And the user selects "/path/to/cloud/drive" as the source
        And the user selects "/path/to/destination/drive" as the destination
        And a file "photo.jpg" exists in both the source and destination
        And the user selects the "overwrite" option
        When the user starts the backup process
        Then the system should overwrite the existing "photo.jpg" in the destination
        And the system should organize the copied photos into folders by YEAR/MONTH/DAY
        And the system should provide progress feedback to the user
        And the system should handle any errors during the copy process

    Scenario: Backup photos with file skip
        Given a mounted cloud drive at "/path/to/cloud/drive"
        And a local drive at "/path/to/destination/drive"
        And the user selects "/path/to/cloud/drive" as the source
        And the user selects "/path/to/destination/drive" as the destination
        And a file "photo.jpg" exists in both the source and destination
        And the user selects the "skip" option
        When the user starts the backup process
        Then the system should skip copying the existing "photo.jpg" in the destination
        And the system should organize the copied photos into folders by YEAR/MONTH/DAY
        And the system should provide progress feedback to the user
        And the system should handle any errors during the copy process
    
    Scenario: Handle insufficient disk space
        Given a mounted cloud drive at "/path/to/cloud/drive"
        And a local drive at "/path/to/destination/drive" with insufficient space
        And the user selects "/path/to/cloud/drive" as the source
        And the user selects "/path/to/destination/drive" as the destination
        When the user starts the backup process
        Then the system should detect the insufficient disk space
        And the system should display an error message to the user
        And the system should stop the backup process
        
    Scenario: Handle file access issues
        Given a mounted cloud drive at "/path/to/cloud/drive"
        And a local drive at "/path/to/destination/drive"
        And a file at "/path/to/cloud/drive/protected.jpg" that cannot be read
        And the user selects "/path/to/cloud/drive" as the source
        And the user selects "/path/to/destination/drive" as the destination
        When the user starts the backup process
        Then the system should detect the file access issue for "/path/to/cloud/drive/protected.jpg"
        And the system should display an error message to the user
        And the system should continue the backup for other files