<template>
  <v-container>
    <point-tab-layout
      :edges="pointsExpired.edges"
      :hasExpireAt="true"
      :onClickFetchMore="onClickFetchMore"
    ></point-tab-layout>
  </v-container>
</template>

<script>
import gql from "graphql-tag";
import PointTabLayout from "./Layout";

export default {
  components: { PointTabLayout },

  data() {
    return {
      pointsExpired: {
        pageInfo: {
          endCursor: "",
          hasNextPage: false,
        },
        edges: [],
      },
    };
  },

  apollo: {
    pointsExpired: {
      query: gql`
        query($first: Int!, $after: String) {
          pointsExpired(first: $first, after: $after) {
            pageInfo {
              endCursor
              hasNextPage
            }
            edges {
              cursor
              node {
                id
                action
                point
                createdAt
                expireAt
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
      if (!this.pointsConsumed.pageInfo.hasNextPage) {
        alert("데이터가 더 존재하지 않습니다.");
        return;
      }
      this.$apollo.queries.pointsExpired.fetchMore({
        variables: {
          first: 30,
          after: this.pointsExpired.pageInfo.endCursor,
        },
        updateQuery(previousResult, { fetchMoreResult }) {
          const newEdges = fetchMoreResult.pointsExpired.edges;
          const pageInfo = fetchMoreResult.pointsExpired.pageInfo;

          return {
            ...previousResult,
            pointsExpired: {
              ...previousResult.pointsExpired,
              edges: [...previousResult.pointsExpired.edges, ...newEdges],
              pageInfo,
            },
          };
        },
      });
    },
  },
};
</script>
