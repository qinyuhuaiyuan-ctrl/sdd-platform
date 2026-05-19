// frontend/src/composables/useStages.js
import { ref, reactive } from 'vue'
import { api } from '../api/index.js'

export function useStages() {
  const stages = ref([])
  const currentStage = ref('')
  const error = ref(null)

  async function fetchStages() {
    try {
      const data = await api.getStages()
      stages.value = data.stages
      currentStage.value = data.current_stage
    } catch (e) {
      error.value = e.message
    }
  }

  async function advanceStage() {
    try {
      const result = await api.advanceStage()
      await fetchStages()
      return result
    } catch (e) {
      error.value = e.message
      throw e
    }
  }

  return { stages, currentStage, error, fetchStages, advanceStage }
}
