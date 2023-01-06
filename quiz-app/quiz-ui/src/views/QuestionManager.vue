<template>
    <div class="question">
        <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
        <QuestionDisplay :question="currentQuestion" @answerSelected="answerClickedHandler" />
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
                questionImage: '',
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
            var json = await quizApiService.getQuestion(position)
            this.currentQuestion.questionTitle = json.data.questionTitle
            this.currentQuestion.questionText = json.data.text
            this.currentQuestion.questionImage = json.data.image
            this.currentQuestion.possibleAnswers = json.data.possibleAnswers
        },
        async answerClickedHandler(answerSelected){
            this.answers[this.currentQuestionPosition-1] = answerSelected
            if(this.currentQuestionPosition >= this.totalNumberOfQuestion)
                this.endQuiz()
            else{
                this.currentQuestionPosition++
                this.loadQuestionByPosition(this.currentQuestionPosition)
            }
        },
        async endQuiz(){
            var playerName = participationStorageService.getPlayerName()
            await quizApiService.saveParticipation(playerName, this.answers)
            participationStorageService.saveParticipationScore(this.score)
            this.$router.push('/');
        }
    },
    async created() {
		console.log("Composant QuestionManager 'created'")
        this.loadQuestionByPosition(this.currentQuestionPosition)
        var json = await quizApiService.getQuizInfo()
        this.totalNumberOfQuestion = json.data.size
    }
}

</script>

<style scoped>
@media (min-width: 1024px) {
    .about {
        min-height: 100vh;
        display: flex;
        align-items: center;
    }
}

body {
    background-color: powderblue;
}

h1 {
    color: blue;
    text-align: center;
}

.container {
    text-align: center;
}

h2 {
    color: darkgreen;
    text-align: center;
}

div {
    text-align: center;
}

p {
    color: red;
}
</style>