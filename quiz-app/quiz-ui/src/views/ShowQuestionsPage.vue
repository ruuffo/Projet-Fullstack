<template>
    <br><button @click.prevent="deleteAll">Delete all Questions</button><br><br><br>

    <label>
      <b>List of question:</b>
      <br />
    </label>

    <div class="answer" v-for="question in all_questions">
      <label>
        <img v-if="question.image" :src="question.image" class="question-image" alt="Question image" />
        <br />
        Question {{ question.position }}<br />
        <span class="question-title" :title="question.title">{{ question.title }}</span>
        <br><button @click.prevent="showDetails(question.position)">Details</button>
        <br /><br />
      </label>
    </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorage";
export default {
  name: "showquestions",
  data() {
    return {
      all_questions: []
    };
  },
  async created() {
    console.log("Composant Show questions page 'created'")
    this.loadQuestions()
  },
  methods: {
    addAnswer() {
      this.answers.push(new Answer());
    },
    async deleteAll() {
      var token = await adminStorageService.getToken();
      var response = await quizApiService.deleteAllQuestion(token);
      console.log("Deleted All Questions.\nResponse:\n" + JSON.stringify(response));
      this.loadQuestions()
    },
    showDetails(position) {
      adminStorageService.setQuestionToDetail(position)
      this.$router.push('/questiondetail');
    },
    async loadQuestions(){
      var json = await quizApiService.getAllQuestions()
      this.all_questions = json.data
    }
  },
};

export class Question {
  text = "";
  title = "";
  image = "";
  position = "";
  possibleAnswers = "";

  constructor() {
    this.text = "";
    this.title = "";
    this.image = "";
    this.position = 1;
    this.possibleAnswers = "";
  }

}

export class Answer {
  text = "";
  isCorrect = "";

  constructor() {
    this.text = "";
    this.isCorrect = false;
  }

}
</script>

<style>
.answer:not(:first-child) {
  margin-top: 1rem;
}

.question-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
}

.question-title {
  font-size: 1.2rem;
  font-weight: bold;
}
</style>
