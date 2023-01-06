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
export default {
    name: "QuestionManager",
    data() {
        return {
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
    components: {
        QuestionDisplay
    },
    methods: {
        async loadQuestionByPosition(position) {
            var json = await quizApiService.getQuestion(position)
            this.currentQuestion.questionTitle = json.data.questionTitle
            this.currentQuestion.questionText = json.data.text
            this.currentQuestion.questionImage = json.data.image
            this.currentQuestion.possibleAnswers = json.data.possibleAnswers
        },
        async answerClickedHandler(answerSelected) {
            this.answers[this.currentQuestionPosition - 1] = answerSelected
            if (this.currentQuestionPosition >= this.totalNumberOfQuestion)
                this.endQuiz()
            else {
                this.currentQuestionPosition++
                this.loadQuestionByPosition(this.currentQuestionPosition)
            }
        },
        async endQuiz() {
            var playerName = participationStorageService.getPlayerName()
            await quizApiService.saveParticipation(playerName, this.answers)
            await quizApiService.getPlayerScore(playerName)
            participationStorageService.saveParticipationScore(this.score)
            this.$router.push('/score');
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
