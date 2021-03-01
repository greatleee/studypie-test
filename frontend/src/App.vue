<template>
  <v-app>
    <router-view></router-view>
    <v-snackbar v-model="isAlertShown" color="red">
      {{ alertMsg }}

      <template v-slot:action="{ attrs }">
        <v-btn color="black" text v-bind="attrs" @click="isAlertShown = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
export default {
  name: "App",

  data() {
    return {
      isAlertShown: false,
      alertMsg: "",
    };
  },

  created() {
    this.$root.$on("showAlert", (msg) => {
      this.isAlertShown = true;
      this.alertMsg = msg;
    });
  },
};
</script>
