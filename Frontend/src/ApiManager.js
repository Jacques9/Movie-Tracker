

const baseUrl = "http://localhost:8000/";
const imagesUrl = "https://image.tmdb.org/t/p/original";
const registerUrl = baseUrl + "user/register";
const loginUrl = baseUrl + "user/login";
const getAllMoviesUrl = baseUrl + "movie/all";
const getMovieByIdUrl = (id) => {return baseUrl + "movie/" + id;}
const getFavMoviesUrl = (id) => {return baseUrl + "user/favorites/" + id;}
const modifyFavMoviesUrl = (id,movie) => {return baseUrl + "user/favorites/" + id + "/" + movie;}
const getWatchedMoviesUrl = (id) => {return baseUrl + "user/watched/" + id;}
const modifyWatchedMoviesUrl = (id,movie) => {return baseUrl + "user/watched/" + id + "/" + movie;}
const getWatchingMoviesUrl = (id) => {return baseUrl + "user/watching/" + id;}
const modifyWatchingMoviesUrl = (id,movie) => {return baseUrl + "user/watching/" + id + "/" + movie;}

async function safeFetch(url,options){
    try{
        return await fetch(url,options);
    }catch(e){
        return {ok: false, json:()=>{ return "Connection error"}};
    }
}

async function registerNewUser(username,password,email){
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username, password: password, email: email })
    };
    const response = await safeFetch(registerUrl, requestOptions);
    const data = await response.json();
    return {response: response, data: data.JSON};
}
async function loginUser(email,password){
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: password, email: email })
    };
    const response = await safeFetch(loginUrl, requestOptions);
    const data = await response.json();
    if(response.ok){
        data.id = "JPWmDAIwp4hpxnGlk8D0";
        data.token = data.idToken;
        data.error = data.detail;
    }
    return {response: response, data: data};
}

async function getAllMovies(){
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await safeFetch(getAllMoviesUrl, requestOptions);
    const data = await response.json();
    if(response.ok){
        data.forEach(element => {
            //https://image.tmdb.org/t/p/original/[poster_path]
            //element.id = element.backdrop_path;
            element.poster_path = imagesUrl + element.poster_path; 
        });
    }
    return {response: response, data: data};
}
async function getFavMovies(user){
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await safeFetch(getFavMoviesUrl(user), requestOptions);
    const data = await response.json();
    if(response.ok){
        data.forEach(element => {
            //https://image.tmdb.org/t/p/original/[poster_path]
            //element.id = element.backdrop_path;
            element.poster_path = imagesUrl + element.poster_path; 
        });
    }
    return {response: response, data: data};
}
async function getWatchedMovies(user){
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await safeFetch(getWatchedMoviesUrl(user), requestOptions);
    const data = await response.json();
    if(response.ok){
        data.forEach(element => {
            //https://image.tmdb.org/t/p/original/[poster_path]
            //element.id = element.backdrop_path;
            element.poster_path = imagesUrl + element.poster_path; 
        });
    }
    return {response: response, data: data};
}
async function getWatchingMovies(user){
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await safeFetch(getWatchingMoviesUrl(user), requestOptions);
    const data = await response.json();
    if(response.ok){
        data.forEach(element => {
            //https://image.tmdb.org/t/p/original/[poster_path]
            //element.id = element.backdrop_path;
            element.poster_path = imagesUrl + element.poster_path; 
        });
    }
    return {response: response, data: data};
}
async function getMovieById(id){
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await safeFetch(getMovieByIdUrl(id), requestOptions);
    const data = await response.json();
    if(response.ok){
        data.poster_path = imagesUrl + data.poster_path; 
    }
    return {response: response, data: data};
}

async function addMovieToFav(user,movie){
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await safeFetch(modifyFavMoviesUrl(user,movie), requestOptions);
    const data = await response.json();
    return {response: response, data: data};
}
async function removeMovieFromFav(user,movie){
    const requestOptions = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await safeFetch(modifyFavMoviesUrl(user,movie), requestOptions);
    const data = await response.json();
    return {response: response, data: data};
}
async function addMovieToWatched(user,movie){
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await safeFetch(modifyWatchedMoviesUrl(user,movie), requestOptions);
    const data = await response.json();
    return {response: response, data: data};
}
async function removeMovieFromWatched(user,movie){
    const requestOptions = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await safeFetch(modifyWatchedMoviesUrl(user,movie), requestOptions);
    const data = await response.json();
    return {response: response, data: data};
}
async function addMovieToWatching(user,movie){
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await safeFetch(modifyWatchingMoviesUrl(user,movie), requestOptions);
    const data = await response.json();
    return {response: response, data: data};
}
async function removeMovieFromWatching(user,movie){
    const requestOptions = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await safeFetch(modifyWatchingMoviesUrl(user,movie), requestOptions);
    const data = await response.json();
    return {response: response, data: data};
}
const Manager = {
    registerNewUser, 
    loginUser,
    getAllMovies,
    getMovieById,
    addMovieToFav,
    removeMovieFromFav,
    getFavMovies,
    getWatchedMovies,
    getWatchingMovies,
    addMovieToWatched,
    removeMovieFromWatched,
    addMovieToWatching,
    removeMovieFromWatching,
}
export default Manager;