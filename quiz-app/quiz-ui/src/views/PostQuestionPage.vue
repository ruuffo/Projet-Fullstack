<template>
  <form @submit="submitForm">
    <label>
      Question:
      <input type="text" v-model="question" />
    </label>
    <br />
    <div class="answer" v-for="(answer, index) in answers" :key="index">
      <label>
        Réponse {{ index + 1 }}:
        <input type="text" v-model="answer.text" />
        <button v-if="index > 0" @click.prevent="removeAnswer(index)">Supprimer</button>
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
export default {
  data() {
    return {
      question: '',
      answers: [{ text: '' }],
    };
  },
  methods: {
    addAnswer() {
      this.answers.push({ text: '' });
    },
    removeAnswer(index) {
      this.answers.splice(index, 1);
    },
    async submitForm() {
      const data = {
        question: this.question,
        answers: this.answers,
      };
      const response = await axios.post('/api/questions', data);
      console.log(response);
    },
  },
};
</script>
