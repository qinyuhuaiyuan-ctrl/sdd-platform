<!-- frontend/src/App.vue 完整版 -->
<template>
  <NavBar />
  <div class="app-body">
    <div class="stage-area">
      <StageProgressBar :stages="stages" />
      <StageGate
        :currentStage="currentStage"
        @advance="onAdvanceStage"
      />
    </div>
    <div class="content">
      <div class="panel-left">
        <AssetTree
          :fileTree="fileTree"
          :activeFile="currentFile"
          @refresh="refreshFileTree"
          @select-file="onSelectFile"
          @select-skill-file="onSelectSkillFile"
          @select-template="onSelectTemplate"
        />
      </div>
      <div class="panel-center">
        <ViewerEditor
          :filePath="currentFile"
          :content="fileContent"
          :readonly="isReadonly"
          @save="onSaveFile"
        />
      </div>
      <div class="panel-right">
        <TerminalPanel />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import NavBar from './components/NavBar.vue'
import StageProgressBar from './components/StageProgressBar.vue'
import AssetTree from './components/AssetTree.vue'
import ViewerEditor from './components/ViewerEditor.vue'
import TerminalPanel from './components/TerminalPanel.vue'
import StageGate from './components/StageGate.vue'
import { useStages } from './composables/useStages.js'
import { useFiles } from './composables/useFiles.js'
import { api } from './api/index.js'

const { stages, currentStage, fetchStages, advanceStage } = useStages()
const { fileTree, currentFile, fileContent, refreshFileTree, openFile, saveFile } = useFiles()

const isReadonly = computed(() => {
  if (!currentFile.value) return false
  const stageOrder = { brainstorming: 0, plan: 1, implement: 2, complete: 3 }
  const current = stageOrder[currentStage.value] || 0
  return current >= 2 && (currentFile.value.includes('.sdd/spec.md') || currentFile.value.includes('.sdd/plan.md'))
})

async function onSelectFile(item) {
  currentFile.value = item.path || item.name
  await openFile(item.path || item.name)
}

async function onSelectSkillFile(stage, file) {
  const path = `skills/${stage}/${file}`
  currentFile.value = path
  try {
    const data = await api.getSkillFile(stage, file)
    fileContent.value = data.content
  } catch(e) { console.error(e) }
}

async function onSelectTemplate(type) {
  currentFile.value = `templates/${type}`
  try {
    const data = await api.getTemplate(type)
    fileContent.value = data.content
  } catch(e) { console.error(e) }
}

async function onSaveFile(content) {
  if (!currentFile.value) return
  if (currentFile.value.startsWith('skills/')) {
    const parts = currentFile.value.split('/')
    await api.saveSkillFile(parts[1], parts.slice(2).join('/'), content)
  } else if (currentFile.value.startsWith('templates/')) {
    await api.saveTemplate(currentFile.value.replace('templates/', ''), content)
  } else {
    await saveFile(currentFile.value, content)
  }
}

async function onAdvanceStage() {
  await advanceStage()
}

onMounted(async () => {
  await fetchStages()
  await refreshFileTree()
})
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, #app { height: 100%; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
body { background: #1e1e2e; color: #cdd6f4; }
.app-body { height: calc(100% - 48px); display: flex; flex-direction: column; }
.stage-area {
  height: 48px;
  border-bottom: 1px solid #313244;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-right: 16px;
}
.content { flex: 1; display: flex; overflow: hidden; }
.panel-left { width: 260px; border-right: 1px solid #313244; }
.panel-center { flex: 1; border-right: 1px solid #313244; }
.panel-right { width: 450px; }
</style>
