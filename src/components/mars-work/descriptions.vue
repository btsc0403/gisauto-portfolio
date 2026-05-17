<template>
    <div class="modal">
      <div class="modal-content">
        <button class="close-button" @click="$emit('close')">×</button>
        <h2>{{ building?.label }}</h2>
        <p>Latitude: {{ building?.lat }}</p>
        <p>Longitude: {{ building?.lng }}</p>
        <p>Description: {{ description }}</p>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  const props = defineProps({
    building: Object,
    description: String
  })
  </script>
  
  <style scoped>
  .modal {
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
    height: 100%;
    background-color: #ffffff;
    padding: 20px;
    z-index: 1000;
    border-radius: 15px;
    border: 2px solid #ccc;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    overflow-y: auto; /* 使模态框可以滚动 */
  }
  
  .modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .close-button {
    position: absolute;
    top: 5px;
    right: 5px;
    background-color: transparent;
    border: none;
    color: #000;
    font-size: 1.5em;
    cursor: pointer;
    outline: none;
    box-shadow: none;
    transition: color 0.3s ease, text-shadow 0.3s ease;
  }
  
  .close-button:hover {
    color: #000;
    text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  }  
  </style>
