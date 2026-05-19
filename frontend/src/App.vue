<template>
  <NavBar />
  <div class="app-body">
    <div class="stage-area">
      <StageProgressBar :stages="stages" />
    </div>
    <div class="content">
      <div class="panel-left">
        <div class="panel-placeholder">资产树</div>
      </div>
      <div class="panel-center">
        <div class="panel-placeholder">查看/编辑器</div>
      </div>
      <div class="panel-right">
        <div class="panel-placeholder">终端</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import NavBar from './components/NavBar.vue'
import StageProgressBar from './components/StageProgressBar.vue'
import { useStages } from './composables/useStages.js'

const { stages, fetchStages } = useStages()
onMounted(() => { fetchStages() })
</script>

<style>
.app-body {
  height: calc(100% - 48px);
  display: flex;
  flex-direction: column;
}
.stage-area { height: 48px; border-bottom: 1px solid #313244; }
.content {
  flex: 1;
  display: flex;
  overflow: hidden;
}
.panel-left { width: 260px; border-right: 1px solid #313244; }
.panel-center { flex: 1; border-right: 1px solid #313244; }
.panel-right { width: 450px; }
.panel-placeholder {
  padding: 16px;
  color: #6c7086;
}
</style>
