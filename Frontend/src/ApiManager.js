

const baseUrl = "http://localhost:8000/";
const imagesUrl = "https://image.tmdb.org/t/p/original";
const registerUrl = baseUrl + "user/register";
const loginUrl = baseUrl + "user/login";
const getAllMoviesUrl = baseUrl + "movie/all";
const getMovieByIdUrl = (id) => {return baseUrl + "movie/" + id;}
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
    data.token = data.idToken;
    data.error = data.detail;
    return {response: response, data: data};
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
        //element.id = element.backdrop_path;
        element.poster_path = imagesUrl + element.poster_path; 
    });
    return {response: response, data: data};
}
async function getMovieById(id){
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    };
    console.log(getMovieByIdUrl(id));
    const response = await fetch(getMovieByIdUrl(id), requestOptions);
    const data = await response.json();
    data.poster_path = imagesUrl + data.poster_path; 
    return {response: response, data: data};
}
const Manager = {
    registerNewUser, 
    loginUser,
    getAllMovies,
    getMovieById,
}
export default Manager;