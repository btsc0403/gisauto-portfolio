<template>
  <div class="app-container">
    <AppHeader />
    <main class="app-main">
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import AppHeader from "./components/AppHeader.vue"
import AppFooter from "./components/AppFooter.vue"
</script>

<style scoped>
.app-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.app-main {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}
</style>
