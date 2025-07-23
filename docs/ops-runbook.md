# Ops Runbook

Operational procedures.

## Database Backup & Restore

Backup scripts reside in `scripts/backup.ps1` and `scripts/restore.ps1`.
`backup.ps1` creates timestamped, compressed dumps and keeps the last N copies.
`restore.ps1` stops the stack, restores the selected dump, and restarts services.
Both scripts accept optional parameters for the database container name, user, and database if these differ from defaults.
An example task scheduler configuration is provided in `scripts/task_backup.xml`.
Example:

```powershell
./scripts/backup.ps1 -Container db -Database postgres -User postgres
./scripts/restore.ps1 -BackupFile .\backups\postgres_20250101.sql.zip
```
