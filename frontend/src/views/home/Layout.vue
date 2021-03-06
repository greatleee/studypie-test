<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <router-link to="/">
          <v-btn text>게시판</v-btn>
        </router-link>
        <router-link to="/points">
          <v-btn text>포인트 내역</v-btn>
        </router-link>
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn v-bind="attrs" v-on="on" text>
              <v-badge v-if="alarms.length !== 0" color="error" dot>
                알람
              </v-badge>
              <span v-else>알람</span>
            </v-btn>
          </template>
          <div style="height: 250px; width: 300px; background: white">
            <v-list
              v-if="alarms.length !== 0"
              height="200"
              width="300"
              style="overflow-y: auto"
            >
              <v-list-item v-for="(edge, index) in alarms" :key="index">
                <v-list-item-title>
                  {{ edge.node.message }}
                </v-list-item-title>
                <v-list-item-icon>
                  <v-icon @click="onClickSetAlarmChecked(index, edge.node.id)">
                    mdi-check-bold
                  </v-icon>
                </v-list-item-icon>
              </v-list-item>
            </v-list>
            <div
              v-else
              style="height: 200px; width: 300px; text-align: center; padding-top: 70px;"
            >
              알람이 없습니다.
            </div>
            <v-list-item link @click="routeToAlarm">
              알람 히스토리 보기
            </v-list-item>
          </div>
        </v-menu>
      </div>

      <v-spacer></v-spacer>

      <div class="mr-2">잔여 포인트: {{ totalRemainedPoint }}</div>
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
import gql from "graphql-tag";
import auth from "@/common/auth";

export default {
  name: "Home",

  data() {
    return {
      totalRemainedPoint: 0,
      alarms: [],
    };
  },

  apollo: {
    totalRemainedPoint: {
      query: gql`
        query {
          totalRemainedPoint
        }
      `,
    },
    alarms: {
      query: gql`
        query {
          alarmsNotChecked(first: 5) {
            edges {
              node {
                id
                message
                isChecked
                createdAt
              }
            }
          }
        }
      `,
      fetchPolicy: "no-cache",
      update: (data) => data.alarmsNotChecked.edges,
    },
  },

  methods: {
    onClickLogoutBtn: async function() {
      if (await auth.logout()) window.location.reload();
    },
    routeToAlarm: function() {
      if (this.$router.currentRoute.name !== "Home.Alarm")
        this.$router.push("/alarms");
    },
    onClickSetAlarmChecked: async function(index, id) {
      try {
        await this.$apollo.mutate({
          mutation: gql`
            mutation($id: ID!) {
              setAlarmIsChecked(input: { id: $id }) {
                alarm {
                  id
                  message
                  isChecked
                }
              }
            }
          `,
          variables: {
            id: id,
          },
        });
      } catch (error) {
        alert(error);
        return;
      }
      this.alarms.splice(index, 1);
    },
  },

  created() {
    const socket = new WebSocket("ws://localhost:8000/alarms/");

    socket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      this.alarms.unshift({
        node: data,
      });
    };

    socket.onopen = () => {
      console.log("websocket connected");
    };

    socket.onclose = () => {
      console.log("websocket connection failed");
    };
  },
};
</script>
