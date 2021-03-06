<style lang="scss">
.center {
  text-align: center;
  margin-top: auto;
  margin-bottom: auto;
}

.w-15 {
  width: 15%;
}

.w-35 {
  width: 35%;
}
</style>

<template>
  <v-container>
    <v-row dense>
      <v-col>
        <v-card height="40" color="primary">
          <div
            class="d-flex white--text justify-space-around"
            style="height: 100%"
          >
            <div class="w-15 center">사유</div>
            <div class="w-15 center">{{ getHumanReadablePointHeader() }}</div>
            <div class="w-35 center">
              {{ getHumanReadableCreatedAtHeader() }}
            </div>
            <div v-if="hasExpireAt" class="w-35 center">만료일</div>
          </div>
        </v-card>
      </v-col>
      <v-col v-for="(edge, i) in edges" :key="i" cols="12">
        <v-card
          height="50"
          :color="checkExpiredAndGetColor(edge.node.expireAt)"
        >
          <div class="d-flex justify-space-around" style="height: 100%">
            <div class="w-15 center">
              {{ getHumanReadablePointAction(edge.node.action) }}
            </div>
            <div class="w-15 center">{{ edge.node.point }}</div>
            <div class="w-35 center">
              {{ formatDate(edge.node.createdAt) }}
            </div>
            <div v-if="hasExpireAt" class="w-35 center">
              {{ formatDate(edge.node.expireAt) }}
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col>
        <div class="center">
          <v-btn color="success" @click="onClickFetchMore">더 보기</v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import utils from "../../common/utils";

export default {
  props: ["edges", "hasExpireAt", "onClickFetchMore"],

  mixins: [utils],

  methods: {
    getHumanReadablePointHeader: function() {
      if (this.hasExpireAt === true) {
        return "획득 포인트";
      } else {
        return "사용 포인트";
      }
    },
    getHumanReadableCreatedAtHeader: function() {
      if (this.hasExpireAt === true) {
        return "획득일";
      } else {
        return "사용일";
      }
    },
    checkExpiredAndGetColor: function(expireAt) {
      if (expireAt === undefined) return "white";
      const now = new Date();
      const expireAtDate = new Date(expireAt);
      if (now < expireAtDate) {
        return "white";
      } else {
        return "red";
      }
    },
  },
};
</script>
