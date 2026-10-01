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
</style>

