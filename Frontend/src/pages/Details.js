import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

// Icons
import { AiFillStar, AiOutlineStar } from 'react-icons/ai';

// Components
import Comments from '../components/Comments';
import AddFavorite from '../components/AddFavorite';
import Manager from '../ApiManager';
import Loading from '../components/Loading';
import { useNavigate } from "react-router-dom";
import AddWatched from '../components/AddWatched';
import AddWatching from '../components/AddWatching';


const Details = ({ user }) => {
  const { id } = useParams();
  const [loading,setLoading] = useState(true);
  const [stars, setStars] = useState([]);
  const [movie, setMovie] = useState(undefined);
  const navigate = useNavigate();
  const setRatingStars = (size) => {
    const arr = [];
    for (let i = 1; i < size / 2; i++) {
      arr.push(i);
    }
    if(!Number.isInteger(size))arr.push(0.5);
    while(arr.length<5)arr.push(-arr.length);
    return arr;
  };
  if (!movie) 
    Manager.getMovieById(id).then((result)=>{
      if(result.response.ok){
        setLoading(false);
        var temp = "";
        result.data.genre_names.forEach(element => {
          temp+= element + ", ";
        });
        result.data.genre = temp.slice(0,-2);
        result.data.id=id;
        setMovie(result.data);
      }else{
        navigate("/");
      }
      
    });
    
  useEffect(() => {
    if (movie) {
      setStars(setRatingStars(movie?.vote_average));
    }
  }, [movie]);


  if (loading){
    return <div className='flex items-center justify-center w-full'>
    <Loading size={'30px'} />
  </div>;
  }

  return (
    <section className='flex items-center justify-center py-4 sectionHeight lg:py-8'>
      <div className='m-auto max-w-[1200px] w-[90%] '>
        <div className='relative flex flex-col gap-10 lg:flex-row'>
          <img
            src={movie.poster_path}
            alt='poster'
            className='object-cover lg:w-[500px] lg:h-[700px] max-h-[500px] md:max-h-[700px]'
          />
          {user && (
            <div className='absolute top-0 left-0 p-2 bg-[rgba(0,0,0,0.7)]  cursor-pointer'>
              <AddFavorite movieId={id} user={user} />
              <AddWatched movieId={id} user={user} />
              <AddWatching movieId={id} user={user} />
            </div>
            
          )}

          <div className='flex flex-col gap-4'>
            <h1 className='w-full text-3xl lg:text-6xl font-bold lg:mt-[-10px]'>
              {movie.title}
            </h1>
            <div className='flex items-center justify-between'>
              <div className='flex items-center'>
                {stars.map((e)  => {
              if(e<0)
                return <AiOutlineStar key={e} className='text-yellow-400' />;
              else if(e === 0.5){
                return <AiFillStar key={e} className='text-yellow-400' style={{width: "10px", overflow:"hidden"}}/>;
              }else
                return <AiFillStar key={e} className='text-yellow-400' />;
            })}
            </div>
            
              <div className='flex items-center gap-4'>
                {/* <AddToFavorits data={movieData} movieId={id} /> */}
                <span className='text-black-400'>
                  Score: {movie?.vote_average/2}. Total Votes: {movie?.vote_count}
                </span>
              </div>
            </div>
            <div>
            <span className='text-xl italic text-gray-500'> {movie.genre}</span>
            </div>
            <p className='text-justify lg:text-xl'>{movie.overview}</p>
          </div>
        </div>
            
        { <Comments movie={movie} user={user} />}
        
      </div>
    </section>
  );
};

export default Details;
