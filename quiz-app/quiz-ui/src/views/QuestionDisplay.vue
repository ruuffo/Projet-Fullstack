<template>
        <div class="question">
            <h1>{{ question.questionTitle }}</h1>
            <img class="img-thumbnail" v-if="question.questionImage" :src="question.questionImage" />
            <h2>{{ question.questionText }}</h2>
            <div class="d-flex flex-column gap-3">
                <div v-for="answer in question.possibleAnswers">
                    <button @click="$emit('answerSelected', answer.position)">{{ answer.text }}</button>
                </div>
            </div>
        </div>
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
