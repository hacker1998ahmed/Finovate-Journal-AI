# Finovate Journal AI - Backup Service

"""
Backup and restore service for Finovate Journal AI.
Supports manual and automatic backups with compression.
"""

import shutil
import zipfile
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class BackupService:
    """Service for database backup and restore operations."""
    
    def __init__(self, backup_dir: str = "./backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Backup directory: {self.backup_dir.absolute()}")
    
    def create_backup(self, db_path: str, 
                      include_logs: bool = False,
                      description: str = "") -> Optional[str]:
        """
        Create a backup of the database.
        
        Args:
            db_path: Path to the SQLite database file
            include_logs: Whether to include log files
            description: Optional description for the backup
            
        Returns:
            Path to the backup file, or None if failed
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"finovate_backup_{timestamp}.zip"
            backup_path = self.backup_dir / backup_name
            
            # Files to backup
            files_to_backup = [db_path]
            
            if include_logs:
                log_dir = Path("./logs")
                if log_dir.exists():
                    files_to_backup.extend(log_dir.glob("*.log"))
            
            # Create metadata
            metadata = {
                "backup_date": timestamp,
                "description": description,
                "files": [str(f) for f in files_to_backup],
                "version": "1.0.0",
                "developer": "Ahmed Mostafa Ibrahim - Finovate AHMED EG"
            }
            
            # Create zip archive
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in files_to_backup:
                    if Path(file_path).exists():
                        arcname = Path(file_path).name
                        zipf.write(file_path, arcname)
                        logger.info(f"Added to backup: {file_path}")
                
                # Add metadata
                metadata_path = self.backup_dir / "backup_metadata.json"
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                
                zipf.write(metadata_path, "backup_metadata.json")
                metadata_path.unlink()  # Remove temporary file
            
            logger.info(f"Backup created successfully: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            return None
    
    def restore_backup(self, backup_path: str, 
                       target_db_path: str,
                       confirm: bool = False) -> bool:
        """
        Restore a backup.
        
        Args:
            backup_path: Path to the backup zip file
            target_db_path: Path where database should be restored
            confirm: Must be True to proceed with restore
            
        Returns:
            True if successful, False otherwise
        """
        if not confirm:
            logger.warning("Restore requires confirmation")
            return False
        
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Extract backup
            extract_dir = self.backup_dir / "restore_temp"
            extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(extract_dir)
                logger.info(f"Extracted backup to {extract_dir}")
            
            # Find database file in extracted contents
            db_files = list(extract_dir.glob("*.db"))
            if not db_files:
                logger.error("No database file found in backup")
                return False
            
            # Backup current database before restore
            target = Path(target_db_path)
            if target.exists():
                old_backup = target.with_suffix('.db.pre_restore')
                shutil.copy2(target, old_backup)
                logger.info(f"Current database backed up to {old_backup}")
            
            # Restore database
            shutil.copy2(db_files[0], target_db_path)
            logger.info(f"Database restored to {target_db_path}")
            
            # Cleanup
            shutil.rmtree(extract_dir)
            
            logger.info("Restore completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups."""
        backups = []
        
        try:
            for backup_file in self.backup_dir.glob("finovate_backup_*.zip"):
                stat = backup_file.stat()
                backups.append({
                    "filename": backup_file.name,
                    "path": str(backup_file),
                    "size_bytes": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            
            # Sort by date (newest first)
            backups.sort(key=lambda x: x["created"], reverse=True)
            
        except Exception as e:
            logger.error(f"Failed to list backups: {e}")
        
        return backups
    
    def delete_backup(self, backup_path: str) -> bool:
        """Delete a backup file."""
        try:
            backup_file = Path(backup_path)
            if backup_file.exists() and backup_file.is_file():
                backup_file.unlink()
                logger.info(f"Deleted backup: {backup_path}")
                return True
            else:
                logger.warning(f"Backup not found: {backup_path}")
                return False
        except Exception as e:
            logger.error(f"Failed to delete backup: {e}")
            return False
    
    def get_backup_info(self, backup_path: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific backup."""
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                return None
            
            # Read metadata from zip
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                if "backup_metadata.json" in zipf.namelist():
                    with zipf.open("backup_metadata.json") as f:
                        metadata = json.load(f)
                        return metadata
                
                # Fallback to file info
                stat = backup_file.stat()
                return {
                    "filename": backup_file.name,
                    "size_bytes": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
                }
        
        except Exception as e:
            logger.error(f"Failed to get backup info: {e}")
            return None
    
    def cleanup_old_backups(self, keep_days: int = 30, keep_count: int = 10) -> int:
        """
        Clean up old backups.
        
        Args:
            keep_days: Keep backups newer than this many days
            keep_count: Always keep at least this many backups
            
        Returns:
            Number of backups deleted
        """
        deleted_count = 0
        backups = self.list_backups()
        
        if len(backups) <= keep_count:
            logger.info(f"Only {len(backups)} backups exist, keeping all")
            return 0
        
        cutoff_date = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)
        
        # Keep the most recent backups
        backups_to_keep = backups[:keep_count]
        backup_paths_to_keep = {b["path"] for b in backups_to_keep}
        
        for backup in backups[keep_count:]:
            backup_time = datetime.fromisoformat(backup["created"]).timestamp()
            
            if backup_time < cutoff_date and backup["path"] not in backup_paths_to_keep:
                if self.delete_backup(backup["path"]):
                    deleted_count += 1
        
        logger.info(f"Cleaned up {deleted_count} old backups")
        return deleted_count
    
    def create_automatic_backup(self, db_path: str) -> Optional[str]:
        """Create an automatic backup with standard naming."""
        return self.create_backup(
            db_path=db_path,
            include_logs=False,
            description="Automatic backup"
        )
