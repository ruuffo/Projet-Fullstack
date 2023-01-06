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
        return this.call("post", "participations", JSON.stringify({"playerName": playerName, "answers": answers}))
    },
    login(password) {
        console.log("login with password : " + password)
        try {
            return this.call("post", "login", JSON.stringify({ "password": password }));
        }
        catch {
            return ''
        }
    },
    addQuestion(token, json) {
        console.log("Add new Question with token : " + token + "\nJSON :\n" + JSON.stringify(json))
        return this.call("post", "questions", JSON.stringify(json), token);
    },
    getPlayerScore(playerName){
        return this.call("get", "participation?name=" + playerName)
    }
};