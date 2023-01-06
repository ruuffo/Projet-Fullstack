<template>
  <form @submit="submitForm">
    <label>
      Question:
      <br />
      Text: <input type="text" v-model="question.text" /><br />
      Title: <input type="text" v-model="question.title" /><br />
      Image: <input type="text" v-model="question.image" /><br />
      Position: <input type="number" min="1" oninput="validity.valid||(value='')" v-model="question.position" /><br />
    </label>
    <br />
    <div class="answer" v-for="(answer, index) in answers" :key="index">
      <label>
        Réponse {{ index + 1 }}:
        <br/>
        Text: <input type="text" v-model="answer.text" /><br />
        Coche si réponse est correcte: <input type="checkbox" id="checkbox" v-model="answer.isCorrect">
        <p>     </p>
        <button v-if="index > 0" @click.prevent="removeAnswer(index)">Supprimer Réponse {{ index + 1}}</button>
      </label>
    </div>
    <br />
    <button @click.prevent="addAnswer">Ajouter une réponse</button>
    <button type="submit">Envoyer</button>
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
    removeAnswer(index) {
      this.answers.splice(index, 1);
    },
    async submitForm() {

      this.question.possibleAnswers = this.answers;

      // var test = {
      //   "text": "test",
      //   "title": "test",
      //   "image": "test",
      //   "position": 12,
      //   "possibleAnswers":[]
      // }

      var token = await adminStorageService.getToken();
7
      var response = await quizApiService.addQuestion(token, this.question);
      console.log("Posting a new question with JSON :\n" + JSON.stringify(this.question) + "\n\nResponse:\n" + JSON.stringify(response));

      this.$router.push('/adminTools');

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
