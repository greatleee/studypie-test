<template>
  <v-app class="board">
    <v-navigation-drawer app permanent>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            게시판
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item link @click.stop="isCreateBoardDialogShown = true">
        <v-list-item-content>
          게시판 추가
        </v-list-item-content>
        <v-list-item-avatar>
          <v-icon color="blue">mdi-plus-circle</v-icon>
        </v-list-item-avatar>
      </v-list-item>

      <v-divider></v-divider>

      <v-list v-for="(item, i) in boards" :key="i">
        <v-list-item link @click="onClickTargetBoard(item.id)">
          <v-list-item-content>
            {{ item.name }}
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app app>
      <v-container fluid>
        <post-table
          v-if="boards.length !== 0"
          :boardId="curBoardId"
        ></post-table>
      </v-container>
    </v-app>
    <create-board-dialog
      :dialog="isCreateBoardDialogShown"
    ></create-board-dialog>
  </v-app>
</template>

<script>
import gql from "graphql-tag";
import CreateBoardDialog from "../../components/CreateBoardDialog.vue";
import PostTable from "../../components/PostTable.vue";

export default {
  name: "Home.Board",

  components: {
    CreateBoardDialog,
    PostTable,
  },

  data() {
    return {
      curBoardId: 0,
      boards: [],
      isCreateBoardDialogShown: false,
    };
  },

  apollo: {
    boards: {
      query: gql`
        query {
          allBoards {
            id
            name
          }
        }
      `,
      update: (data) => data.allBoards,
    },
  },

  watch: {
    boards: function() {
      if (this.curBoardId === 0 && this.boards.length !== 0) {
        this.curBoardId = this.boards[0].id;
      }
    },
  },

  methods: {
    onClickTargetBoard: function(boardId) {
      this.curBoardId = boardId;
    },
  },

  created() {
    this.$root.$on("hideCreateBoardDialog", () => {
      this.isCreateBoardDialogShown = false;
    });
    this.$root.$on("setBoardList", (boards) => {
      this.boards = boards;
      this.isCreateBoardDialogShown = false;
    });
  },
};
</script>
