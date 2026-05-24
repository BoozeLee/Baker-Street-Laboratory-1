#!/usr/bin/env python3
"""
AI Permission Manager - Interactive permission control
Baker Street Laboratory Security System v1.0
"""

import json
import os
from datetime import datetime
from typing import Dict, List

class AIPermissionManager:
    """Interactive permission manager for AI operations"""
    
    def __init__(self):
        self.permissions_file = "/home/booze/ai_permissions.json"
        self.load_permissions()
    
    def load_permissions(self):
        """Load current permissions"""
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
        except Exception as e:
            print(f"Error loading permissions: {e}")
            self.permissions = {"allowed_operations": [], "blocked_operations": []}
    
    def save_permissions(self):
        """Save permissions to file"""
        try:
            self.permissions["last_updated"] = datetime.now().isoformat()
            with open(self.permissions_file, 'w') as f:
                json.dump(self.permissions, f, indent=2)
            print("Permissions saved successfully!")
        except Exception as e:
            print(f"Error saving permissions: {e}")
    
    def show_permissions(self):
        """Display current permissions"""
        print("\n🔒 CURRENT AI PERMISSIONS 🔒")
        print("=" * 50)
        
        print(f"\n✅ ALLOWED OPERATIONS ({len(self.permissions.get('allowed_operations', []))}):")
        for op in self.permissions.get('allowed_operations', []):
            print(f"  • {op}")
        
        print(f"\n❌ BLOCKED OPERATIONS ({len(self.permissions.get('blocked_operations', []))}):")
        for op in self.permissions.get('blocked_operations', []):
            print(f"  • {op}")
        
        print(f"\n⚠️  REQUIRE APPROVAL ({len(self.permissions.get('require_approval', []))}):")
        for op in self.permissions.get('require_approval', []):
            print(f"  • {op}")
        
        print(f"\nLast updated: {self.permissions.get('last_updated', 'Never')}")
    
    def add_allowed_operation(self, operation: str):
        """Add operation to allowed list"""
        if "allowed_operations" not in self.permissions:
            self.permissions["allowed_operations"] = []
        
        if operation not in self.permissions["allowed_operations"]:
            self.permissions["allowed_operations"].append(operation)
            print(f"✅ Added to allowed operations: {operation}")
        else:
            print(f"Operation already allowed: {operation}")
    
    def add_blocked_operation(self, operation: str):
        """Add operation to blocked list"""
        if "blocked_operations" not in self.permissions:
            self.permissions["blocked_operations"] = []
        
        if operation not in self.permissions["blocked_operations"]:
            self.permissions["blocked_operations"].append(operation)
            print(f"❌ Added to blocked operations: {operation}")
        else:
            print(f"Operation already blocked: {operation}")
    
    def remove_operation(self, operation: str):
        """Remove operation from both lists"""
        removed = False
        
        if operation in self.permissions.get("allowed_operations", []):
            self.permissions["allowed_operations"].remove(operation)
            print(f"✅ Removed from allowed operations: {operation}")
            removed = True
        
        if operation in self.permissions.get("blocked_operations", []):
            self.permissions["blocked_operations"].remove(operation)
            print(f"❌ Removed from blocked operations: {operation}")
            removed = True
        
        if not removed:
            print(f"Operation not found: {operation}")
    
    def set_default_permissions(self):
        """Set default security permissions"""
        print("Setting default security permissions...")
        
        # Block dangerous operations
        dangerous_ops = [
            "reboot", "shutdown", "halt", "poweroff",
            "rm -rf /", "rm -rf /*", "dd if=/dev/zero",
            "mkfs", "fdisk", "chmod 777 /", "passwd"
        ]
        
        for op in dangerous_ops:
            self.add_blocked_operation(op)
        
        # Allow safe operations
        safe_ops = [
            "ls", "cat", "grep", "find", "python", "git status",
            "git log", "git diff", "git show", "git branch"
        ]
        
        for op in safe_ops:
            self.add_allowed_operation(op)
        
        print("Default permissions set successfully!")
    
    def interactive_menu(self):
        """Interactive permission management menu"""
        while True:
            print("\n🔒 AI PERMISSION MANAGER 🔒")
            print("=" * 30)
            print("1. Show current permissions")
            print("2. Add allowed operation")
            print("3. Add blocked operation")
            print("4. Remove operation")
            print("5. Set default permissions")
            print("6. Save and exit")
            print("7. Exit without saving")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                self.show_permissions()
            elif choice == "2":
                operation = input("Enter operation to allow: ").strip()
                if operation:
                    self.add_allowed_operation(operation)
            elif choice == "3":
                operation = input("Enter operation to block: ").strip()
                if operation:
                    self.add_blocked_operation(operation)
            elif choice == "4":
                operation = input("Enter operation to remove: ").strip()
                if operation:
                    self.remove_operation(operation)
            elif choice == "5":
                self.set_default_permissions()
            elif choice == "6":
                self.save_permissions()
                print("Goodbye!")
                break
            elif choice == "7":
                print("Exiting without saving...")
                break
            else:
                print("Invalid choice. Please try again.")

def main():
    """Main permission manager"""
    print("🔒 Baker Street Laboratory AI Permission Manager 🔒")
    print("Managing AI operation permissions...")
    
    manager = AIPermissionManager()
    manager.interactive_menu()

if __name__ == "__main__":
    main()
