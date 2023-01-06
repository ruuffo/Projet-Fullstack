<template>
        Question n°{{question.questionPosition}}:
        <br>
        <p> {{question.questionTitle}} </p>
        <p> {{question.questionText}} </p>
        <img v-if="question.questionImage" :src="question.questionImage" />
      <br>
      <div v-for="answer in question.possibleAnswers">
        <p>{{ answer.text }}</p>
      </div>
      <br>
  </template>

<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorage";
export default {
  name:"questiondetail",
  data() {
        return {
            question: {
                questionTitle: '',
                questionText: '',
                questionImage: '',
                possibleAnswers: [],
                questionPosition: 1
            }
        }
    },
  methods: {
    async loadQuestionByPosition(position) {
            var json = await quizApiService.getQuestion(position)
            this.question.questionPosition = position
            this.question.questionTitle = json.data.questionTitle
            this.question.questionText = json.data.text
            this.question.questionImage = json.data.image
            this.question.possibleAnswers = json.data.possibleAnswers
        },
  },
  async created() {
        console.log("Composant QuestionDetail 'created'")
        var position = adminStorageService.getQuestionToDetail()
        this.loadQuestionByPosition(position)
    }
};
</script>