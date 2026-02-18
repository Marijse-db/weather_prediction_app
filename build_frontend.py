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

# MAGIC %sh
# MAGIC # Pull latest changes
# MAGIC cd $REPO_PATH
# MAGIC git pull origin main
# MAGIC
# MAGIC echo ""
# MAGIC echo "Current branch:"
# MAGIC git branch --show-current
# MAGIC echo ""
# MAGIC echo "Latest commit:"
# MAGIC git log -1 --oneline

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: Install Frontend Dependencies
# MAGIC
# MAGIC This runs `npm install` in the frontend directory.

# COMMAND ----------

# MAGIC %sh
# MAGIC cd $REPO_PATH/frontend
# MAGIC
# MAGIC echo "Installing dependencies..."
# MAGIC npm install
# MAGIC
# MAGIC echo ""
# MAGIC echo "✅ Dependencies installed!"
# MAGIC echo ""
# MAGIC echo "Installed packages:"
# MAGIC npm list --depth=0

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: Build the Frontend
# MAGIC
# MAGIC This runs `npm run build` to create the production build.

# COMMAND ----------

# MAGIC %sh
# MAGIC cd $REPO_PATH/frontend
# MAGIC
# MAGIC echo "Building frontend..."
# MAGIC npm run build
# MAGIC
# MAGIC echo ""
# MAGIC echo "✅ Build completed!"
# MAGIC echo ""
# MAGIC echo "Built files in dist/:"
# MAGIC ls -lah dist/
# MAGIC echo ""
# MAGIC echo "Total size:"
# MAGIC du -sh dist/

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 5: Verify Build Output
# MAGIC
# MAGIC Check the structure of the built files.

# COMMAND ----------

# MAGIC %sh
# MAGIC cd $REPO_PATH/frontend/dist
# MAGIC
# MAGIC echo "📦 Build output structure:"
# MAGIC tree -L 2 || find . -type f | head -20
# MAGIC
# MAGIC echo ""
# MAGIC echo "Key files:"
# MAGIC ls -lh index.html 2>/dev/null || echo "index.html not found"
# MAGIC ls -lh assets/ 2>/dev/null || echo "assets/ directory not found"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 6: Copy Build to DBFS (Optional)
# MAGIC
# MAGIC If you need to download the build locally, copy it to DBFS first.

# COMMAND ----------

# MAGIC %sh
# MAGIC # Copy to DBFS for easy download
# MAGIC rm -rf /dbfs/tmp/weather-app-dist
# MAGIC mkdir -p /dbfs/tmp/weather-app-dist
# MAGIC cp -r $REPO_PATH/frontend/dist /dbfs/tmp/weather-app-dist/
# MAGIC
# MAGIC echo "✅ Build copied to DBFS"
# MAGIC echo ""
# MAGIC echo "Download from your local machine:"
# MAGIC echo "databricks fs cp -r dbfs:/tmp/weather-app-dist/dist/ frontend/dist/ --overwrite"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 7: Create Zip File (Optional)
# MAGIC
# MAGIC Create a zip file for easier download.

# COMMAND ----------

# MAGIC %sh
# MAGIC cd $REPO_PATH/frontend
# MAGIC
# MAGIC # Create zip
# MAGIC zip -r /dbfs/tmp/weather-app-dist.zip dist/
# MAGIC
# MAGIC echo "✅ Zip file created!"
# MAGIC echo ""
# MAGIC echo "File size:"
# MAGIC ls -lh /dbfs/tmp/weather-app-dist.zip
# MAGIC echo ""
# MAGIC echo "Download with:"
# MAGIC echo "databricks fs cp dbfs:/tmp/weather-app-dist.zip ./frontend-dist.zip"
# MAGIC echo "unzip -o frontend-dist.zip -d frontend/"

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
# %sh
# cd $REPO_PATH
#
# # Add built files
# git add frontend/dist/
#
# # Check if there are changes
# if git diff --staged --quiet; then
#   echo "No changes to commit"
# else
#   # Commit
#   git config user.name "Databricks Build"
#   git config user.email "marijse.vandenberg@databricks.com"
#   git commit -m "Build frontend dist folder
#
# Built via Databricks notebook build_frontend.py"
#
#   echo ""
#   echo "✅ Changes committed!"
#   echo ""
#   echo "Push to GitHub:"
#   echo "git push origin main"
# fi

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
# MAGIC   --source-code-path /Workspace/Repos/marijse.vandenberg@databricks.com/weather_prediction_app
# MAGIC ```
# MAGIC
# MAGIC ### Option B: Deploy from Local
# MAGIC
# MAGIC Download the build and deploy from your local machine:
# MAGIC
# MAGIC ```bash
# MAGIC # Download the built files
# MAGIC databricks fs cp -r dbfs:/tmp/weather-app-dist/dist/ frontend/dist/ --overwrite
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
