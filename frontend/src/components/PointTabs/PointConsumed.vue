<template>
  <v-container>
    <point-tab-layout
      :edges="pointsConsumed.edges"
      :hasExpireAt="false"
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
      pointsConsumed: {
        pageInfo: {
          endCursor: "",
          hasNextPage: false,
        },
        edges: [],
      },
    };
  },

  apollo: {
    pointsConsumed: {
      query: gql`
        query($first: Int!, $after: String) {
          pointsConsumed(first: $first, after: $after) {
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
      this.$apollo.queries.pointsConsumed.fetchMore({
        variables: {
          first: 30,
          after: this.pointsConsumed.pageInfo.endCursor,
        },
        updateQuery(previousResult, { fetchMoreResult }) {
          const newEdges = fetchMoreResult.pointsConsumed.edges;
          const pageInfo = fetchMoreResult.pointsConsumed.pageInfo;

          return {
            ...previousResult,
            pointsConsumed: {
              ...previousResult.pointsConsumed,
              edges: [...previousResult.pointsConsumed.edges, ...newEdges],
              pageInfo,
            },
          };
        },
      });
    },
  },
};
</script>
