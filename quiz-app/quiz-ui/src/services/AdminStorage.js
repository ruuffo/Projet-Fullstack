export default {
    clear() {
          window.localStorage.clear();
    },
      saveToken(token) {
            window.localStorage.setItem("token", token);
    },
    clearToken(){
      window.localStorage.setItem("token",'');
    },
    getToken() {
          var token = window.localStorage.getItem("token");
          if (token == undefined || token == null)
            token = "";
          return token;
    }
  };