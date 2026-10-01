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
