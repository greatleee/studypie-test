<template>
  <div class="home">
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center"></div>

      <v-spacer></v-spacer>

      <v-btn text @click="onClickLogoutBtn">
        <span class="mr-2">로그아웃</span>
      </v-btn>
    </v-app-bar>

    <v-main></v-main>
  </div>
</template>

<script>
import auth from "@/common/auth";

export default {
  name: "Home",

  methods: {
    onClickLogoutBtn: async function() {
      if (await auth.logout()) window.location.reload();
    },
  },
};
</script>
