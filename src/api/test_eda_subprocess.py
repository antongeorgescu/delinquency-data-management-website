#!/usr/bin/env python3
"""
Test the EDA subprocess call that Flask is using
"""
import subprocess
import sys
import os

# Set up paths exactly as Flask does
current_dir = os.path.dirname(__file__)
output_dir = os.path.join(current_dir, 'static', 'eda_outputs')
os.makedirs(output_dir, exist_ok=True)

script_path = os.path.join(current_dir, 'services', 'run_eda_analysis.py')

# Parameters
n_clusters = 5
n_components = 10

# Build command exactly as Flask does
cmd = [
    sys.executable, script_path,
    '--output_dir', output_dir,
    '--n_clusters', str(n_clusters),
    '--n_components', str(n_components)
]

print("🚀 Testing EDA subprocess call...")
print(f"📂 Current directory: {current_dir}")
print(f"📂 Output directory: {output_dir}")
print(f"📄 Script path: {script_path}")
print(f"⚙️ Command: {' '.join(cmd)}")

# Execute EDA script exactly as Flask does
result = subprocess.run(cmd, capture_output=True, text=True, cwd=current_dir)

print(f"\n📊 Results:")
print(f"Return code: {result.returncode}")
print(f"STDOUT:\n{result.stdout}")
if result.stderr:
    print(f"STDERR:\n{result.stderr}")

if result.returncode == 0:
    print("✅ EDA subprocess completed successfully!")
else:
    print("❌ EDA subprocess failed!")