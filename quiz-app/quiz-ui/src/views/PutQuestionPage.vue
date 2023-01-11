<template>
    <table style="text-align:center">
        <button @click.prevent="goBack">Back</button><br><br>
        <div v-if="question != null">
            <label>
                <h2>Question:</h2>
                Text: <input type="text" v-model="question.text" /><br />
                Title: <input type="text" v-model="question.title" /><br />
                Image: <input type="text" v-model="question.image" /><br />
                Position: <input type="number" min="1" oninput="validity.valid||(value='')" v-model="question.position" /><br />
            </label>
            <br />
            <div class="answer" v-for="(answer, index) in answers" :key="index">
                <label>
                    <h3>Réponse {{ index + 1 }}:</h3>
                    Text: <input type="text" v-model="answer.text" /><br />
                    Cocher si réponse est correcte: <input type="checkbox" id="checkbox" v-model="answer.isCorrect">
                    <p> </p>
                    <button v-if="index > 0" @click.prevent="removeAnswer(index)">Supprimer Réponse {{ index + 1}}</button>
                </label>
            </div>
            <br />
            <tr><button @click.prevent="addAnswer">Ajouter une réponse</button></tr>
            <tr><button @click.prevent="submitQuestion">Envoyer</button></tr>
        </div>
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
    name: "putquestion",
    data() {
        return {
            question: new Question(),
            answers: []
        };
    },
    async created() {
        console.log("Composant Put Question Page 'created'")
        var position = adminStorageService.getQuestionToDetail();
        await this.loadQuestionByPosition(position)
        console.log("Question loaded")
        //this.$forceUpdate()
    },
    methods: {
        async loadQuestionByPosition(position) {
            var json = await quizApiService.getQuestion(position)
            this.question.position = position
            this.question.title = json.data.title
            this.question.text = json.data.text
            this.question.image = json.data.image
            this.question.id = json.data.id

            for(var a in json.data.possibleAnswers){
                this.answers.push(new Answer(a.text, a.isCorrect))
            }
        },
        goBack() {
            this.$router.push('/questiondetail');
        },
        addAnswer() {
            this.answers.push(new Answer(null,null));
        },
        removeAnswer(index) {
            this.answers.splice(index, 1);
        },
        async submitQuestion() {
            if (confirm("Submit this question ?")) {
                this.question.possibleAnswers = this.answers;

                var token = await adminStorageService.getToken();

                var response = await quizApiService.updateQuestion(token, this.question);
                console.log("Update a question with JSON :\n" + JSON.stringify(this.question) + "\n\nResponse:\n" + JSON.stringify(response));

                this.$router.push('/showquestions');
            }
        },
    },
};

export class Question {
    id = "";
    text = "";
    title = "";
    image = "";
    position = "";
    possibleAnswers = "";

    constructor(id, tx, ti, im, po, pa) {
        this.text = id;
        this.text = tx;
        this.title = ti;
        this.image = im;
        this.position = po;
        this.possibleAnswers = [];
    }

}

export class Answer {
    text = "";
    isCorrect = "";

    constructor(te, ic) {
        if (te == null) this.text = "";
        else this.text = te;

        if(ic == null) this.isCorrect = false;
        else this.isCorrect = ic;
    }

}
</script>
