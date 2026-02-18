# Databricks notebook source
# MAGIC %md
# MAGIC # Build Weather Prediction App Frontend
# MAGIC
# MAGIC This notebook builds the React frontend for the Weather Prediction Databricks App.
# MAGIC
# MAGIC **Steps:**
# MAGIC 1. Install Node.js and npm
# MAGIC 2. Copy frontend source files to DBFS
# MAGIC 3. Build the frontend
# MAGIC 4. Download the built `dist/` folder back to your local machine
# MAGIC
# MAGIC **Requirements:**
# MAGIC - Upload your `frontend/` folder to DBFS first, or use the cells below to do it via CLI

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 1: Install Node.js

# COMMAND ----------

# MAGIC %sh
# MAGIC # Install Node.js 20.x LTS
# MAGIC curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
# MAGIC sudo apt-get install -y nodejs
# MAGIC
# MAGIC # Verify installation
# MAGIC node --version
# MAGIC npm --version

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: Upload Frontend Source Files
# MAGIC
# MAGIC Run this from your local machine to upload the frontend:
# MAGIC ```bash
# MAGIC databricks fs cp -r frontend/ dbfs:/tmp/weather-app-build/frontend/ --overwrite
# MAGIC ```
# MAGIC
# MAGIC Or use the cell below if you're running from a workspace with access to the files.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: Copy Files and Install Dependencies

# COMMAND ----------

# MAGIC %sh
# MAGIC # Create working directory
# MAGIC rm -rf /tmp/frontend-build
# MAGIC mkdir -p /tmp/frontend-build
# MAGIC
# MAGIC # Copy files from DBFS to local filesystem
# MAGIC cp -r /dbfs/tmp/weather-app-build/frontend /tmp/frontend-build/
# MAGIC
# MAGIC # Navigate and install dependencies
# MAGIC cd /tmp/frontend-build/frontend
# MAGIC npm install
# MAGIC
# MAGIC echo "Dependencies installed successfully!"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: Build the Frontend

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /tmp/frontend-build/frontend
# MAGIC npm run build
# MAGIC
# MAGIC echo "Build completed!"
# MAGIC ls -lah dist/

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 5: Copy Built Files Back to DBFS

# COMMAND ----------

# MAGIC %sh
# MAGIC # Copy the built dist folder to DBFS
# MAGIC rm -rf /dbfs/tmp/weather-app-build/frontend/dist
# MAGIC cp -r /tmp/frontend-build/frontend/dist /dbfs/tmp/weather-app-build/frontend/
# MAGIC
# MAGIC echo "Built files copied to DBFS at: dbfs:/tmp/weather-app-build/frontend/dist/"
# MAGIC ls -lah /dbfs/tmp/weather-app-build/frontend/dist/

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 6: Download Built Files to Local Machine
# MAGIC
# MAGIC Run this command from your local terminal:
# MAGIC ```bash
# MAGIC # Download the built dist folder
# MAGIC databricks fs cp -r dbfs:/tmp/weather-app-build/frontend/dist/ frontend/dist/ --overwrite
# MAGIC
# MAGIC # Or download as a zip
# MAGIC databricks fs cp dbfs:/tmp/weather-app-build/frontend-dist.zip ./frontend-dist.zip
# MAGIC unzip -o frontend-dist.zip -d frontend/
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## Alternative: Create a Zip File for Easy Download

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /tmp/frontend-build/frontend
# MAGIC zip -r /dbfs/tmp/weather-app-build/frontend-dist.zip dist/
# MAGIC
# MAGIC echo "Zip file created at: dbfs:/tmp/weather-app-build/frontend-dist.zip"
# MAGIC echo ""
# MAGIC echo "Download with:"
# MAGIC echo "databricks fs cp dbfs:/tmp/weather-app-build/frontend-dist.zip ./frontend-dist.zip"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verification
# MAGIC
# MAGIC Check the built files:

# COMMAND ----------

# MAGIC %sh
# MAGIC find /dbfs/tmp/weather-app-build/frontend/dist -type f | head -20

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next Steps
# MAGIC
# MAGIC After downloading the `dist/` folder to your local `frontend/dist/`:
# MAGIC
# MAGIC 1. Verify files locally: `ls frontend/dist/`
# MAGIC 2. Test the app locally: `uvicorn app:app --reload --port 8000`
# MAGIC 3. Deploy to Databricks Apps:
# MAGIC    ```bash
# MAGIC    databricks apps create weather-prediction-app
# MAGIC    databricks apps deploy weather-prediction-app --source-code-path /Workspace/Users/your@email.com/weather-prediction-app
# MAGIC    ```
