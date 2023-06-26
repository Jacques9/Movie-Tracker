

const baseUrl = "http://localhost:8000/";
const registerUrl = baseUrl + "user/register";
const loginUrl = baseUrl + "user/login";
const getAllMoviesUrl = baseUrl + "movie/all";

async function registerNewUser(username,password,email){
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username, password: password, email: email })
    };
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
    const response = await fetch(loginUrl, requestOptions);
    const data = await response.json();
    return {response: response, data: data.idToken};
}

async function getAllMovies(){
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await fetch(getAllMoviesUrl, requestOptions);
    const data = await response.json();
    data.forEach(element => {
        //https://image.tmdb.org/t/p/original/[poster_path]
        element.id = element.backdrop_path;
        element.poster_path = "https://image.tmdb.org/t/p/original" + element.poster_path; 
    });
    return {response: response, data: data};
}

const Manager = {
    registerNewUser, 
    loginUser,
    getAllMovies
}
export default Manager;