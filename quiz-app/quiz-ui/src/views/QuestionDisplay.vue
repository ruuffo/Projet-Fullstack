<template>
    <div class="question">
        <h1>{{question.questionTitle}}</h1>
      <img v-if="question.image" :src="question.image"/>
      <h2>{{question.questionText}}</h2>
      <div v-for="answer in question.possibleAnswers">
        <button @click="$emit('answerSelected', question.answer.position)">{{question.answer.text}}</button>
      </div>
        
    </div>
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