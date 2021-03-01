<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <router-link to="/">
          <v-btn text>게시판</v-btn>
        </router-link>
      </div>

      <v-spacer></v-spacer>

      <v-btn text @click="onClickLogoutBtn">
        <span>로그아웃</span>
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
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
