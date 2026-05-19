<template>
  <div class="progress-bar">
    <div
      v-for="stage in stages"
      :key="stage.id"
      class="stage-step"
      :class="stage.status"
    >
      <div class="step-indicator">
        <span v-if="stage.status === 'completed'" class="check">✓</span>
        <span v-else-if="stage.status === 'active'" class="active-dot"></span>
        <span v-else class="lock">🔒</span>
      </div>
      <div class="step-label">
        <div class="step-name">{{ stageNames[stage.name] || stage.name }}</div>
        <div class="step-status-text">{{ statusText(stage.status) }}</div>
      </div>
      <div v-if="!isLast(stage)" class="step-connector" :class="stage.status"></div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  stages: { type: Array, default: () => [] }
})

const stageNames = {
  'brainstorming': '① Brainstorming',
  'plan': '② Plan',
  'implement': '③ Implement',
  'complete': '④ Complete'
}

function statusText(status) {
  return status === 'completed' ? '已完成' : status === 'active' ? '进行中' : '未解锁'
}

function isLast(stage) {
  return stage.display_order === props.stages.length
}
</script>

<style scoped>
.progress-bar {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 24px;
  gap: 0;
}
.stage-step {
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}
.step-indicator {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}
.completed .step-indicator { background: #a6e3a1; color: #1e1e2e; }
.active .step-indicator { background: #cba6f7; color: #1e1e2e; }
.locked .step-indicator { background: #45475a; color: #6c7086; }

.step-label { font-size: 12px; }
.step-name { font-weight: 600; }
.completed .step-name { color: #a6e3a1; }
.active .step-name { color: #cba6f7; }
.locked .step-name { color: #585b70; }
.step-status-text { font-size: 10px; color: #6c7086; }

.step-connector {
  width: 40px;
  height: 2px;
  margin: 0 8px;
  background: #45475a;
}
.step-connector.completed { background: #a6e3a1; }
.check { font-weight: bold; }
.active-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: #1e1e2e;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
</style>
