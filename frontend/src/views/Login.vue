<template>
  <v-main class="login">
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-text-field v-model="username" label="Username" required></v-text-field>
      <v-text-field
        v-model="password"
        :type="'password'"
        label="Password"
        required
      ></v-text-field>
      <v-btn :disabled="!valid" color="info" @click="onClickLoginBtn">
        로그인
      </v-btn>
    </v-form>
  </v-main>
</template>

<script>
import auth from "../common/auth";

export default {
  name: "Login",

  data() {
    return {
      valid: false,
      username: "",
      password: "",
    };
  },

  methods: {
    onClickLoginBtn: async function() {
      let response;
      try {
        response = await auth.login(this.username, this.password);
      } catch (error) {
        this.$root.$emit("showAlert", "네트워크 오류입니다.");
      }

      if (response.status === 200) {
        this.$router.push("/");
      } else if (response.status === 401) {
        this.$root.$emit("showAlert", "사용자 이름과 비밀번호를 확인해주세요.");
      } else {
        this.$root.$emit("showAlert", "네트워크 오류입니다.");
      }
    },
  },
};
</script>
