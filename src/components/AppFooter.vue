<template>
  <footer class="app-footer">
    <div class="footer-left">
      <span class="footer-brand">Heritage Explorer</span>
      <span class="footer-copyright">&copy; 2026 Heritage GIS Platform. Data provided by Heritage Architecture Consortium.</span>
    </div>
    <div class="footer-right">
      <a href="#" class="footer-link">Attribution</a>
      <a href="#" class="footer-link">Privacy Policy</a>
      <a href="#" class="footer-link">API Docs</a>
      <a href="#" class="footer-link">Contact</a>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 24px;
  background: var(--glass-highlight), var(--footer-bg);
  backdrop-filter: blur(var(--footer-blur)) saturate(1.4);
  -webkit-backdrop-filter: blur(var(--footer-blur)) saturate(1.4);
  flex-shrink: 0;
  z-index: 100;
  transition: background-color 0.4s ease;
}

.footer-brand { transition: color 0.4s; }
.footer-copyright { transition: color 0.4s; }
.footer-link { transition: color 0.3s; }

.footer-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.footer-brand {
  font-family: "Georgia", "Times New Roman", serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--footer-brand);
}

.footer-copyright {
  font-size: 11px;
  color: var(--footer-text);
  line-height: 1.4;
}

.footer-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.footer-link {
  font-size: 12px;
  color: var(--footer-text);
  text-decoration: none;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: color 0.2s;
}

.footer-link:hover {
  color: var(--footer-brand);
}
</style>
