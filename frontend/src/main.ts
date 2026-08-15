import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'
import { generateProjectOverview } from './services/aiOverview'

const app = createApp(App)
generateProjectOverview("12");

app.use(router)
app.mount('#app')