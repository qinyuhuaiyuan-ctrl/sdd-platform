<template>
  <div class="stage-gate">
    <button
      v-if="currentStage !== 'complete'"
      class="advance-btn"
      :disabled="loading"
      @click="handleAdvance"
    >
      {{ loading ? '校验中...' : `进入下一阶段 →` }}
    </button>
    <span v-else class="complete-badge">✓ 流程已完成</span>
    <div v-if="error" class="gate-error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  currentStage: { type: String, default: '' }
})

const emit = defineEmits(['advance'])
const loading = ref(false)
const error = ref(null)

async function handleAdvance() {
  loading.value = true
  error.value = null
  try {
    await emit('advance')
  } catch (e) {
    error.value = e.message || '阶段推进失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.stage-gate { display: flex; align-items: center; gap: 12px; }
.advance-btn {
  background: #cba6f7; color: #1e1e2e; border: none; padding: 6px 16px;
  border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer;
}
.advance-btn:hover { background: #b4befe; }
.advance-btn:disabled { opacity: 0.5; cursor: default; }
.complete-badge { color: #a6e3a1; font-weight: 600; font-size: 13px; }
.gate-error { color: #f38ba8; font-size: 12px; }
</style>
