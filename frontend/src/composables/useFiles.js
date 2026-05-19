// frontend/src/composables/useFiles.js
import { ref } from 'vue'
import { api } from '../api/index.js'

export function useFiles() {
  const fileTree = ref([])
  const currentFile = ref(null)
  const fileContent = ref('')
  const loading = ref(false)

  async function refreshFileTree() {
    try {
      const data = await api.refreshFiles()
      fileTree.value = data.file_tree || []
    } catch (e) {
      console.error('Failed to refresh files:', e)
    }
  }

  async function openFile(path) {
    loading.value = true
    try {
      const data = await api.getFile(path)
      currentFile.value = path
      fileContent.value = data.content
    } catch (e) {
      console.error('Failed to open file:', e)
    } finally {
      loading.value = false
    }
  }

  async function saveFile(path, content) {
    await api.saveFile(path, content)
  }

  return { fileTree, currentFile, fileContent, loading, refreshFileTree, openFile, saveFile }
}
