<template>
  <el-card style="max-width: 380px; margin: 120px auto">
    <template #header>AIMA 控制台</template>
    <el-form :model="form" label-width="70px" @submit.prevent="onSubmit">
      <el-form-item label="用户名">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" type="password" show-password />
      </el-form-item>
      <el-button type="primary" :loading="loading" @click="onSubmit">登录</el-button>
    </el-form>
  </el-card>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const form = reactive({ username: 'admin', password: '' })

async function onSubmit() {
  loading.value = true
  try {
    await auth.login(form.username, form.password)
    router.push('/tasks')
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    loading.value = false
  }
}
</script>
