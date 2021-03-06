export default {
  methods: {
    formatDate: function(datetime) {
      return new Date(datetime).toLocaleString();
    },
    getHumanReadablePointAction: function(action) {
      let text = "알 수 없는 행동";
      switch (action) {
        case "A_0":
          text = "회원가입";
          break;
        case "A_1":
          text = "게시글 작성";
          break;
        case "A_2":
          text = "댓글 작성";
          break;
      }
      return text;
    },
  },
};
