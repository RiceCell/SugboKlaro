import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.ts'
import './style.css'
import { generateProjectOverview } from './services/aiOverview.ts'

const app = createApp(App)
generateProjectOverview("PROC-002");

app.use(router)
app.mount('#app')