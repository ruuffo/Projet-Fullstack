<template>

    <div style="text-align: center">
      <button @click.prevent="goBack">Back</button><br><br>
      <button @click.prevent="deleteAll">Delete all Questions</button><br><br><br>

    </div>

    <table style="text-align: center">
      <tr>
        <label>
          <h2><b>List of {{ totalNumberOfQuestion }} question:</b></h2>
          <br><br><br>
        </label>
      </tr>
      <tr>
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
      </tr>
    </table>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorage";
export default {
  name: "showquestions",
  data() {
    return {
      all_questions: [],
      totalNumberOfQuestion: 1
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
    goBack() {
      this.$router.push('/admintools');
    },
    async deleteAll() {
      if(confirm("Do you really want to delete ALL questions ?"))
      {
        var token = await adminStorageService.getToken();
        var response = await quizApiService.deleteAllQuestion(token);
        console.log("Deleted All Questions.\nResponse:\n" + JSON.stringify(response));
        this.loadQuestions()
      }
    },
    showDetails(position) {
      adminStorageService.setQuestionToDetail(position)
      this.$router.push('/questiondetail');
    },
    async loadQuestions() {
      var json = await quizApiService.getQuizInfo()
      this.totalNumberOfQuestion = json.data.size
      json = await quizApiService.getAllQuestions()
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
