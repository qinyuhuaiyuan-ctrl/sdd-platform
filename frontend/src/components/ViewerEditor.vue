<!-- frontend/src/components/ViewerEditor.vue -->
<template>
  <div class="viewer-editor">
    <div class="editor-header">
      <span class="file-path">{{ filePath || '未打开文件' }}</span>
      <div v-if="filePath && !readonly" class="header-actions">
        <button class="action-btn" @click="save" :disabled="!dirty">💾 保存</button>
      </div>
    </div>
    <div class="editor-body">
      <div v-if="!filePath" class="empty-state">
        从左侧资产树选择文件查看或编辑
      </div>
      <div v-else-if="isMarkdown" ref="editorContainer" class="cm-editor-container"></div>
      <pre v-else class="plain-view"><code>{{ content }}</code></pre>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { EditorView, basicSetup } from 'codemirror'
import { markdown } from '@codemirror/lang-markdown'
import { oneDark } from '@codemirror/theme-one-dark'

const props = defineProps({
  filePath: { type: String, default: null },
  content: { type: String, default: '' },
  readonly: { type: Boolean, default: false },
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['save'])

const dirty = ref(false)
const isMarkdown = ref(true)
let editorView = null
const editorContainer = ref(null)

function initEditor() {
  if (!editorContainer.value) return
  if (editorView) editorView.destroy()

  editorView = new EditorView({
    doc: props.content,
    extensions: [
      basicSetup,
      markdown(),
      oneDark,
      EditorView.updateListener.of(update => {
        if (update.docChanged) dirty.value = true
      }),
      EditorView.editable.of(!props.readonly)
    ],
    parent: editorContainer.value
  })
}

function updateContent(newContent) {
  if (editorView && editorView.state.doc.toString() !== newContent) {
    editorView.dispatch({
      changes: { from: 0, to: editorView.state.doc.length, insert: newContent }
    })
    dirty.value = false
  }
}

watch(() => props.filePath, (path) => {
  if (!path) return
  isMarkdown.value = path.endsWith('.md') || path.endsWith('.SKILL.md')
  dirty.value = false
  nextTick(() => {
    if (isMarkdown.value) initEditor()
  })
})

watch(() => props.content, updateContent)

watch(() => isMarkdown.value, () => {
  if (isMarkdown.value) initEditor()
})

function save() {
  if (!editorView) return
  emit('save', editorView.state.doc.toString())
  dirty.value = false
}

onMounted(() => {
  if (isMarkdown.value && props.filePath) initEditor()
})

onBeforeUnmount(() => {
  if (editorView) editorView.destroy()
})
</script>

<style scoped>
.viewer-editor { height: 100%; display: flex; flex-direction: column; background: #1e1e2e; }
.editor-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 12px; border-bottom: 1px solid #313244; font-size: 12px;
}
.file-path { color: #a6adc8; font-family: monospace; }
.header-actions { display: flex; gap: 6px; }
.action-btn {
  background: #45475a; border: none; color: #cdd6f4; padding: 4px 10px;
  border-radius: 4px; cursor: pointer; font-size: 11px;
}
.action-btn:hover { background: #585b70; }
.action-btn:disabled { opacity: 0.4; cursor: default; }
.editor-body { flex: 1; overflow: auto; }
.empty-state {
  display: flex; align-items: center; justify-content: center;
  height: 100%; color: #6c7086; font-size: 14px;
}
.cm-editor-container { height: 100%; }
.plain-view { padding: 16px; font-family: monospace; font-size: 13px; white-space: pre-wrap; }
</style>
