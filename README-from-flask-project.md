# Flask vuejs app with sqlite database azure app service  
  
## Overview  
  
Deploying a Flask and Vue.js application with a SQLite database to Azure App Service requires a specific architectural design: because Azure App Service container file systems are stateless by default, you must use a persistent storage mount (like Azure Files) or enable persistent storage configuration to prevent your SQLite database from being wiped out during app restarts or scaling events.Below is the structured layout and step-by-step implementation for this full-stack application.  
  
## Project Structure  
  
```  
flask-vue-azure/  
├── backend/  
│   ├── app.py  
│   ├── requirements.txt  
│   └── database/          <-- SQLite DB file will live here  
├── frontend/  
│   ├── src/  
│   ├── package.json  
│   └── vite.config.js     <-- Or vue.config.js  
├── dist/                  <-- Built Vue.js static assets  
├── startup.sh             <-- Azure App Service startup script  
└── requirements.txt       <-- Root requirements file for Azure  
```  
  
## Backend Python  
  
### Flask App  
  
backend/app.py  
```  
import os  
from flask import Flask, jsonify, send_from_directory  
from flask_sqlalchemy import SQLAlchemy  
  
app = Flask(__name__, static_folder='../dist', static_url_path='/')  
  
# CRITICAL FOR AZURE: Store DB in a persistent path or subfolder  
# On Azure Linux App Service, /home is persistent.  
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', 'app.db')  
os.makedirs(os.path.dirname(db_path), exist_ok=True)  
  
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)  
  
# Sample Model  
class Item(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(80), nullable=False)  
  
# API Endpoint  
@app.route('/api/items', methods=['GET'])  
def get_items():  
    items = Item.query.all()  
    return jsonify([{'id': i.id, 'name': i.name} for i in items])  
  
# Catch-all route to serve Vue Router paths  
@app.route('/', defaults={'path': ''})  
@app.route('/<path:path>')  
def catch_all(path):  
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):  
        return send_from_directory(app.static_folder, path)  
    return send_from_directory(app.static_folder, 'index.html')  
  
if __name__ == '__main__':  
    with app.app_context():  
        db.create_all()  
    app.run()  
```  
  
### Requirements  
  
backend/requirements.txt:  
```  
Flask==3.0.3  
Flask-SQLAlchemy==3.1.1  
gunicorn==22.0.0  
```  
  
## Frontend VueJS  
  
### Vite Config  
  
frontend/vite.config.js:  
```  
import { defineConfig } from 'vite'  
import vue from '@vitejs/vite-plugin-vue'  
import path from 'path'  
  
export default defineConfig({  
  plugins: [vue()],  
  build: {  
    // Output directly to the root dist folder  
    outDir: path.resolve(__dirname, '../dist'),  
    emptyOutDir: true  
  },  
  server: {  
    proxy: {  
      // Proxy local API requests to Flask during development  
      '/api': 'http://127.0.0.1:5000'  
    }  
  }  
})  
```  
  
### Package.json  
  
Place this file directly inside your frontend/ directory. It includes scripts optimized for your folder layout and pulls in vue-router.  
  
package.json:  
```  
{  
  "name": "flask-vue-frontend",  
  "private": true,  
  "version": "0.1.0",  
  "type": "module",  
  "scripts": {  
    "dev": "vite",  
    "build": "vite build",  
    "preview": "vite preview"  
  },  
  "dependencies": {  
    "vue": "^3.4.0",  
    "vue-router": "^4.3.0"  
  },  
  "devDependencies": {  
    "@vitejs/plugin-vue": "^5.0.0",  
    "vite": "^5.0.0"  
  }  
}  
```  
  
### Vue Router Configuration  
  
Create a new file at frontend/src/router/index.js. This handles client-side routing.  
  
frontend/src/router/index.js:  
```  
import { createRouter, createWebHistory } from 'vue-router'  
  
// 1. Define your page/view components  
// (Using lazy-loading to keep initial bundle sizes small)  
const HomeView = () => import('../views/HomeView.vue')  
const AboutView = () => import('../views/AboutView.vue')  
  
// 2. Define the route paths  
const routes = [  
  {  
    path: '/',  
    name: 'home',  
    component: HomeView  
  },  
  {  
    path: '/about',  
    name: 'about',  
    component: AboutView  
  }  
]  
  
// 3. Create the router instance  
const router = createRouter({  
  // Using HTML5 History mode. Flask is already configured with  
  // a catch-all route to gracefully support this on Azure!  
  history: createWebHistory(import.meta.env.BASE_URL),  
  routes  
})  
  
export default router  
```  
  
  
### App.vue  
  
Use a relative URL path like /api/items. Because Vite handles the proxy during local development, and Flask hosts the compiled files directly in production, you don't need to hardcode http://localhost:5000.  
  
frontend/src/App.vue:  
```  
<template>  
  <div id="app-layout">  
    <nav class="navigation-bar">  
      <!-- RouterLink prevents page reloads and manages active classes -->  
      <RouterLink to="/">Home</RouterLink> |  
      <RouterLink to="/about">About App</RouterLink>  
    </nav>  
  
    <main class="main-content">  
      <!-- The component matching the current URL path will render here -->  
      <RouterView />  
    </main>  
  </div>  
</template>  
  
<style scoped>  
#app-layout {  
  font-family: sans-serif;  
  max-width: 800px;  
  margin: 0 auto;  
  padding: 1rem;  
}  
.navigation-bar {  
  padding: 1rem 0;  
  border-bottom: 1px solid #eee;  
  margin-bottom: 2rem;  
}  
.navigation-bar a {  
  text-decoration: none;  
  color: #2c3e50;  
  font-weight: bold;  
}  
.navigation-bar a.router-link-exact-active {  
  color: #42b983;  
}  
</main>  
</style>  
```  
  
### HomeView.vue  
  
This component acts as your landing page and fetches live data from your Flask backend API.  
  
frontend/src/views/HomeView.vue:  
```  
<template>  
  <div class="page-container">  
    <h2>Data from SQLite</h2>  
    <p class="subtitle">This view communicates directly with your Flask API endpoints.</p>  
  
    <div class="card">  
      <ul v-if="items.length" class="item-list">  
        <li v-for="item in items" :key="item.id" class="item-row">  
          <span class="badge">ID: {{ item.id }}</span> {{ item.name }}  
        </li>  
      </ul>  
      <p v-else class="empty-state">Loading items from database or table is empty...</p>  
    </div>  
  </div>  
</template>  
  
<script setup>  
import { ref, onMounted } from 'vue'  
  
const items = ref([])  
  
const fetchItems = async () => {  
  try {  
    const response = await fetch('/api/items')  
    if (response.ok) {  
      items.value = await response.json()  
    }  
  } catch (error) {  
    console.error('Error fetching data from Flask backend:', error)  
  }  
}  
  
onMounted(() => {  
  fetchItems()  
})  
</script>  
  
<style scoped>  
.page-container {  
  padding: 1rem 0;  
}  
.subtitle {  
  color: #666;  
  margin-bottom: 1.5rem;  
}  
.card {  
  background: #f9f9f9;  
  border: 1px solid #e0e0e0;  
  border-radius: 8px;  
  padding: 1.5rem;  
}  
.item-list {  
  list-style: none;  
  padding: 0;  
  margin: 0;  
}  
.item-row {  
  padding: 0.75rem 0;  
  border-bottom: 1px solid #eaeaea;  
  display: flex;  
  align-items: center;  
}  
.item-row:last-child {  
  border-bottom: none;  
}  
.badge {  
  background: #42b983;  
  color: white;  
  padding: 0.2rem 0.5rem;  
  border-radius: 4px;  
  font-size: 0.8rem;  
  margin-right: 1rem;  
  font-weight: bold;  
}  
.empty-state {  
  color: #999;  
  font-style: italic;  
  text-align: center;  
}  
</style>  
```  
  
### AboutView.vue  
  
This component demonstrates a pure static client-side page handled seamlessly by your frontend Vue Router.  
  
frontend/src/views/AboutView.vue:  
```  
<template>  
  <div class="page-container">  
    <h2>About This Application</h2>  
    <p>This is a single-page application (SPA) built using the following stack:</p>  
  
    <ul class="tech-stack">  
      <li><strong>Frontend:</strong> Vue.js 3 with Vite and Vue Router</li>  
      <li><strong>Backend:</strong> Flask with Gunicorn production server</li>  
      <li><strong>Database:</strong> SQLite with SQLAlchemy ORM</li>  
      <li><strong>Cloud:</strong> Azure App Service (Linux Web App)</li>  
    </ul>  
  
    <div class="info-box">  
      <strong>Azure Note:</strong> Client-side route changes on this page (like reloading or deep linking to <code>/about</code>) work seamlessly because your Flask backend has a configured catch-all route that hands asset handling back over to <code>index.html</code>.  
    </div>  
  </div>  
</template>  
  
<style scoped>  
.page-container {  
  padding: 1rem 0;  
  line-height: 1.6;  
}  
.tech-stack {  
  margin: 1.5rem 0;  
  padding-left: 1.5rem;  
}  
.tech-stack li {  
  margin-bottom: 0.5rem;  
}  
.info-box {  
  background: #e8f5e9;  
  border-left: 4px solid #42b983;  
  padding: 1rem;  
  border-radius: 0 8px 8px 0;  
  margin-top: 2rem;  
  color: #2e7d32;  
}  
</style>  
```  
  
### Main.js  
  
This is your standard boilerplate to mount the application.  
  
frontend/src/main.js:  
```  
import { createApp } from 'vue'  
import App from './App.vue'  
import router from './router' // <-- Import the router config  
  
const app = createApp(App)  
  
app.use(router) // <-- Tell Vue to use the router  
app.mount('#app')  
```  
  
### Build  
  
Before deploying, run the build command inside the frontend/ directory to generate the production-ready tracking assets inside dist/:  
```  
cd frontend  
npm install  
npm run build  
```  
  
This forces Vite to compile your code into plain HTML/JS/CSS and drop it directly into the top-level dist/ directory, where your Flask app is waiting to serve it.  
  
## Mock script for initial sample (p.412)  
  
### Seed script  
  
Here is a seed script you can use to initialize your SQLite database with mock data.Create a file named seed.py directly inside your backend/ folder.  
  
backend/seed.py:  
```  
import os  
import sys  
  
# Ensure Python can find app.py if running from outside the folder  
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  
  
from app import app, db, Item  
  
def seed_database():  
    print("Connecting to database and verifying tables...")  
  
    with app.app_context():  
        # Create database tables if they do not exist yet  
        db.create_all()  
  
        # Check if items already exist to avoid duplicate entries  
        if Item.query.count() == 0:  
            print("Database is empty. Injecting mock records...")  
  
            mock_items = [  
                Item(name="Flask Backend Framework"),  
                Item(name="Vue.js 3 Composition API"),  
                Item(name="SQLite Persistent Storage"),  
                Item(name="Azure Web App Linux Container"),  
                Item(name="Vite Bundler & Dev Proxy")  
            ]  
  
            db.session.bulk_save_objects(mock_items)  
            db.session.commit()  
            print("Successfully seeded 5 core project elements!")  
        else:  
            print(f"Database already contains {Item.query.count()} item(s). Skipping seed script.")  
  
if __name__ == '__main__':  
    seed_database()  
```  
  
### How to Run and Verify Locally  
  
Follow these terminal steps to seed your database and spin up your stack for a quick local integration test:Step  
  
#### 1: Run the Seed Script  
  
Navigate into your backend folder, ensure your Python environment is active, and execute the file.  
  
Run:  
```  
cd backend  
python3 -m venv .venv  
source .venv/bin/activate  
pip3 install -r requirements.txt  
python3 seed.py  
```  
  
(You will see a new database/app.db file generated automatically inside the backend/ directory).  
  
#### 2. Fire Up Flask  
  
Run:  
```  
python3 app.py  
```  
  
Your backend API server is now running locally on http://127.0.0.1:5000.  
  
#### 3. Run Vue  
  
Open a second terminal window, change to your frontend directory, and spin up Vite.  
  
Run:  
```  
cd frontend  
npm install  
npm run dev  
```  
  
Open the local browser URL provided by Vite (usually http://localhost:5173). Thanks to your configuration proxy rules, your frontend will securely request /api/items and fetch the seeded database content automatically.  
  
## Azure App Service Configuration  
  
Azure Linux App Service looks for a requirements.txt file at the root level of your deployment package to install dependencies and automatically searches for a Gunicorn entry point.  
  
 ### Root Requirements File  
  
Copy or reference the backend requirements in a top-level requirements.txt.  
  
/requirements.txt:  
```  
-r backend/requirements.txt  
```  
  
### Startup Script  
  
Create a custom startup file in your root folder to ensure your database folder is initialized and the production server points correctly to the nested Flask app folder.  
  
startup.sh:  
```  
#!/bin/bash  
# Create database directory if it doesn't exist  
mkdir -p backend/database  
  
# Run Gunicorn pointing to app inside the backend directory  
gunicorn --bind=0.0.0.0 --timeout 600 backend.app:app  
```  
  
## Deploying (line 498)  
  
To deploy your Flask and Vue.js app directly from VS Code, you must first run a local production build for your frontend, bundle your project accurately, and use the Azure Tools extension.  
  
Follow this complete step-by-step pipeline to handle your compilation and deployment directly from your editor workspace.  
  
### Step 1: Compile the Vue Frontend Locally  
  
Azure's automated Python builder (Oryx) will install Python pip dependencies, but it will not compile Node/Vue assets automatically. You must build the frontend locally so it is packaged into the deployment bundle.  
  
Open your terminal in VS Code and execute:  
```  
# 1. Navigate to frontend folder and install node modules  
cd frontend  
npm install  
  
# 2. Compile Vue components into the root '/dist' directory  
npm run build  
  
# 3. Return back to your project root workspace  
cd ..  
```  
  
Verify that a dist/ directory has appeared at your root project folder level containing index.html and an assets/ subfolder.  
  
### Step 2: Install Required Extensions  
Ensure you have the official extension bundle installed in VS Code:  
- Click the Extensions icon on the left sidebar (or press Ctrl+Shift+X / Cmd+Shift+X).  
- Search for Azure Tools (published by Microsoft) and click Install.  
- Click the newly added Azure icon on your sidebar and select Sign in to Azure... to authenticate your account.  
  
### Step 3: Configure Project Deployment Exclusions  
  
To keep your uploaded bundle small, create a .appserviceignore file in your root project directory. This prevents heavy, unnecessary local development directories from being uploaded to Azure:  
```  
# .appserviceignore  
node_modules/  
frontend/node_modules/  
frontend/src/  
backend/__pycache__/  
.venv/  
.git/  
```  
  
(Azure will compile its own virtual environment using your root requirements.txt file automatically upon code initialization).  
  
###  Step 4: Create and Provision the Web App on Azure  
  
- Click the Azure icon on the left menu pane.  
- Under the Resources section, click the + (Plus) icon and select Create App Service Web App...  
- Follow the interactive prompts at the top of your screen:  
    - Enter a unique name: e.g., flask-vue-sqlite-app  
    - Select a runtime stack: Select Python (Latest version, e.g., Python 3.12 or 3.11).  
    - Select a pricing tier: Choose Free (F1) or Basic (B1) depending on your project scope.  
- Wait a few moments while Azure provisions your resource hosting plan.  
  
### Step 5: Configure Persistent Storage & Custom Startup Settings  
  
Because SQLite requires a persistent directory path, you must toggle critical environmental variables inside Azure before launching the live server.  
  
- Find your newly created app inside the Azure Activity Tree view in your sidebar.  
- Expand your Web App name and right-click on Application Settings -> select Add New Setting...  
- Add the following key-value pairings:  
    - SCM_DO_BUILD_DURING_DEPLOYMENT = true (Forces Azure to build your Python requirements environment).  
    - WEBSITES_ENABLE_APP_SERVICE_STORAGE = true (Enables persistent state cycles so your SQLite file doesn't vanish on server reboots).  
- Go to the Azure Portal, navigate to your App Service, and under Settings -> Configuration -> Stack Settings, update your Startup Command to match your shell script:  
```  
/home/site/wwwroot/startup.sh  
```  
  
### Step 6: Trigger the VS Code Deployment  
  
- In your VS Code file explorer, right-click on an empty space inside your root project folder (containing backend/, dist/, requirements.txt, and startup.sh).  
- Select Deploy to Web App...  
- Select your subscription and choose the targeted Web App name you created in Step 4.  
- A prompt will ask: "Are you sure you want to deploy... this will overwrite previous configurations?" Click Deploy.  
Monitor the Output Window in your bottom tray. Azure will automatically unpack your zip package, construct a Python virtual container layer, run your root requirements.txt, launch startup.sh, and serve your app securely on the web.  
  