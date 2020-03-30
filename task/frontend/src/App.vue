<template>
<div class="wrapper-sidebar" id="task-app">

  <nav class="sidebar" :class="{'active': hideSidebar}">
    <span><i class="fas fa-bars mt-2"></i> ALL</span>
    <ul class="list-unstyled components">
      <li><router-link to="/">Projects</router-link></li>
      <li><router-link to="/tasks">Tasks</router-link></li>
      <li><router-link to="/about">About</router-link></li>
    </ul>
  </nav>

  <div class="content w-100">
    <ul class="nav mx-2">
      <button type="button" class="btn btn-info btn-sm" @click="hideSidebar = !hideSidebar">
        <i class="fas fa-align-left"></i><span>Toggle</span>
      </button>
    </ul>

    <router-view></router-view>
  </div> <!-- End content -->
</div> <!-- End wrapper -->

</template>

<script lang="ts">
import Vue from 'vue';
export default Vue.extend({
  data() {
    return {
      hideSidebar: false,
    };
  },
});
</script>