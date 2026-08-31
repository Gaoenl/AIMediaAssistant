<template>
  <el-container>
    <el-header style="display: flex; justify-content: space-between; align-items: center">
      <span>AIMA · 热点选题池</span>
      <div>
        <el-button @click="router.push('/tasks')">生成任务</el-button>
        <el-button @click="logout">退出</el-button>
      </div>
    </el-header>
    <el-main>
      <el-card>
        <el-form inline>
          <el-form-item label="来源">
            <el-select v-model="query.source" clearable placeholder="全部来源" style="width: 160px" @change="load">
              <el-option label="知乎热榜" value="zhihu_hot" />
              <el-option label="B站热门" value="bilibili_hot" />
              <el-option label="36氪" value="rss_36kr" />
              <el-option label="虎嗅" value="rss_huxiu" />
              <el-option label="节日日历" value="festival" />
              <el-option label="抖音热榜" value="douyin_hot" />
              <el-option label="微博热搜" value="weibo_hot" />
              <el-option label="百度热搜" value="baidu_hot" />
              <el-option label="头条热榜" value="toutiao_hot" />
            </el-select>
          </el-form-item>
          <el-form-item label="最低热度">
            <el-input-number v-model="query.minScore" :min="0" :max="100" placeholder="不限" @change="load" />
          </el-form-item>
          <el-button type="primary" @click="load">刷新</el-button>
        </el-form>

        <el-table :data="rows" v-loading="loading" stripe>
          <el-table-column prop="hotScore" label="热度" width="80" sortable />
          <el-table-column prop="trend" label="趋势" width="80">
            <template #default="{ row }">
              <el-tag v-if="row.trend === 'NEW'" type="success" size="small">新</el-tag>
              <el-tag v-else-if="row.trend === 'RISING'" type="danger" size="small">↑</el-tag>
              <el-tag v-else-if="row.trend === 'FALLING'" type="info" size="small">↓</el-tag>
              <span v-else>—</span>
            </template>
          </el-table-column>
          <el-table-column label="标题" min-width="320">
            <template #default="{ row }">
              <a v-if="row.url" :href="row.url" target="_blank" rel="noopener">{{ row.title }}</a>
              <span v-else>{{ row.title }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="source" label="来源" width="130" />
          <el-table-column prop="collectedAt" label="采集时间" width="180">
            <template #default="{ row }">{{ formatTime(row.collectedAt) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="130" fixed="right">
            <template #default="{ row }">
              <el-button size="small" type="primary" @click="openGenerate(row)">生成文章</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-pagination
          style="margin-top: 12px"
          layout="prev, pager, next, total"
          :total="total"
          :page-size="query.size"
          v-model:current-page="query.page"
          @current-change="load"
        />
      </el-card>

      <el-dialog v-model="genVisible" title="生成文章" width="440px">
        <el-form label-width="80px">
          <el-form-item label="主题">
            <el-input :model-value="current?.title" disabled />
          </el-form-item>
          <el-form-item label="风格">
            <el-select v-model="stylePrompt" style="width: 100%">
              <el-option label="小红书口语化" value="小红书口语化,亲切活泼" />
              <el-option label="知乎深度" value="知乎风格,理性分析,结构清晰" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="genVisible = false">取消</el-button>
          <el-button type="primary" :loading="submitting" @click="submit">提交生成</el-button>
        </template>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createArticleFromTopic, getTopics } from '../api/topic'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const rows = ref([])
const total = ref(0)
const loading = ref(false)
const query = reactive({ source: '', minScore: null, page: 1, size: 20 })

const genVisible = ref(false)
const submitting = ref(false)
const current = ref(null)
const stylePrompt = ref('小红书口语化,亲切活泼')

async function load() {
  loading.value = true
  try {
    const data = await getTopics(query)
    rows.value = data.records || []
    total.value = data.total || 0
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    loading.value = false
  }
}

function formatTime(v) {
  return v ? new Date(v).toLocaleString() : ''
}

function openGenerate(row) {
  current.value = row
  genVisible.value = true
}

async function submit() {
  submitting.value = true
  try {
    const task = await createArticleFromTopic(current.value.id, stylePrompt.value)
    ElMessage.success(`已提交生成,任务 ${task.id}`)
    genVisible.value = false
    router.push('/tasks')
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    submitting.value = false
  }
}

function logout() {
  auth.logout()
  router.push('/login')
}

onMounted(load)
</script>
