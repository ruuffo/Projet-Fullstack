<template>
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
            <br />
            Text: <input type="text" v-model="answer.text" /><br />
            Coche si réponse est correcte: <input type="checkbox" id="checkbox" v-model="answer.isCorrect">
            <p> </p>
            <button v-if="index > 0" @click.prevent="removeAnswer(index)">Supprimer Réponse {{ index + 1}}</button>
        </label>
    </div>
    <br />
    <button @click.prevent="addAnswer">Ajouter une réponse</button>
    <button @click.prevent="submitQuestion">Envoyer</button>
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
            question: null,
            answers: []
        };
    },
    async create() {
        var position = adminStorageService.getQuestionToDetail();
        var q = await quizApiService.getQuestion(position)
        this.question = new Question(q.id, q.text, q.title, q.image, q.position, q.answers)
        console.log("Question : " + this.question.text)
    },
    methods: {
        addAnswer() {
            this.answers.push(new Answer(null,null));
        },
        removeAnswer(index) {
            this.answers.splice(index, 1);
        },
        async submitQuestion() {

            this.question.possibleAnswers = this.answers;

            var token = await adminStorageService.getToken();

            var response = await quizApiService.updateQuestion(token, this.question);
            console.log("Update a question with JSON :\n" + JSON.stringify(this.question) + "\n\nResponse:\n" + JSON.stringify(response));

            this.$router.push('/showquestions');

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
        for (var a in pa) {
            this.possibleAnswers.push(new Answer(a.text, a.isCorrect));
        }
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
