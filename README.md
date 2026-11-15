Redis GitHub Repository Manager

A lightweight, command-line Python application for managing GitHub repository metadata using Redis. It demonstrates how to ingest newline-delimited JSON datasets (like those from GH Archive) and perform core database operations using Redis Hashes and Sorted Sets.

Features

Load & List (Load JSON & List Top Repos): Batch-loads repository records from Sample_Repos.json into Redis and displays the top 5 most-watched repositories.

Add or Update (Add or Update a Repo): Performs an "upsert" operation to create a new repository entry or update the watch count of an existing one.

Delete (Delete a Repo): Completely removes a repository from both the detail store and the ranking leaderboard.
