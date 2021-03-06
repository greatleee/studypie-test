<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="posts"
      :items-per-page="10"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialogCreate" max-width="500px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                글 작성하기
              </v-btn>
            </template>
            <v-card>
              <v-card-text>
                <v-container>
                  <v-form v-model="isValid">
                    <v-text-field
                      v-model="newPost.title"
                      :counter="100"
                      :rules="titleRules"
                      label="제목"
                      required
                    ></v-text-field>
                    <v-textarea
                      v-model="newPost.content"
                      name="input-7-1"
                      label="내용"
                    ></v-textarea>
                  </v-form>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn :disabled="!isValid" text @click="dialogCreate = false">
                  취소
                </v-btn>
                <v-btn color="blue" text @click="onClickConfirmCreate">
                  완료
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="headline">
                정말 삭제하시겠습니까?
              </v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text @click="dialogDelete = false">
                  취소
                </v-btn>
                <v-btn color="red" @click="onClickConfirmDel()">
                  확인
                </v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.createdAt="{ item }">
        {{ formatDate(item.createdAt) }}
      </template>
      <template v-slot:item.detail="{ item }">
        <v-btn color="info" @click="onClickRow(item)" x-small>자세히</v-btn>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon @click="onClickDel(item.id)">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import gql from "graphql-tag";
import utils from "../common/utils";

export default {
  props: ["boardId"],

  mixins: [utils],

  data() {
    return {
      isValid: false,
      dialogCreate: false,
      newPost: {
        title: "",
        content: "",
      },
      titleRules: [
        (v) => !!v || "필수 입력 항목입니다.",
        (v) => (v && v.length <= 50) || "50 글자 이하만 입력가능합니다.",
      ],
      deletePostId: 0,
      dialogDelete: false,
      headers: [
        {
          text: "제목",
          align: "center",
          sortable: false,
          value: "title",
        },
        { text: "작성자", align: "center", value: "creator.username" },
        { text: "작성일", align: "center", value: "createdAt" },
        { text: "", align: "center", value: "detail" },
        { text: "", align: "center", value: "actions" },
      ],
      posts: [],
    };
  },

  apollo: {
    posts: {
      query: gql`
        query($boardId: Int!) {
          postsByBoard(boardId: $boardId) {
            id
            title
            creator {
              username
            }
            createdAt
          }
        }
      `,
      variables() {
        return {
          boardId: this.boardId,
        };
      },
      update: (data) => data.postsByBoard,
      fetchPolicy: "no-cache",
    },
  },

  methods: {
    initNewPost: function() {
      this.newPost = {
        title: "",
        content: "",
      };
    },
    onClickCancelCreate: function() {
      this.dialogCreate = false;
      this.initNewPost();
    },
    onClickConfirmCreate: async function() {
      let response;
      try {
        response = await this.$apollo.mutate({
          mutation: gql`
            mutation($title: String!, $content: String!, $boardId: Int!) {
              createPost(title: $title, content: $content, boardId: $boardId) {
                postsByBoard(boardId: $boardId) {
                  id
                  title
                  creator {
                    username
                  }
                  createdAt
                }
              }
            }
          `,
          variables: {
            title: this.newPost.title,
            content: this.newPost.content,
            boardId: this.boardId,
          },
        });
      } catch (error) {
        alert(error);
        return;
      }
      this.posts = response.data.createPost.postsByBoard;
      this.dialogCreate = false;
      this.initNewPost();
    },
    onClickDel: function(id) {
      this.deletePostId = id;
      this.dialogDelete = true;
    },
    onClickConfirmDel: async function() {
      let response;
      try {
        response = await this.$apollo.mutate({
          mutation: gql`
            mutation($id: Int!, $boardId: Int!) {
              deletePost(id: $id, boardId: $boardId) {
                postsByBoard(boardId: $boardId) {
                  id
                  title
                  creator {
                    username
                  }
                  createdAt
                }
              }
            }
          `,
          variables: {
            id: this.deletePostId,
            boardId: this.boardId,
          },
        });
      } catch (error) {
        alert(error);
        return;
      }
      this.posts = response.data.deletePost.postsByBoard;
      this.dialogDelete = false;
    },
    onClickRow: function(row) {
      console.log(row);
      this.$router.push({
        name: "Home.Post",
        params: {
          id: row.id,
        },
      });
    },
  },
};
</script>
