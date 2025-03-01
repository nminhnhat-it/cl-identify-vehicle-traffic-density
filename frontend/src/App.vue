<script>
export default {
  async mounted() {
    this.$store.state.apiUrl = "http://localhost:3000/";
  }
}
</script>

<template>
  <router-view />
</template>