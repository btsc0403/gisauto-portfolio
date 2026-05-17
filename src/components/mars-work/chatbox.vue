<template>
  <div class="chatbox">
    <div class="chat-content">
      <p
        v-for="(msg, index) in chatMessages"
        :key="index"
        :class="typeof msg === 'string' && msg.startsWith('用户') ? 'user-message' : ''"
      >
        {{ msg }}
      </p>
    </div>
    <div class="input-container">
      <textarea v-model="userInput" placeholder="请输入您的问题..."></textarea>
      <button @click="sendMessage">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="feather feather-send"
        >
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { callClaudeAPI } from "../../config/api"

const userInput = ref("")
const chatMessages = ref<string[]>([])

const sendMessage = async () => {
  if (userInput.value.trim() === "") {
    return
  }

  chatMessages.value.push(`用户 ${userInput.value}`)

  try {
    // 使用Claude API
    const content = await callClaudeAPI([
      { 
        role: "user", 
        content: userInput.value 
      }
    ])
    
    chatMessages.value.push(`AI ${content}`)

  } catch (error) {
    console.error("Error:", error)
    chatMessages.value.push("AI 对不起，出错了。")
  } finally {
    userInput.value = ""
  }
}
</script>

<style scoped>
.chatbox {
  display: flex;
  flex-direction: column
}

.chat-content {
  height: 600px;
  overflow-y: auto;
  margin-bottom: 10px;
  line-height: 1.6;
}

.chat-content p {
  padding: 10px;
  margin: 5px 0;
  border-radius: 8px;
  background-color: #f0f8ff;
  border: 1px solid #add8e6;
}

.chat-content p.user-message {
  background-color: #e0ffe0;
  border: 1px solid #90ee90;
}

.input-container {
  display: flex;
  align-items: center;
}

textarea {
  flex: 1;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
  resize: none;
}

button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}

button svg {
  vertical-align: middle
}

button:hover {
  background-color: #0056b3;
}
</style>
