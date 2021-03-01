import gql from "graphql-tag";
import { apolloClient } from "../vue-apollo";

async function getCSRFToken() {
  try {
    await fetch("http://localhost:8000/csrf/", {
      method: "GET",
      credentials: "include",
    });
    return true;
  } catch (error) {
    return false;
  }
}

async function login(username, password) {
  const body = {
    username: username,
    password: password,
  };
  const csrftoken = getCookie("csrftoken");
  return await fetch("http://localhost:8000/login/", {
    method: "POST",
    credentials: "include",
    headers: {
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify(body),
  });
}

async function logout() {
  try {
    const csrftoken = getCookie("csrftoken");
    await fetch("http://localhost:8000/logout/", {
      method: "POST",
      credentials: "include",
      headers: {
        "X-CSRFTOKEN": csrftoken,
      },
    });
  } catch (error) {
    return false;
  }
  return true;
}

async function loggedIn() {
  try {
    await apolloClient.query({
      query: gql(`
        query {
          curUserInfo {
            username
          }
        }
      `),
    });
    return true;
  } catch (error) {
    return false;
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export default {
  getCSRFToken,
  login,
  logout,
  loggedIn,
  getCookie,
};
