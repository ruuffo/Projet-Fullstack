<template>
    <div class="question">
        <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
        <QuestionDisplay :question="currentQuestion" @click-on-answer="answerClickedHandler" />
    </div>
</template>
  
<script>
import participationStorageService from "@/services/ParticipationStorageService";
import quizApiService from "@/services/QuizApiService";
import QuestionDisplay from "@/views/QuestionDisplay.vue";
export default{
    name: "QuestionManager",
    data(){
        return{
            currentQuestion: {
                questionTitle: '',
                questionText: '',
                possibleAnswers: [],
            },
            currentQuestionPosition: 1,
            totalNumberOfQuestion: 1,
            score: 1,
            answers: []
        }
    },
    components:{
        QuestionDisplay
    },
    methods:{
        async loadQuestionByPosition(position){
            currentQuestionPosition++
            var json = await quizApiService.getQuestion(position)

        },
        async answerClickedHandler(answerSelected){
            answers[currentQuestionPosition] = answerSelected
            if(currentQuestionPosition == totalNumberOfQuestion)
                endQuiz()
            else{

            }
        },
        async endQuiz(){
            await quizApiService.saveParticipation(this.answers)
            participationStorageService.saveParticipationScore(score)
        }
    },
    async created() {
		console.log("Composant QuestionManager 'created'")
        var json = await quizApiService.getQuestion(currentQuestionPosition)
        this.currentQuestion = json.data.question
        this.totalNumberOfQuestion = json.data.totalNumberOfQuestion
  }
}

</script>

<style>
  @media (min-width: 1024px) {
    .about {
      min-height: 100vh;
      display: flex;
      align-items: center;
    }
  }
</style>