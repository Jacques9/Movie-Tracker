import React from 'react';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import AddFavorite from '../components/AddFavorite';
import Card from '../components/Card';
import Manager from '../ApiManager';
import Loading from '../components/Loading';
import AddWatched from '../components/AddWatched';
var watched = [];
const Watched = ({ user }) => {
  const [loading, setLoading] = useState(watched===[]);
  const [error, setError] = useState(null);
  const [refresh, setRefresh] = useState(true);
  if(refresh)
  {
    setLoading(true);
    Manager.getWatchedMovies(user).then(
    (m)=>{
      if(m.response.ok){
        watched = m.data;
      }else{
        setError(m.data);
      }
      setLoading(false);
    });
    setRefresh(false);
  }
  if (loading || error){
    return <div className='flex items-center justify-center w-full'>
      <p>{error}</p>
    <Loading size={'30px'} />
  </div>;
  }
  return (
    <section className='flex flex-col items-center justify-start gap-10 py-16 sectionHeight lg:py-32'>
      <h1 className='mb-2 text-3xl font-bold sm:text-4xl xl:text-5xl'>
        <span className='text-yellow-400 border-b-4 border-black '>
          Watched
        </span>
      </h1>
      <div className='grid items-start grid-flow-row grid-cols-1 gap-8 py-8 justify-items-center sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4'>
        {watched &&
          watched.length > 0 &&
          watched?.map((movie) => (
            <div className='relative ' key={movie.id}>
              <Link to={`/details/${movie.id}`} className='flex items-center '>
              <Card
                image={movie.poster_path}
                title={movie.title}
                genre={movie.genre_names}
                rating={movie.vote_average}
              />
              </Link>
              <div className='absolute top-0 left-0 p-2 bg-[rgba(0,0,0,0.7)] cursor-pointer'>
                <AddFavorite movieId={movie.id} user={user} callback={()=>setRefresh(true)} />
                <AddWatched movieId={movie.id} user={user} callback={()=>setRefresh(true)} watched={true} />
              </div>
            </div>
          ))}
      </div>

      {watched && watched.length === 0 && (
        <p className='italic text-gray-400'>No favorites added</p>
      )}
    </section>
  );
};

export default Watched;
