<template>
  <form @submit="submitForm">
    <label>
      List of question:
      <br />
    </label>

    <div class="answer" v-for="question in all_questions">
      <label>
        {{ question.image }}<br />
        Question {{ question.position }}<br />
        {{ question.title }}<br />

        <br/><br />
      </label>
    </div>
  </form>
</template>

<style>
.answer:not(:first-child) {
  margin-top: 1rem;
}
</style>

<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorage";
export default {
  name:"showquestions",
  data() {
    return {
      all_questions : []
    };
  },
  async created() {
    console.log("Composant Show questions page 'created'")
    var json = await quizApiService.getAllQuestions()
    this.all_questions = json.data
  },
  methods: {
    addAnswer() {
      this.answers.push(new Answer());
    },
    removeAnswer(index) {
      this.answers.splice(index, 1);
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
