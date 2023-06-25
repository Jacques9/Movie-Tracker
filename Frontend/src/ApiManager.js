

const baseUrl = "http://localhost:8000/";
const registerUrl = baseUrl + "user/register";
const loginUrl = baseUrl + "user/login";

async function registerNewUser(username,password,email){
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username, password: password, email: email })
    };
    console.log(requestOptions.body);
    const response = await fetch(registerUrl, requestOptions);
    const data = await response.json();
    return {response: response, data: data.JSON};
}
async function loginUser(email,password){
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: password, email: email })
    };
    console.log(requestOptions.body);
    const response = await fetch(loginUrl, requestOptions);
    const data = await response.json();
    return {response: response, data: data.JSON};
}

const Manager = {
    registerNewUser, 
    loginUser
}
export default Manager;