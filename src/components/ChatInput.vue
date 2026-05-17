<template>
  <div class="chat-input-wrapper">
    <!-- Branding banner — fades out on focus -->
    <div :class="['input-branding', { hidden: inputFocused }]">
      <img class="branding-logo" src="/logo.png" alt="Heritage Explorer" />
      <span class="branding-tagline">Journey through historic</span>
    </div>

    <div class="chat-input-box" :class="{ focused: inputFocused }">
      <input
        ref="fileInputRef"
        type="file"
        accept="image/*"
        style="display:none"
        @change="onFileSelected"
      />

      <div v-if="chatStore.uploadPreviewUrl" class="upload-preview">
        <img :src="chatStore.uploadPreviewUrl" alt="preview" />
        <button class="remove-preview" @click="chatStore.setUploadFile(null)" title="移除图片">&times;</button>
      </div>

      <textarea
        ref="textareaRef"
        v-model="chatStore.userInput"
        placeholder="搜索建筑、构件，或提出任何问题..."
        @keydown.enter.exact.prevent="chatStore.sendMessage()"
        @focus="inputFocused = true"
        @blur="inputFocused = false"
      ></textarea>

      <div class="input-toolbar">
        <div class="toolbar-spacer"></div>
        <button class="attach-btn" @click="fileInputRef?.click()" title="上传图片搜索">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="3" />
            <circle cx="8.5" cy="8.5" r="1.5" />
            <path d="m21 15-5-5L5 21" />
          </svg>
        </button>
        <button
          class="send-btn"
          :disabled="chatStore.isSearching || (!chatStore.userInput.trim() && !chatStore.uploadedFile)"
          @click="chatStore.sendMessage()"
        >
          <svg v-if="chatStore.isSearching" class="spin" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
          </svg>
          <svg v-else viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="19" x2="12" y2="5" />
            <polyline points="5 12 12 5 19 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useChatStore } from "../stores/chatStore"

const chatStore = useChatStore()
const fileInputRef = ref<HTMLInputElement | null>(null)
const textareaRef = ref<HTMLTextAreaElement | null>(null)
const inputFocused = ref(false)

function onFileSelected(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files?.length) {
    chatStore.setUploadFile(input.files[0])
  }
  input.value = ""
}
</script>

<style scoped>
.chat-input-wrapper {
  position: fixed;
  bottom: 65px;
  left: calc(355px + (72% - 375px) / 4);
  right: calc(28% + 20px + (72% - 375px) / 4);
  z-index: 100;
  pointer-events: auto;
}

/* --- Branding banner --- */
.input-branding {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 6px 8px;
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.35s ease, transform 0.35s ease;
  pointer-events: none;
}
.input-branding.hidden {
  opacity: 0;
  transform: translateY(6px);
}

.branding-logo {
  height: 36px;
  width: auto;
  object-fit: contain;
}

.branding-tagline {
  font-family: "Alfa Slab One", serif;
  font-size: 13px;
  color: var(--text-secondary);
  opacity: 0.55;
  letter-spacing: 0.3px;
}

/* --- Input box --- */
.chat-input-box {
  border: 1px solid rgba(160, 180, 200, 0.35);
  border-radius: 14px;
  background: rgba(245, 245, 248, 1);
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  box-shadow:
    0 2px 20px rgba(0, 0, 0, 0.08),
    0 0 0 0.5px rgba(255, 255, 255, 0.15) inset;
  transition: border-color 0.25s, box-shadow 0.25s, background 0.3s;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.chat-input-box.focused {
  border-color: color-mix(in srgb, var(--btn-bg) 40%, rgba(160, 180, 200, 0.4));
  box-shadow:
    0 4px 28px rgba(0, 0, 0, 0.1),
    0 0 0 2px color-mix(in srgb, var(--btn-bg) 10%, transparent),
    0 0 0 0.5px rgba(255, 255, 255, 0.18) inset;
  background: rgba(240, 240, 244, 1);
}

.upload-preview {
  position: relative;
  padding: 6px 10px 0;
  display: flex;
  align-items: flex-start;
}
.upload-preview img {
  width: auto;
  max-width: 120px;
  max-height: 48px;
  object-fit: contain;
  border-radius: 6px;
  border: 1px solid rgba(160, 180, 200, 0.25);
}
.remove-preview {
  position: absolute;
  top: 6px;
  left: 118px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: rgba(0,0,0,0.45);
  color: #fff;
  border: none;
  font-size: 12px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}
.remove-preview:hover { background: rgba(0,0,0,0.7); }

textarea {
  width: 100%;
  padding: 10px 14px 4px;
  border: none;
  outline: none;
  resize: none;
  min-height: 26px;
  max-height: 80px;
  font-size: 13px;
  line-height: 1.4;
  caret-color: var(--btn-bg);
  box-sizing: border-box;
  background: transparent;
  color: var(--text-primary);
  font-family: "Microsoft YaHei", "PingFang SC", system-ui, sans-serif;
}
textarea::placeholder {
  color: var(--text-secondary);
  opacity: 0.45;
  font-size: 12.5px;
}

.input-toolbar {
  display: flex;
  align-items: center;
  padding: 0 10px 9px;
  margin-top: 0;
  gap: 4px;
}
.toolbar-spacer { flex: 1; }

.attach-btn {
  width: 28px;
  height: 28px;
  padding: 0;
  border-radius: 50%;
  border: none;
  background: #c27a7a;
  color: #fff;
  opacity: 0.35;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background-color 0.2s, transform 0.12s, opacity 0.25s;
}
.chat-input-box.focused .attach-btn { opacity: 1; }
.attach-btn:hover { background: #a85a5a; opacity: 1; }
.attach-btn:active { transform: scale(0.92); }

.send-btn {
  width: 28px;
  height: 28px;
  padding: 0;
  border-radius: 50%;
  border: none;
  background-color: var(--btn-bg);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  opacity: 0.35;
  transition: background-color 0.2s, transform 0.12s, opacity 0.25s;
}
.chat-input-box.focused .send-btn { opacity: 1; }
.send-btn:hover:not(:disabled) { background-color: var(--btn-hover); opacity: 1; }
.send-btn:active:not(:disabled) { transform: scale(0.92); }
.send-btn:disabled { opacity: 0.25 !important; cursor: not-allowed; }

@keyframes spin { to { transform: rotate(360deg); } }
.spin { animation: spin 1s linear infinite; }
</style>
