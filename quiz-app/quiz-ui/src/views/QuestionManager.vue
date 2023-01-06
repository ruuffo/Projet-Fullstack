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
            participationStorageService.saveParticipationScore(this.score)
        }
    },
    async created() {
		console.log("Composant QuestionManager 'created'")
        var json = await quizApiService.getQuestion(this.currentQuestionPosition)
        console.log(json)
        this.currentQuestion.questionTitle = json.data.questionTitle
        this.currentQuestion.questionText = json.data.text
        this.currentQuestion.questionImage = json.data.image
        this.currentQuestion.possibleAnswers = json.data.possibleAnswers
        json = await quizApiService.getQuizInfo()
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