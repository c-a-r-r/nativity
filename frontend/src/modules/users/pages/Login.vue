<!-- frontend/src/views/Login.vue -->
<template>
  <div>
    <!-- Top bar -->
    <div class="vz-login-top">
      <p class="vz-login-logo">
        <svg width="30" height="30" xmlns="http://www.w3.org/2000/svg">
          <rect x="2" y="2" width="26" height="26"
                fill="#fff" stroke="#333" stroke-width="2" rx="5" ry="5"/>
          <text x="50%" y="50%" dy=".4em"
                font-family="Arial" font-weight="bold" font-size="22"
                text-anchor="middle" fill="#333">V</text>
        </svg>
        <span style="font-weight:bold">VIZITOR</span>
      </p>
    </div>

    <!-- Centered Card -->
    <div class="vz-login-container">
        <div class="vz-logo">
        <svg
            class="vz-logo-svg"  
            viewBox="0 0 100 100"
            xmlns="http://www.w3.org/2000/svg">

            <!-- outer square -->
            <rect x="5" y="5" width="90" height="90"
                rx="12" ry="12"
                fill="#fff"
                stroke="#333"
                stroke-width="4"/>

            <!-- big centred V -->
            <text x="50" y="50"
                text-anchor="middle"
                dominant-baseline="central"
                font-family="Roboto, sans-serif"
                font-weight="bold"
                font-size="70"
                fill="#333">
            V
            </text>
        </svg>
        </div>
        <!-- Login Form -->
      <h1>VIZITOR</h1>

        <form @submit.prevent="onSubmit">
        <input
            id="usuario"
            v-model="form.usuario"
            type="text"
            placeholder="Username"
            autocomplete="username"
        />

        <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="Password"
            autocomplete="current-password"
        />

        <button type="submit">Sign In</button>
        </form>

      <p v-if="error" class="error">{{ error }}</p>
    </div>

    <!-- Footer -->
    <div class="vz-login-bottom">
      <p>Copyright © 2023 Vizitor Inc. All rights reserved</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router  = useRouter()
const form    = ref({ usuario: '', password: '' })
const error   = ref('')
const loading = ref(false)

async function onSubmit() {
  // reset any previous error
  error.value = ''

  // front‐end validation
  if (!form.value.usuario || !form.value.password) {
    error.value = 'Both fields are required'
    return
  }

  // start spinner (optional)
  loading.value = true

  let tokens
  try {
    const res = await axios.post('/api/auth/login/', {
      usuario:  form.value.usuario,
      password: form.value.password
    })
    tokens = res.data
  } catch (e) {
    // stop spinner
    loading.value = false

    // only treat 401 as "invalid creds"
    if (e.response?.status === 401) {
      error.value = "Your username and password didn't match."
    } else {
      error.value = 'An unexpected error occurred.'
      console.error(e)
    }
    return     // <—— return early so we don’t try to navigate
  }

  // login success: store tokens
  localStorage.setItem('access',  tokens.access)
  localStorage.setItem('refresh', tokens.refresh)

  // stop spinner
  loading.value = false

  // now navigate (if this fails, it won't reset our error)
  router.push({ name: 'Dashboard' })
    .catch(navErr => console.warn('Navigation error:', navErr))
}
</script>

<style>
/* Global page styles */
body {
  background-color: #f7f7f7;
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
 
  justify-content: center;
  align-items: center;
  height: 100%;

}

/* Top bar */
.vz-login-top {
  position: fixed;
  top: 0;
  width: 100%;
  text-align: left;
  z-index: 100;
  background: transparent;
}
.vz-login-logo {
  margin: 5px;
  display: flex;
  align-items: center;
  gap: 5px;
}

/* Main card */
.vz-login-container {
  position: fixed;      /* keep it pinned to the viewport */
  top: 50%;             /* 50% down from the top */
  left: 50%;            /* 50% in from the left */
  transform: translate(-50%, -50%); /* pull it back by half its own width/height */
  width: 500px;
  max-width: calc(100% - 40px);     /* responsive on very small screens */
  border-radius: 30px;
  padding: 30px;
  text-align: center;
  background-color: #fff;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1),
              0 4px 12px rgba(0, 0, 0, 0.15);
}

.vz-logo {
  margin-bottom: 10px;
}
h1 {
  font-size: 30px;
  margin-bottom: 10px;
}


/* Error message */
.error {
  color: #d32f2f;
  margin-top: 12px;
  font-size: 0.9rem;
}

/* Bottom footer */
.vz-login-bottom {
  position: fixed;
  bottom: 0;
  width: 100%;
  background-color: #bfbebe;
  text-align: center;
  z-index: 100;
}
.vz-login-bottom p {
  font-size: 11px;
  color: rgb(49, 49, 49);
  margin: 5px 0;
}
/* Add or update in your <style> */
.vz-login-container form {
  width: 80%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}


.vz-login-container form button {
  background-color: #113a5c;
  color: #fff;
  padding: 12px 0;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 18px;
  margin-top: 20px;
  width: 50%;
  transition: background 0.2s;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.vz-login-container form button:hover {
  background-color: #14508c;
}
.vz-login-container input[type="text"],
.vz-login-container input[type="password"] {
  width: 100%;
  box-sizing: border-box;
  padding: 15px;
  margin-top: 5px;
  margin-bottom: 16px;   /* Add this line for spacing */
  border: 1px solid #ccc;
  border-radius: 10px;
  font-size: 1rem;
  background: #e6eeff;
}
.vz-logo-svg {
  width: 100px;
  height: 100px;
}
</style>