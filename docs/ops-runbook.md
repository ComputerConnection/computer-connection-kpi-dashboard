# Ops Runbook

Operational procedures.

## Database Backup & Restore

Backup scripts reside in `scripts/backup.ps1` and `scripts/restore.ps1`.
`backup.ps1` creates timestamped, compressed dumps and keeps the last N copies.
`restore.ps1` stops the stack, restores the selected dump, and restarts services.
An example task scheduler configuration is provided in `scripts/task_backup.xml`.
