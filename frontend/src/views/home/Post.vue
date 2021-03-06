<template>
  <v-app class="post">
    <v-container>
      <v-toolbar color="light" flat>
        <v-spacer></v-spacer>
        <v-btn v-if="!isEditing" color="primary" @click="onClickEditing">
          글 수정하기
        </v-btn>
        <v-btn v-else color="success" @click="onClickSavePost">
          저장하기
        </v-btn>
      </v-toolbar>
      <div class="text-h5 mt-5 d-flex">
        <div class="mr-4">제목:</div>
        <div v-if="!isEditing">
          {{ post.title }}
        </div>
        <div v-else>
          <v-text-field v-model="editedPost.title" dense></v-text-field>
        </div>
      </div>
      <div class="mt-5">
        <div class="text-h6">내용</div>
        <div v-if="!isEditing" class="text-body-1">
          {{ post.content }}
        </div>
        <div v-else>
          <v-textarea v-model="editedPost.content"></v-textarea>
        </div>
      </div>
      <div class="mt-5">
        <div class="text-h6">댓글</div>
        <div>
          <div class="d-flex">
            <v-textarea
              v-model="newComment"
              placeholder="댓글을 입력하세요"
              no-resize
            ></v-textarea>
            <div class="ml-10 my-auto">
              <v-btn color="primary" @click="onClickSubmitComment">등록</v-btn>
            </div>
          </div>
          <div class="mt-5">
            <div v-for="(comment, i) in post.commentSet" :key="i" class="mb-5">
              <div class="d-flex">
                <div>{{ comment.creator.username }}</div>
                <div class="ml-5">
                  {{ datetimeToLocale(comment.createdAt) }}
                </div>
              </div>
              <div class="mt-2">{{ comment.content }}</div>
            </div>
          </div>
        </div>
      </div>
    </v-container>
  </v-app>
</template>

<script>
import gql from "graphql-tag";

export default {
  props: ["id"],

  data() {
    return {
      isEditing: false,
      post: {
        title: "",
        content: "",
        commentSet: [],
        createdAt: "",
        updatedAt: "",
      },
      editedPost: {
        title: "",
        content: "",
      },
      newComment: "",
    };
  },

  apollo: {
    post: {
      query: gql`
        query($postId: Int) {
          postById(postId: $postId) {
            title
            content
            commentSet {
              content
              creator {
                username
              }
              createdAt
            }
            createdAt
            updatedAt
          }
        }
      `,
      variables() {
        return {
          postId: this.id,
        };
      },
      update: (data) => data.postById,
    },
  },

  methods: {
    onClickEditing: function() {
      this.isEditing = true;
      this.editedPost.title = this.post.title;
      this.editedPost.content = this.post.content;
    },
    onClickSavePost: async function() {
      let response,
        params = {};
      if (this.editedPost.title !== this.post.title)
        params.title = this.editedPost.title;
      if (this.editedPost.content !== this.post.content)
        params.content = this.editedPost.content;
      if (Object.keys(params).length === 0) {
        this.isEditing = false;
        return;
      }
      try {
        response = await this.$apollo.mutate({
          mutation: gql`
            mutation($id: Int!, $title: String!, $content: String!) {
              updatePost(id: $id, title: $title, content: $content) {
                post {
                  title
                  content
                  updatedAt
                }
              }
            }
          `,
          variables() {
            params.id = this.id;
            return params;
          },
        });
      } catch (error) {
        alert(error);
        return;
      }
      this.post.title = response.data.post.title;
      this.post.content = response.data.content;
      this.post.updatedAt = response.data.updatedAt;
      this.isEditing = false;
    },
    onClickSubmitComment: async function() {
      let response;
      try {
        response = await this.$apollo.mutate({
          mutation: gql`
            mutation($content: String!, $postId: Int!) {
              createComment(content: $content, postId: $postId) {
                comment {
                  content
                  creator {
                    username
                  }
                  createdAt
                }
              }
            }
          `,
          variables: {
            content: this.newComment,
            postId: this.id,
          },
        });
      } catch (error) {
        alert(error);
        return;
      }
      const comment = response.data.createComment.comment;
      if (comment !== null) this.post.commentSet.unshift(comment);
    },
    datetimeToLocale: function(datetime) {
      return new Date(datetime).toLocaleString();
    },
  },
};
</script>
