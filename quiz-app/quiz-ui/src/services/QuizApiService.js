import axios from "axios";

const instance = axios.create({
    baseURL: `${import.meta.env.VITE_API_URL}`,
    json: true
});

export default {
    async call(method, resource, data = null, token = null) {
        var headers = {
            "Content-Type": "application/json",
        };
        if (token != null) {
            headers.authorization = "Bearer " + token;
        }

        return instance({
            method,
            headers: headers,
            url: resource,
            data,
        })
            .then((response) => {
                return { status: response.status, data: response.data };
            })
            .catch((error) => {
                console.error(error);
            });
    },
    getQuizInfo() {
        return this.call("get", "quiz-info");
    },
    getQuestion(position) {
        return this.call("get", "questions?position=" + position);
    },
    saveParticipation(playerName, answers){
        return this.call("post", "participations", {"playerName": playerName, "answers": answers})
    },
    login(password) {
        console.log("login with password : " + password)
        try {
            return this.call("post", "login", { "password": password });
        }
        catch {
            return ''
        }
    },
    getPlayerScore(playerName){
        return this.call("get", "participations?name=" + playerName)
    },
    addQuestion(token, json) {
        console.log("Add new Question with token : \n" + token + "\n\nJSON :\n" + JSON.stringify(json))
        return this.call("post", "questions", json, token);
    },
    updateQuestion(token, json) {
        console.log("Update Question with token : \n" + token + "\n\nJSON :\n" + JSON.stringify(json))
        return this.call("put", "questions/" + json.id, json, token);
    },
    deleteQuestion(token, q_id) {
        console.log("Delete Question with token : \n" + token + "\n\nID :\n" + q_id)
        return this.call("delete", "questions/" + q_id, null, token);
    },
    deleteAllQuestion(token){
        console.log("Deleting all Questions with token : \n" + token + "\n")
        return this.call("delete", "questions/all", null, token);
    },
    getAllQuestions(token, json) {
        console.log("Getting all questions")
        return this.call("get", "questions/all");
    },
    rebuildDB(token) {
        console.log("Rebuilding database")
        return this.call("post", "rebuild-db", null, token);
    }
};