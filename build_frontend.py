# Databricks notebook source
# MAGIC %md
# MAGIC # Build Weather Prediction App Frontend
# MAGIC
# MAGIC This notebook builds the React frontend for the Weather Prediction Databricks App using GitHub repo integration.
# MAGIC
# MAGIC **Prerequisites:**
# MAGIC - Your GitHub repo is synced to Databricks via Repos (Workspace → Repos)
# MAGIC - GitHub repo URL: `https://github.com/Marijse-db/weather_prediction_app`
# MAGIC
# MAGIC **Steps:**
# MAGIC 1. Install Node.js and npm
# MAGIC 2. Pull latest changes from GitHub
# MAGIC 3. Build the frontend from the Repos location
# MAGIC 4. Commit and push the built files back to GitHub (optional)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration
# MAGIC
# MAGIC **Update the `REPO_PATH` below to match your Databricks Repos location.**

# COMMAND ----------

# Set your repo path - UPDATE THIS!
REPO_PATH = "/Workspace/Users/marijse.vandenberg@databricks.com/weather_prediction_app"

# Verify the repo exists
import os
if not os.path.exists(REPO_PATH):
    print(f"⚠️  Repository not found at: {REPO_PATH}")
    print("\nTo find your repo path:")
    print("1. Go to Workspace → Repos in Databricks")
    print("2. Right-click your repo → Copy path")
    print("3. Update REPO_PATH in the cell above")
    raise FileNotFoundError(f"Repository not found: {REPO_PATH}")
else:
    print(f"✅ Repository found: {REPO_PATH}")
    print(f"📁 Contents: {os.listdir(REPO_PATH)}")

# Set environment variable for shell commands
os.environ['REPO_PATH'] = REPO_PATH
print(f"\n✅ REPO_PATH environment variable set: {os.environ['REPO_PATH']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 1: Install Node.js
# MAGIC
# MAGIC This installs Node.js 20.x LTS on the cluster.

# COMMAND ----------

# MAGIC %sh
# MAGIC # Install Node.js 20.x LTS
# MAGIC curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
# MAGIC sudo apt-get install -y nodejs
# MAGIC
# MAGIC # Verify installation
# MAGIC echo "Node.js version:"
# MAGIC node --version
# MAGIC echo ""
# MAGIC echo "npm version:"
# MAGIC npm --version

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: Pull Latest Changes from GitHub
# MAGIC
# MAGIC This ensures you're building from the latest code.

# COMMAND ----------

import subprocess

print(f"📂 Working directory: {REPO_PATH}")
print(f"Pulling latest changes...\n")

result = subprocess.run(
    ["git", "pull", "origin", "main"],
    cwd=REPO_PATH,
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print(result.stderr)

# Show current branch and commit
result = subprocess.run(
    ["git", "branch", "--show-current"],
    cwd=REPO_PATH,
    capture_output=True,
    text=True
)
print(f"Current branch: {result.stdout.strip()}")

result = subprocess.run(
    ["git", "log", "-1", "--oneline"],
    cwd=REPO_PATH,
    capture_output=True,
    text=True
)
print(f"Latest commit: {result.stdout.strip()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: Install Frontend Dependencies
# MAGIC
# MAGIC This runs `npm install` in the frontend directory.

# COMMAND ----------

import subprocess

frontend_path = os.path.join(REPO_PATH, "frontend")
print(f"📂 Frontend directory: {frontend_path}")
print(f"Installing dependencies...\n")

result = subprocess.run(
    ["npm", "install"],
    cwd=frontend_path,
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print(result.stderr)

print("\n✅ Dependencies installed!")

# Show installed packages
result = subprocess.run(
    ["npm", "list", "--depth=0"],
    cwd=frontend_path,
    capture_output=True,
    text=True
)
print("\nInstalled packages:")
print(result.stdout)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: Build the Frontend
# MAGIC
# MAGIC This runs `npm run build` to create the production build.

# COMMAND ----------

import subprocess

frontend_path = os.path.join(REPO_PATH, "frontend")
print(f"📂 Building frontend in: {frontend_path}\n")

result = subprocess.run(
    ["npm", "run", "build"],
    cwd=frontend_path,
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print(result.stderr)

print("\n✅ Build completed!")

# Show build output
dist_path = os.path.join(frontend_path, "dist")
if os.path.exists(dist_path):
    print(f"\n📦 Built files in {dist_path}:")
    for item in os.listdir(dist_path):
        item_path = os.path.join(dist_path, item)
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path)
            print(f"  - {item} ({size:,} bytes)")
        else:
            print(f"  - {item}/ (directory)")
else:
    print(f"\n⚠️ Dist directory not found at: {dist_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 5: Verify Build Output
# MAGIC
# MAGIC Check the structure of the built files.

# COMMAND ----------

import os

dist_path = os.path.join(REPO_PATH, "frontend", "dist")
print(f"📦 Build output structure: {dist_path}\n")

if os.path.exists(dist_path):
    # Show directory tree
    for root, dirs, files in os.walk(dist_path):
        level = root.replace(dist_path, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:10]:  # Limit to first 10 files per directory
            size = os.path.getsize(os.path.join(root, file))
            print(f"{subindent}{file} ({size:,} bytes)")
        if len(files) > 10:
            print(f"{subindent}... and {len(files) - 10} more files")

    # Check key files
    print("\n✅ Key files:")
    index_html = os.path.join(dist_path, "index.html")
    if os.path.exists(index_html):
        print(f"  - index.html: {os.path.getsize(index_html):,} bytes")
    else:
        print("  - ⚠️ index.html not found!")

    assets_dir = os.path.join(dist_path, "assets")
    if os.path.exists(assets_dir):
        asset_count = len(os.listdir(assets_dir))
        print(f"  - assets/ directory: {asset_count} files")
    else:
        print("  - ⚠️ assets/ directory not found!")
else:
    print(f"⚠️ Build output not found at: {dist_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 6: Copy Build to DBFS (Optional)
# MAGIC
# MAGIC If you need to download the build locally, copy it to DBFS first.

# COMMAND ----------

import shutil

dist_path = os.path.join(REPO_PATH, "frontend", "dist")
dbfs_dest = "/dbfs/tmp/weather-app-dist"

if os.path.exists(dist_path):
    # Remove old copy if exists
    if os.path.exists(dbfs_dest):
        shutil.rmtree(dbfs_dest)

    # Copy to DBFS
    shutil.copytree(dist_path, dbfs_dest)

    print(f"✅ Build copied to DBFS")
    print(f"\nDBFS location: dbfs:/tmp/weather-app-dist/")
    print(f"\nDownload from your local machine:")
    print(f"databricks fs cp -r dbfs:/tmp/weather-app-dist/ frontend/dist/ --overwrite")
else:
    print(f"⚠️ Cannot copy - dist directory not found at: {dist_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 7: Create Zip File (Optional)
# MAGIC
# MAGIC Create a zip file for easier download.

# COMMAND ----------

import shutil
import os

dist_path = os.path.join(REPO_PATH, "frontend", "dist")
zip_path = "/dbfs/tmp/weather-app-dist"

if os.path.exists(dist_path):
    # Create zip file
    shutil.make_archive(zip_path, 'zip', dist_path)

    zip_file = f"{zip_path}.zip"
    if os.path.exists(zip_file):
        size = os.path.getsize(zip_file)
        print(f"✅ Zip file created!")
        print(f"\nFile: dbfs:/tmp/weather-app-dist.zip")
        print(f"Size: {size:,} bytes ({size / 1024 / 1024:.2f} MB)")
        print(f"\nDownload with:")
        print(f"databricks fs cp dbfs:/tmp/weather-app-dist.zip ./frontend-dist.zip")
        print(f"unzip -o frontend-dist.zip -d frontend/")
    else:
        print("⚠️ Failed to create zip file")
else:
    print(f"⚠️ Cannot create zip - dist directory not found at: {dist_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 8: Commit Build to Git (Optional)
# MAGIC
# MAGIC **⚠️ Warning:** This will commit the `dist/` folder to your Git repository.
# MAGIC
# MAGIC Only run this if you want to commit the built files to version control.
# MAGIC Some teams prefer to build during deployment instead.

# COMMAND ----------

# Uncomment to commit the build to Git
# import subprocess
#
# # Add built files
# subprocess.run(["git", "add", "frontend/dist/"], cwd=REPO_PATH)
#
# # Check if there are changes
# result = subprocess.run(
#     ["git", "diff", "--staged", "--quiet"],
#     cwd=REPO_PATH
# )
#
# if result.returncode != 0:  # There are changes
#     # Configure git
#     subprocess.run(["git", "config", "user.name", "Databricks Build"], cwd=REPO_PATH)
#     subprocess.run(["git", "config", "user.email", "marijse.vandenberg@databricks.com"], cwd=REPO_PATH)
#
#     # Commit
#     result = subprocess.run(
#         ["git", "commit", "-m", "Build frontend dist folder\n\nBuilt via Databricks notebook build_frontend.py"],
#         cwd=REPO_PATH,
#         capture_output=True,
#         text=True
#     )
#     print(result.stdout)
#
#     print("\n✅ Changes committed!")
#     print("\nPush to GitHub:")
#     print("git push origin main")
# else:
#     print("No changes to commit")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next Steps
# MAGIC
# MAGIC ### Option A: Deploy from Repos (Recommended)
# MAGIC
# MAGIC Your app is built and ready in the Repos location. Deploy directly:
# MAGIC
# MAGIC ```bash
# MAGIC databricks apps create weather-prediction-app
# MAGIC databricks apps deploy weather-prediction-app \
# MAGIC   --source-code-path /Workspace/Users/marijse.vandenberg@databricks.com/weather_prediction_app
# MAGIC ```
# MAGIC
# MAGIC ### Option B: Deploy from Local
# MAGIC
# MAGIC Download the build and deploy from your local machine:
# MAGIC
# MAGIC ```bash
# MAGIC # Download the built files
# MAGIC databricks fs cp -r dbfs:/tmp/weather-app-dist/ frontend/dist/ --overwrite
# MAGIC
# MAGIC # Deploy
# MAGIC databricks apps create weather-prediction-app
# MAGIC databricks apps deploy weather-prediction-app \
# MAGIC   --source-code-path /Workspace/Users/marijse.vandenberg@databricks.com/weather-prediction-app
# MAGIC ```
# MAGIC
# MAGIC ### Test the App
# MAGIC
# MAGIC After deployment, get the app URL:
# MAGIC ```bash
# MAGIC databricks apps get weather-prediction-app
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary
# MAGIC
# MAGIC ✅ **Completed:**
# MAGIC - Installed Node.js 20.x LTS
# MAGIC - Pulled latest code from GitHub
# MAGIC - Installed npm dependencies
# MAGIC - Built production frontend (dist/)
# MAGIC - Copied build to DBFS for download
# MAGIC - Created zip file for download
# MAGIC
# MAGIC 🚀 **Your Weather Prediction App is ready to deploy!**
