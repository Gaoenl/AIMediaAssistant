<template>
  <el-container>
    <el-header style="display: flex; justify-content: space-between; align-items: center">
      <span>AIMA · 内容生成(M1)</span>
      <el-button @click="logout">退出</el-button>
    </el-header>
    <el-main>
      <el-card>
        <el-form inline>
          <el-form-item label="主题">
            <el-input v-model="form.topic" style="width: 260px" />
          </el-form-item>
          <el-form-item label="风格">
            <el-select v-model="form.stylePrompt" style="width: 200px">
              <el-option label="小红书口语化" value="小红书口语化,亲切活泼" />
              <el-option label="知乎深度" value="知乎风格,理性分析,结构清晰" />
            </el-select>
          </el-form-item>
          <el-button type="primary" :loading="submitting" @click="onSubmit">生成</el-button>
        </el-form>
      </el-card>

      <el-card v-if="task" style="margin-top: 16px">
        <template #header>
          任务状态:{{ task.status }}
          <el-tag v-if="task.qualityScore" style="margin-left: 8px">质检 {{ task.qualityScore }}</el-tag>
        </template>
        <el-alert v-if="task.status === 'FAILED'" type="error" :title="task.error || '生成失败'" />
        <template v-if="task.title">
          <h3>{{ task.title }}</h3>
          <pre style="white-space: pre-wrap">{{ task.content }}</pre>
        </template>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
import { reactive, ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { submitGeneration, getTask } from '../api/task'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const form = reactive({ topic: 'AI 智能媒体', stylePrompt: '小红书口语化,亲切活泼' })
const submitting = ref(false)
const task = ref(null)
let timer = null

async function onSubmit() {
  if (!form.topic) return ElMessage.warning('请输入主题')
  submitting.value = true
  try {
    task.value = await submitGeneration(form.topic, form.stylePrompt)
    poll(task.value.id)
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    submitting.value = false
  }
}

async function poll(id) {
  clearInterval(timer)
  timer = setInterval(async () => {
    try {
      task.value = await getTask(id)
      if (['SUCCESS', 'FAILED'].includes(task.value.status)) clearInterval(timer)
    } catch (e) {
      clearInterval(timer)
      ElMessage.error(e.message)
    }
  }, 2000)
}

function logout() {
  clearInterval(timer)
  auth.logout()
  router.push('/login')
}

onUnmounted(() => clearInterval(timer))
</script>
