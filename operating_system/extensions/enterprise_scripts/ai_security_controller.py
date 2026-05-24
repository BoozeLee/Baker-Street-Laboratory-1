#!/usr/bin/env python3
"""
AI Security Controller - Prevents unauthorized system operations
Baker Street Laboratory Security System v1.0
"""

import os
import sys
import json
import hashlib
import subprocess
import logging
from datetime import datetime
from typing import Dict, List, Optional

class AISecurityController:
    """Security controller to prevent unauthorized AI operations"""
    
    def __init__(self):
        self.security_log_file = "/home/booze/ai_security.log"
        self.permissions_file = "/home/booze/ai_permissions.json"
        self.blocked_commands = [
            "reboot", "shutdown", "halt", "poweroff", "init 0", "init 6",
            "systemctl reboot", "systemctl shutdown", "systemctl poweroff",
            "sudo reboot", "sudo shutdown", "sudo halt", "sudo poweroff",
            "rm -rf /", "rm -rf /*", "dd if=/dev/zero", "mkfs", "fdisk",
            "chmod 777 /", "chown -R", "passwd", "userdel", "groupdel"
        ]
        self.require_permission_commands = [
            "git push", "git pull", "pip install", "apt install", "apt update",
            "systemctl", "service", "crontab", "cron", "at", "batch"
        ]
        self.setup_logging()
        self.load_permissions()
    
    def setup_logging(self):
        """Setup security logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.security_log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_permissions(self):
        """Load AI permissions from file"""
        try:
            if os.path.exists(self.permissions_file):
                with open(self.permissions_file, 'r') as f:
                    self.permissions = json.load(f)
            else:
                self.permissions = {
                    "allowed_operations": [],
                    "blocked_operations": [],
                    "require_approval": [],
                    "last_updated": datetime.now().isoformat()
                }
                self.save_permissions()
        except Exception as e:
            self.logger.error(f"Error loading permissions: {e}")
            self.permissions = {"allowed_operations": [], "blocked_operations": []}
    
    def save_permissions(self):
        """Save AI permissions to file"""
        try:
            self.permissions["last_updated"] = datetime.now().isoformat()
            with open(self.permissions_file, 'w') as f:
                json.dump(self.permissions, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving permissions: {e}")
    
    def check_command_permission(self, command: str) -> bool:
        """Check if AI has permission to execute a command"""
        self.logger.info(f"Checking permission for command: {command}")
        
        # Check if command is blocked
        for blocked in self.blocked_commands:
            if blocked in command.lower():
                self.logger.warning(f"BLOCKED: Command contains blocked operation: {blocked}")
                return False
        
        # Check if command requires permission
        for req_perm in self.require_permission_commands:
            if req_perm in command.lower():
                if command not in self.permissions.get("allowed_operations", []):
                    self.logger.warning(f"REQUIRES PERMISSION: {command}")
                    return False
        
        # Check if command is explicitly allowed
        if command in self.permissions.get("allowed_operations", []):
            self.logger.info(f"ALLOWED: Command explicitly permitted")
            return True
        
        # Check if command is explicitly blocked
        if command in self.permissions.get("blocked_operations", []):
            self.logger.warning(f"BLOCKED: Command explicitly blocked")
            return False
        
        # Default: allow safe commands
        safe_commands = ["ls", "cat", "grep", "find", "python", "git status", "git log"]
        for safe in safe_commands:
            if command.startswith(safe):
                self.logger.info(f"ALLOWED: Safe command")
                return True
        
        # Unknown command - require permission
        self.logger.warning(f"UNKNOWN COMMAND: {command} - requires permission")
        return False
    
    def request_permission(self, command: str, reason: str = "") -> bool:
        """Request permission for a command from user"""
        print(f"\n🔒 AI SECURITY ALERT 🔒")
        print(f"AI attempting to execute: {command}")
        if reason:
            print(f"Reason: {reason}")
        print(f"Time: {datetime.now()}")
        
        while True:
            response = input("\nAllow this command? (y/n/q to quit): ").lower().strip()
            if response == 'y':
                self.grant_permission(command)
                return True
            elif response == 'n':
                self.deny_permission(command)
                return False
            elif response == 'q':
                print("Exiting...")
                sys.exit(0)
            else:
                print("Please enter y, n, or q")
    
    def grant_permission(self, command: str):
        """Grant permission for a command"""
        if "allowed_operations" not in self.permissions:
            self.permissions["allowed_operations"] = []
        
        if command not in self.permissions["allowed_operations"]:
            self.permissions["allowed_operations"].append(command)
            self.save_permissions()
        
        self.logger.info(f"PERMISSION GRANTED: {command}")
    
    def deny_permission(self, command: str):
        """Deny permission for a command"""
        if "blocked_operations" not in self.permissions:
            self.permissions["blocked_operations"] = []
        
        if command not in self.permissions["blocked_operations"]:
            self.permissions["blocked_operations"].append(command)
            self.save_permissions()
        
        self.logger.warning(f"PERMISSION DENIED: {command}")
    
    def secure_execute(self, command: str, reason: str = "") -> bool:
        """Securely execute a command with permission checking"""
        if not self.check_command_permission(command):
            if not self.request_permission(command, reason):
                return False
        
        try:
            self.logger.info(f"EXECUTING: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.info(f"SUCCESS: {command}")
                return True
            else:
                self.logger.error(f"FAILED: {command} - {result.stderr}")
                return False
        except Exception as e:
            self.logger.error(f"ERROR executing {command}: {e}")
            return False
    
    def create_system_protection(self):
        """Create system protection scripts"""
        protection_script = """#!/bin/bash
# System Protection Script - Baker Street Laboratory

# Prevent unauthorized reboots
alias reboot='echo "REBOOT BLOCKED - Contact system administrator"'
alias shutdown='echo "SHUTDOWN BLOCKED - Contact system administrator"'
alias halt='echo "HALT BLOCKED - Contact system administrator"'
alias poweroff='echo "POWEROFF BLOCKED - Contact system administrator"'

# Log all system commands
export PROMPT_COMMAND='history -a; echo "$(date): $USER@$HOSTNAME: $BASH_COMMAND" >> /home/booze/system_commands.log'

echo "System protection activated - Baker Street Laboratory"
"""
        
        try:
            with open("/home/booze/system_protection.sh", "w") as f:
                f.write(protection_script)
            os.chmod("/home/booze/system_protection.sh", 0o755)
            self.logger.info("System protection script created")
        except Exception as e:
            self.logger.error(f"Error creating protection script: {e}")
    
    def monitor_system(self):
        """Monitor system for suspicious activity"""
        self.logger.info("Starting system monitoring...")
        
        # Monitor critical system files
        critical_files = [
            "/etc/passwd", "/etc/shadow", "/etc/sudoers",
            "/etc/crontab", "/etc/fstab", "/boot/grub/grub.cfg"
        ]
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    file_hash = hashlib.md5(content).hexdigest()
                    
                    # Store hash for comparison
                    hash_file = f"/home/booze/.file_hashes/{os.path.basename(file_path)}.hash"
                    os.makedirs(os.path.dirname(hash_file), exist_ok=True)
                    
                    if os.path.exists(hash_file):
                        with open(hash_file, 'r') as f:
                            stored_hash = f.read().strip()
                        if file_hash != stored_hash:
                            self.logger.warning(f"CRITICAL FILE MODIFIED: {file_path}")
                    else:
                        with open(hash_file, 'w') as f:
                            f.write(file_hash)
                except Exception as e:
                    self.logger.error(f"Error monitoring {file_path}: {e}")

def main():
    """Main security controller"""
    print("🔒 Baker Street Laboratory AI Security Controller 🔒")
    print("Initializing security systems...")
    
    controller = AISecurityController()
    controller.create_system_protection()
    controller.monitor_system()
    
    print("Security controller initialized successfully!")
    print(f"Security log: {controller.security_log_file}")
    print(f"Permissions file: {controller.permissions_file}")
    print("\nTo activate system protection, run:")
    print("source /home/booze/system_protection.sh")
    
    return controller

if __name__ == "__main__":
    main()
