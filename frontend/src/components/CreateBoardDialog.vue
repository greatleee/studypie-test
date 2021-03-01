<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="400px" persistent>
      <v-card>
        <v-card-title>
          <span class="headline">게시판 생성하기</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-form v-model="isValid">
              <v-text-field
                v-model="name"
                :counter="50"
                :rules="nameRules"
                label="이름*"
                required
              ></v-text-field>
            </v-form>
          </v-container>
          <small>* 표시는 필수 기입</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="$root.$emit('hideCreateBoardDialog')">
            취소
          </v-btn>
          <v-btn :disabled="!isValid" color="blue" @click="onClickSubmit">
            완료
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import gql from "graphql-tag";
export default {
  props: ["dialog"],

  data() {
    return {
      isValid: false,
      name: "",
      nameRules: [
        (v) => !!v || "필수 입력 항목입니다.",
        (v) => (v && v.length <= 50) || "50 글자 이하만 입력가능합니다.",
      ],
    };
  },

  methods: {
    onClickSubmit: async function() {
      let response;
      try {
        response = await this.$apollo.mutate({
          mutation: gql`
            mutation($name: String!) {
              createBoard(name: $name) {
                allBoards {
                  id
                  name
                }
              }
            }
          `,
          variables: {
            name: this.name,
          },
        });
      } catch (error) {
        alert(error);
        return;
      }
      this.$root.$emit("setBoardList", response.data.createBoard.allBoards);
    },
  },
};
</script>
