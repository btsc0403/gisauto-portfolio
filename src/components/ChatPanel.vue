<template>
  <div class="gpt4-chatbox">
    <div class="component-header">
      <div class="arrow"></div>
      <span>问答</span>
    </div>
    <div class="chat-content" ref="chatContentRef">
      <!-- Messages -->
      <template v-for="(msg, index) in chatStore.chatMessages" :key="index">
        <div
          :class="[
            'bubble-row',
            isUserMsg(msg) ? 'user' : 'bot',
            { 'msg-new': isNewBotMsg(index) }
          ]"
        >
          <div class="bubble-avatar">
            <svg v-if="!isUserMsg(msg)" class="avatar-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="4" width="18" height="14" rx="3" />
              <circle cx="9" cy="11" r="1.5" fill="currentColor" stroke="none" />
              <circle cx="15" cy="11" r="1.5" fill="currentColor" stroke="none" />
              <path d="M4 4V3a1 1 0 0 1 1-1h2M18 4V3a1 1 0 0 0-1-1h-2" />
              <path d="M9 18v2M15 18v2" />
            </svg>
            <svg v-else class="avatar-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="8" r="4" />
              <path d="M6 21v-1a6 6 0 0 1 12 0v1" />
            </svg>
          </div>
          <div class="chat-bubble" v-html="stripPrefix(msg)"></div>
        </div>
      </template>

      <!-- Thinking dots -->
      <div v-if="chatStore.isSearching" class="bubble-row bot thinking-row">
        <div class="bubble-avatar">
          <svg class="avatar-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="4" width="18" height="14" rx="3" />
            <circle cx="9" cy="11" r="1.5" fill="currentColor" stroke="none" />
            <circle cx="15" cy="11" r="1.5" fill="currentColor" stroke="none" />
            <path d="M4 4V3a1 1 0 0 1 1-1h2M18 4V3a1 1 0 0 0-1-1h-2" />
            <path d="M9 18v2M15 18v2" />
          </svg>
        </div>
        <div class="thinking-bubble">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>

      <!-- Search results (building or component, staggered entrance) -->
      <div
        v-if="showResults && chatStore.themeSearchResults?.length"
        :class="['theme-results results-enter', { 'component-results': resultType === 'component' }]"
      >
        <div class="theme-results-header">
          <span>{{ resultType === 'component' ? '相关构件结果' : '相关建筑结果' }}</span>
        </div>
        <div class="theme-results-list">
          <div
            v-for="(item, idx) in chatStore.themeSearchResults"
            :key="idx"
            class="result-item result-stagger"
            :style="{ '--i': idx }"
            @click="handleResultClick(item)"
          >
            <span class="result-number">{{ idx + 1 }}</span>
            <div class="result-content">
              <span class="result-name">
                {{ resultType === 'component' ? (item.component || item.name) : item.name }}
              </span>
              <div class="result-details">
                <span v-if="item.building && resultType === 'component'" class="result-structure">{{ item.building }}</span>
                <span v-if="item.city" class="result-city">{{ item.city }}</span>
                <span v-if="item.structure && resultType !== 'component'" class="result-structure">{{ item.structure }}</span>
                <span v-if="item.year" class="result-year">{{ item.year }}</span>
                <span v-for="feat in (item.features || []).slice(0, 3)" :key="feat" class="result-feature">{{ feat }}</span>
                <span v-if="item.score != null" class="result-score">{{ (item.score * 100).toFixed(1) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onUnmounted } from "vue"
import { useChatStore } from "../stores/chatStore"

const emit = defineEmits<{
  jumpToBuilding: [coordinate: { lat: number; lng: number }]
}>()

const chatStore = useChatStore()
const chatContentRef = ref<HTMLElement | null>(null)

/* --- Animation state --- */
const showResults = ref(false)
const msgCountBeforeSearch = ref(0)
let expandTimer: ReturnType<typeof setTimeout> | null = null
let scrollTimer: ReturnType<typeof setInterval> | null = null

const resultType = computed(() => {
  const first = chatStore.themeSearchResults?.[0]
  return first?._type || "building"
})

function isUserMsg(msg: string) {
  return msg.startsWith("User:")
}

function stripPrefix(msg: string) {
  if (msg.startsWith("User: ")) return msg.slice(6)
  if (msg.startsWith("User:")) return msg.slice(5)
  if (msg.startsWith("BOT: ")) return msg.slice(5)
  if (msg.startsWith("BOT:")) return msg.slice(4)
  return msg
}

/** New bot messages (from current search round) get the expand animation */
function isNewBotMsg(index: number) {
  return index >= msgCountBeforeSearch.value && !isUserMsg(chatStore.chatMessages[index])
}

function handleResultClick(item: any) {
  if (item.coordinate) emit("jumpToBuilding", item.coordinate)
}

function scrollToBottom() {
  if (chatContentRef.value) {
    chatContentRef.value.scrollTop = chatContentRef.value.scrollHeight
  }
}

function clearTimers() {
  if (expandTimer) { clearTimeout(expandTimer); expandTimer = null }
  if (scrollTimer) { clearInterval(scrollTimer); scrollTimer = null }
}

/* --- Phase transitions --- */
watch(() => chatStore.isSearching, (searching) => {
  if (searching) {
    // New search started — record baseline and hide old results
    msgCountBeforeSearch.value = chatStore.chatMessages.length
    showResults.value = false
    clearTimers()
    nextTick(scrollToBottom)
  } else {
    // Search done — auto-scroll during expand, then reveal results
    scrollTimer = setInterval(scrollToBottom, 80)

    expandTimer = setTimeout(() => {
      // Remove expand animation constraints (overflow:hidden / max-height)
      msgCountBeforeSearch.value = chatStore.chatMessages.length

      if (chatStore.themeSearchResults?.length) {
        showResults.value = true
      }

      // Keep scrolling during result stagger, then stop
      setTimeout(() => {
        if (scrollTimer) { clearInterval(scrollTimer); scrollTimer = null }
      }, 900)
    }, 700)
  }
})

// Scroll on new messages
watch(() => chatStore.chatMessages.length, async () => {
  await nextTick()
  scrollToBottom()
})

onUnmounted(clearTimers)
</script>

<style scoped>
.gpt4-chatbox {
  width: 325px;
  flex: 0 0 325px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--glass-highlight), var(--chat-bg);
  backdrop-filter: blur(var(--glass-blur)) saturate(1.4);
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.4);
  padding: 15px 12px 12px 12px;
  border-radius: var(--glass-radius);
  box-shadow: var(--glass-shadow);
  border: 1px solid var(--chat-border);
  box-sizing: border-box;
  transition: box-shadow 0.4s, border-color 0.4s;
}
.gpt4-chatbox:hover {
  box-shadow: var(--glass-hover-shadow);
  border-color: var(--glass-hover-border);
}

/* --- Header --- */
.component-header { display: flex; align-items: center; margin-bottom: 10px; z-index: 999; opacity: 0.75; }
.arrow { width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 8px solid var(--text-primary); margin-right: 5px; transition: border-color 0.4s; }
.component-header span { font-weight: bold; font-size: 16px; font-family: "DengXian", "等线", sans-serif; color: var(--text-primary); transition: color 0.4s; }

/* --- Chat Content Area --- */
.chat-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  margin-bottom: 0;
  min-height: 0;
  padding: 4px 6px 4px 0;
}
.chat-content::-webkit-scrollbar { width: 5px; }
.chat-content::-webkit-scrollbar-track { background: transparent; }
.chat-content::-webkit-scrollbar-thumb { background-color: var(--scrollbar-thumb); border-radius: 4px; }
.chat-content::-webkit-scrollbar-button { display: none; }

/* ============================================
   Bubble Row — default entrance
   ============================================ */
.bubble-row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 14px;
  animation: bubbleIn 0.35s cubic-bezier(0.22, 0.61, 0.36, 1) both;
}
.bubble-row.user { flex-direction: row-reverse; }

@keyframes bubbleIn {
  from { opacity: 0; transform: translateY(10px) scale(0.97); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ============================================
   New bot message — Stitch-style expand
   ============================================ */
.bubble-row.bot.msg-new {
  /* Override bubbleIn: row fades in instantly so avatar is visible */
  animation: msgRowIn 0.25s ease both;
}

@keyframes msgRowIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

.msg-new .chat-bubble {
  animation: msgExpand 0.65s cubic-bezier(0.22, 0.61, 0.36, 1) forwards;
  overflow: hidden;
}

@keyframes msgExpand {
  0%  { max-height: 36px; opacity: 0.5; }
  30% { max-height: 36px; opacity: 1; }
  100% { max-height: 80vh; opacity: 1; }
}

/* ============================================
   Thinking Dots
   ============================================ */
.thinking-row {
  animation: thinkingIn 0.3s ease-out both;
}
@keyframes thinkingIn {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

.thinking-bubble {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 11px 18px;
  border-radius: 14px;
  border-top-left-radius: 4px;
  background-color: var(--chat-msg-bg);
  border: 1px solid var(--chat-msg-border);
  transition: background-color 0.4s, border-color 0.4s;
}

.thinking-bubble .dot {
  display: block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--text-secondary);
  animation: dotPulse 1.4s ease-in-out infinite;
}
.thinking-bubble .dot:nth-child(2) { animation-delay: 0.2s; }
.thinking-bubble .dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes dotPulse {
  0%, 80%, 100% { opacity: 0.25; transform: scale(0.75); }
  40%           { opacity: 1;    transform: scale(1.15); }
}

/* ============================================
   Avatar
   ============================================ */
.bubble-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--chat-msg-bg);
  border: 1px solid var(--chat-msg-border);
  transition: background-color 0.4s, border-color 0.4s;
}
.bubble-row.user .bubble-avatar {
  background: rgba(200, 206, 214, 0.5);
  border-color: rgba(170, 178, 190, 0.45);
}
.avatar-icon {
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
}

/* ============================================
   Chat Bubble
   ============================================ */
.chat-bubble {
  max-width: 78%;
  padding: 9px 13px;
  border-radius: 14px;
  font-size: 13px;
  line-height: 1.55;
  word-break: break-word;
  color: var(--text-primary);
  transition: background-color 0.4s, border-color 0.4s, color 0.4s, box-shadow 0.4s;
  position: relative;
}

.bubble-row.bot .chat-bubble {
  background-color: var(--chat-msg-bg);
  border: 1px solid var(--chat-msg-border);
  border-top-left-radius: 4px;
  max-width: 74%;
}
.bubble-row.user .chat-bubble {
  background-color: var(--chat-user-bg);
  border: 1px solid var(--chat-user-border);
  border-top-right-radius: 4px;
}

/* ============================================
   Search Results — section entrance
   ============================================ */
.results-enter {
  animation: resultsSectionIn 0.35s ease-out both;
}
@keyframes resultsSectionIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

.theme-results {
  margin: 12px 0;
  padding: 10px;
  background: transparent;
  border-radius: 12px;
  border: 1px solid rgba(140, 180, 220, 0.35);
  box-shadow: none;
}
.theme-results.component-results { border-color: rgba(230, 160, 80, 0.35); }
.theme-results-header { font-weight: bold; font-size: 13px; color: var(--text-primary); margin-bottom: 8px; padding-bottom: 5px; border-bottom: 1px solid rgba(140, 180, 220, 0.2); }
.component-results .theme-results-header { border-bottom-color: rgba(230, 160, 80, 0.2); }
.theme-results-list { display: flex; flex-direction: column; gap: 6px; }

/* ============================================
   Result Items — staggered entrance
   ============================================ */
.result-stagger {
  opacity: 0;
  transform: translateY(10px);
  animation: resultSlideIn 0.32s ease forwards;
  animation-delay: calc(var(--i, 0) * 0.07s);
}
@keyframes resultSlideIn {
  to { opacity: 1; transform: translateY(0); }
}

.result-item {
  display: flex;
  align-items: center;
  padding: 7px 8px;
  background: var(--glass-bg);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid var(--glass-border);
}
.result-item:hover {
  background: color-mix(in srgb, var(--btn-bg) 12%, var(--glass-bg));
  border-color: var(--btn-bg);
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.result-number { background: #4CAF50; color: white; width: 18px; height: 18px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; margin-right: 8px; flex-shrink: 0; }
.component-results .result-number { background: #e67e22; }
.result-content { flex: 1; display: flex; flex-direction: column; gap: 5px; }
.result-name { font-size: 12px; color: var(--text-primary); font-weight: 500; line-height: 1.2; }
.result-details { display: flex; flex-wrap: wrap; gap: 4px; align-items: center; }
.result-city { font-size: 9px; color: #e67e22; background: #fef9e7; padding: 1px 6px; border-radius: 12px; font-weight: 500; border: 1px solid #f39c12; }
.result-structure { font-size: 9px; color: #3498db; background: #ebf3fd; padding: 1px 6px; border-radius: 12px; font-weight: 500; border: 1px solid #3498db; }
.result-year { font-size: 9px; color: #9b59b6; background: #f4ecf7; padding: 1px 6px; border-radius: 12px; font-weight: 500; border: 1px solid #9b59b6; }
.result-feature { font-size: 9px; color: #16a085; background: #e8f8f5; padding: 1px 6px; border-radius: 12px; font-weight: 500; border: 1px solid #1abc9c; }
.result-score { font-size: 9px; color: #7f8c8d; background: rgba(127,140,141,0.1); padding: 1px 6px; border-radius: 12px; font-weight: 600; border: 1px solid rgba(127,140,141,0.25); }
</style>
