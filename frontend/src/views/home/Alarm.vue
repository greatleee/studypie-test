<style lang="scss">
.center {
  text-align: center;
  margin-top: auto;
  margin-bottom: auto;
}

.w-70 {
  width: 70%;
}

.w-30 {
  width: 30%;
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
            <div class="w-70 center">내용</div>
            <div class="w-30 center">날짜</div>
          </div>
        </v-card>
      </v-col>
      <v-col v-for="(edge, i) in alarms.edges" :key="i" cols="12">
        <v-card height="50">
          <div class="d-flex justify-space-around" style="height: 100%">
            <div class="w-70 center">
              {{ edge.node.message }}
            </div>
            <div class="w-30 center">
              {{ formatDate(edge.node.createdAt) }}
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
import gql from "graphql-tag";
import utils from "../../common/utils";

export default {
  mixins: [utils],

  data() {
    return {
      alarms: {
        pageInfo: {
          endCursor: "",
          hasNextPage: false,
        },
        edges: [],
      },
    };
  },

  apollo: {
    alarms: {
      query: gql`
        query($first: Int!, $after: String) {
          alarms(first: $first, after: $after) {
            pageInfo {
              endCursor
              hasNextPage
            }
            edges {
              cursor
              node {
                id
                message
                createdAt
              }
            }
          }
        }
      `,
      variables() {
        return {
          first: 30,
        };
      },
    },
  },

  methods: {
    onClickFetchMore: function() {
      if (!this.alarms.pageInfo.hasNextPage) {
        alert("데이터가 더 존재하지 않습니다.");
        return;
      }
      this.$apollo.queries.alarms.fetchMore({
        variables: {
          first: 30,
          after: this.alarms.pageInfo.endCursor,
        },
        updateQuery(previousResult, { fetchMoreResult }) {
          const newEdges = fetchMoreResult.alarms.edges;
          const pageInfo = fetchMoreResult.alarms.pageInfo;

          return {
            ...previousResult,
            alarms: {
              ...previousResult.alarms,
              edges: [...previousResult.alarms.edges, ...newEdges],
              pageInfo,
            },
          };
        },
      });
    },
  },
};
</script>
