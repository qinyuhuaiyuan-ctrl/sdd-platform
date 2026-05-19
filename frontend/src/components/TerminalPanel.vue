<template>
  <div class="terminal-panel">
    <div class="terminal-header">
      <span>终端</span>
      <span class="connection-status" :class="{ connected }">
        {{ connected ? '● 已连接' : '○ 未连接' }}
      </span>
    </div>
    <div ref="terminalContainer" class="terminal-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useTerminal } from '../composables/useTerminal.js'

const { terminal, connected, init, dispose } = useTerminal()
const terminalContainer = ref(null)

onMounted(() => {
  if (terminalContainer.value) {
    init(terminalContainer.value)
  }
})

onBeforeUnmount(() => {
  dispose()
})
</script>

<style scoped>
.terminal-panel { height: 100%; display: flex; flex-direction: column; background: #1e1e2e; }
.terminal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 12px; border-bottom: 1px solid #313244; font-size: 12px; font-weight: 600;
}
.connection-status { font-size: 11px; color: #6c7086; }
.connection-status.connected { color: #a6e3a1; }
.terminal-container { flex: 1; padding: 4px; }
</style>
