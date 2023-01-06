<template>
    <body>
        <div class="question">
            <h1>{{question.questionTitle}}</h1>
        <img v-if="question.image" :src="question.image"/>
        <h2>{{question.questionText}}</h2>
        <div v-for="answer in question.possibleAnswers">
            <button @click="$emit('answerSelected', question.answer.position)">{{question.answer.text}}</button>
        </div>

        </div>
    </body>
</template>

<script>
export default{
    name: "QuestionDisplay",
    props:{
        question:{
            type: object
        }
    },
    emits: ["answerSelected"]
}
</script>

<style scoped>
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