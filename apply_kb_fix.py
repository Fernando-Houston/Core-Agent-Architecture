#!/usr/bin/env python3
"""
Apply the knowledge base loader fix to get the system working
"""

import shutil
from pathlib import Path

def apply_fix():
    print("🔧 Applying Knowledge Base Loader Fix...")
    
    # Backup original
    original = Path("knowledge_base_loader.py")
    backup = Path("knowledge_base_loader_original.py")
    fixed = Path("knowledge_base_loader_fixed.py")
    
    if original.exists() and not backup.exists():
        print("   - Creating backup of original...")
        shutil.copy2(original, backup)
    
    # Apply fixed version
    if fixed.exists():
        print("   - Applying fixed version...")
        shutil.copy2(fixed, original)
        print("✅ Fix applied successfully!")
        print("\n📝 What was fixed:")
        print("   - Properly handles nested dictionary structure in JSON files")
        print("   - Extracts content from nested 'content' objects")
        print("   - Builds proper TF-IDF index with actual text content")
        print("   - Improves search relevance scoring")
        print("\n🚀 The system should now return real data instead of 'Limited data available'")
        print("\n⚡ Next steps:")
        print("   1. Restart the API server")
        print("   2. Test queries in the Streamlit chat")
        print("   3. Consider implementing Hugging Face enhancement for even better results")
    else:
        print("❌ Fixed file not found!")

if __name__ == "__main__":
    apply_fix()