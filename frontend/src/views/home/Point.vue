<template>
  <v-container>
    <v-toolbar color="primary" dense>
      <template v-slot>
        <v-tabs v-model="curTab" align-with-title>
          <v-tabs-slider color="white"></v-tabs-slider>

          <v-tab class="white--text" v-for="tab in tabs" :key="tab.key">
            {{ tab.value }}
          </v-tab>
        </v-tabs>
      </template>
    </v-toolbar>
    <div>
      <point-issued v-if="curTab === 0"></point-issued>
      <point-consumed v-else-if="curTab === 1"></point-consumed>
      <point-expired v-else-if="curTab === 2"></point-expired>
    </div>
  </v-container>
</template>

<script>
import PointIssued from "../../components/PointTabs/PointIssued.vue";
import PointConsumed from "../../components/PointTabs/PointConsumed.vue";
import PointExpired from "../../components/PointTabs/PointExpired.vue";

export default {
  name: "Point",

  components: {
    PointIssued,
    PointConsumed,
    PointExpired,
  },

  data() {
    return {
      curTab: 0,
      tabs: [
        { key: 0, value: "누적 히스토리" },
        { key: 1, value: "사용 히스토리" },
        { key: 2, value: "만료된 포인트" },
      ],
    };
  },

  watch: {},

  methods: {},
};
</script>
