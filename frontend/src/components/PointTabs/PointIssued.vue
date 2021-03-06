<template>
  <v-container>
    <point-tab-layout
      :edges="pointsIssued.edges"
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
      pointsIssued: {
        pageInfo: {
          endCursor: "",
          hasNextPage: false,
        },
        edges: [],
      },
    };
  },

  apollo: {
    pointsIssued: {
      query: gql`
        query($first: Int!, $after: String) {
          pointsIssued(first: $first, after: $after) {
            pageInfo {
              startCursor
              endCursor
              hasNextPage
              hasPreviousPage
            }
            edges {
              cursor
              node {
                id
                action
                point
                expireAt
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
      this.$apollo.queries.pointsIssued.fetchMore({
        variables: {
          first: 30,
          after: this.pointsIssued.pageInfo.endCursor,
        },
        updateQuery(previousResult, { fetchMoreResult }) {
          const newEdges = fetchMoreResult.pointsIssued.edges;
          const pageInfo = fetchMoreResult.pointsIssued.pageInfo;

          return {
            ...previousResult,
            pointsIssued: {
              ...previousResult.pointsIssued,
              edges: [...previousResult.pointsIssued.edges, ...newEdges],
              pageInfo,
            },
          };
        },
      });
    },
  },
};
</script>
