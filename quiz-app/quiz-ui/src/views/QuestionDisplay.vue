<template>

    <body>
        <div class="question">
            <h1>{{ question.questionTitle }}</h1>
            <img v-if="question.image" :src="question.questionImage" />
            <h2>{{ question.questionText }}</h2>
            <div v-for="answer in question.possibleAnswers">
                <button @click="$emit('answerSelected', answer.position)">{{ answer.text }}</button>
            </div>

        </div>
    </body>
</template>

<script>
export default {
    name: "QuestionDisplay",
    props: {
        question: {
            type: Object
        }
    },
    emits: ["answerSelected"]
}
</script>
