<template>
    <table style="text-align:center">
      <button @click.prevent="goBack">Back</button><br><br>
      <label>
        <h2>Question:</h2>
        <br />
        Text: <input type="text" v-model="question.text" /><br />
        Title: <input type="text" v-model="question.title" /><br />
        Image: <input type="text" v-model="question.image" /><br />
        Position: <input type="number" min="1" oninput="validity.valid||(value='')" v-model="question.position" /><br />
      </label>
      <br />
      <div class="answer" v-for="(answer, index) in answers" :key="index">
        <label>
          <h3>Réponse {{ index + 1 }}:</h3>
          <br/>
          Text: <input type="text" v-model="answer.text" /><br />
          Coche si réponse est correcte: <input type="checkbox" id="checkbox" v-model="answer.isCorrect">
          <p>     </p>
          <button v-if="index > 0" @click.prevent="removeAnswer(index)">Supprimer Réponse {{ index + 1}}</button>
        </label>
      </div>
      <br />
      <tr><button @click.prevent="addAnswer">Ajouter une réponse</button></tr>
      <tr><button @click.prevent="submitQuestion">Envoyer</button></tr>
    </table>
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
  name:"postquestion",
  data() {
    return {
      question: new Question(),
      answers: [new Answer()],
    };
  },
  methods: {
    addAnswer() {
      this.answers.push(new Answer());
    },
    goBack() {
      this.$router.push('/admintools');
    },
    removeAnswer(index) {
      this.answers.splice(index, 1);
    },
    async submitQuestion() {
      if (confirm("Submit this question ?")) {
        this.question.possibleAnswers = this.answers;

        var token = await adminStorageService.getToken();

        var response = await quizApiService.addQuestion(token, this.question);
        console.log("Posting a new question with JSON :\n" + JSON.stringify(this.question) + "\n\nResponse:\n" + JSON.stringify(response));

        this.$router.push('/adminTools');
      }

    },
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
