<template>
  <div class="asset-tree">
    <div class="tree-header">
      <span>资产树</span>
      <button class="refresh-btn" @click="$emit('refresh')" title="刷新文件列表">🔄</button>
    </div>
    <div class="tree-body">
      <!-- 项目过程数据 -->
      <div class="tree-group">
        <div class="group-header" @click="toggleGroup('project')">
          <span class="arrow">{{ groups.project.open ? '▾' : '▸' }}</span>
          📁 项目过程
        </div>
        <div v-show="groups.project.open" class="group-items">
          <div
            v-for="item in projectFiles"
            :key="item.path"
            class="tree-item"
            :class="{ active: activeFile === item.path }"
            @click="selectFile(item)"
          >
            <span class="file-icon">{{ item.type === 'directory' ? '📁' : '📄' }}</span>
            <span>{{ item.name }}</span>
          </div>
        </div>
      </div>

      <!-- Skill 资产 -->
      <div class="tree-group">
        <div class="group-header" @click="toggleGroup('skills')">
          <span class="arrow">{{ groups.skills.open ? '▾' : '▸' }}</span>
          📁 Skill资产
        </div>
        <div v-show="groups.skills.open" class="group-items">
          <div v-for="skill in skillList" :key="skill.name">
            <div class="tree-item" @click="toggleSkill(skill.name)">
              <span class="arrow">{{ skill.open ? '▾' : '▸' }}</span>
              {{ skill.label }}
            </div>
            <div
              v-show="skill.open"
              v-for="file in skill.files"
              :key="file"
              class="tree-item nested"
              :class="{ active: activeFile === 'skills/' + skill.name + '/' + file }"
              @click="selectSkillFile(skill.name, file)"
            >
              <span class="file-icon">📄</span>
              <span>{{ file }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 阶段模板 -->
      <div class="tree-group">
        <div class="group-header" @click="toggleGroup('templates')">
          <span class="arrow">{{ groups.templates.open ? '▾' : '▸' }}</span>
          📁 阶段模板
        </div>
        <div v-show="groups.templates.open" class="group-items">
          <div
            v-for="tpl in templateList"
            :key="tpl"
            class="tree-item"
            :class="{ active: activeFile === 'templates/' + tpl }"
            @click="selectTemplate(tpl)"
          >
            <span class="file-icon">📄</span>
            <span>{{ tpl }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { api } from '../api/index.js'

const props = defineProps({
  fileTree: { type: Array, default: () => [] },
  activeFile: { type: String, default: null }
})

const emit = defineEmits(['refresh', 'select-file', 'select-skill-file', 'select-template'])

const groups = reactive({
  project: { open: true },
  skills: { open: true },
  templates: { open: true }
})

const skillList = ref([
  { name: 'brainstorming', label: '① brainstorming', open: false, files: [] },
  { name: 'writing-plans', label: '② plan', open: false, files: [] },
  { name: 'subagent-driven-development', label: '③ subagent-dev', open: false, files: [] },
  { name: 'finishing-a-development-branch', label: '④ finishing', open: false, files: [] },
])

const templateList = ref([])

const projectFiles = ref([])

function toggleGroup(name) { groups[name].open = !groups[name].open }
function toggleSkill(name) {
  const s = skillList.value.find(x => x.name === name)
  if (s) s.open = !s.open
}
function selectFile(item) { emit('select-file', item) }
function selectSkillFile(stage, file) { emit('select-skill-file', stage, file) }
function selectTemplate(type) { emit('select-template', type) }

onMounted(async () => {
  try {
    const data = await api.getSkills()
    for (const skill of data.skills) {
      const s = skillList.value.find(x => x.name === skill.name)
      if (s) s.files = skill.files
    }
  } catch (e) { /* ignore */ }
  try {
    const data = await api.getTemplates()
    templateList.value = data.templates || []
  } catch (e) { /* ignore */ }
})
</script>

<style scoped>
.asset-tree { height: 100%; display: flex; flex-direction: column; background: #181825; }
.tree-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 12px; border-bottom: 1px solid #313244; font-weight: 600; font-size: 13px;
}
.refresh-btn { background: none; border: none; cursor: pointer; font-size: 14px; color: #cba6f7; }
.tree-body { flex: 1; overflow-y: auto; padding: 4px 0; }
.tree-group { margin-bottom: 2px; }
.group-header {
  padding: 4px 12px; cursor: pointer; font-size: 12px; font-weight: 600;
  color: #a6adc8; user-select: none;
}
.group-header:hover { background: #313244; }
.arrow { display: inline-block; width: 14px; font-size: 10px; }
.group-items { padding-left: 4px; }
.tree-item {
  padding: 3px 12px 3px 24px; cursor: pointer; font-size: 13px;
  display: flex; align-items: center; gap: 4px; user-select: none;
}
.tree-item:hover { background: #313244; }
.tree-item.active { background: #45475a; color: #cba6f7; }
.tree-item.nested { padding-left: 40px; }
.file-icon { font-size: 11px; }
</style>
