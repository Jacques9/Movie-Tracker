import React, { useEffect, useState } from 'react';
import Loading from '../components/Loading';
import Card from '../components/Card';
import Manager from '../ApiManager';

const NewReview = ({ user }) => {
  const [loading, setLoading] = useState(true);
  const [movies, setMovies] = useState(undefined);
  const [target,setTarget] = useState(undefined);
  const [error, setError] = useState(undefined);
  const [description, setDescription] = useState(undefined);
  const [rating, setRating] = useState(undefined);
  const handleSubmit = ()=>{
    setLoading(true);
    Manager.addReview(user,target,rating,description).then(
      (m)=>{
        if(m.response.ok){
          setTarget(undefined);
        }else{
          setError(m.data);
        }
        setLoading(false);
      });
  };
  useEffect(()=>{
    if(movies===undefined || movies === []){
      Manager.getAllMovies().then(
        (m)=>{
          if(m.response.ok){
            setMovies(m.data);
          }else{
            setError(m.data);
          }
          setLoading(false);
        });
    }
  },[movies]);
  
  if (loading || error){
    return <div className='flex items-center justify-center w-full'>
      <p>{error}</p>
    <Loading size={'30px'} />
  </div>;
  }

  return (
    <section className='flex flex-col items-center justify-center bg-amber-200 sectionHeight'>
      <h1 className='my-8 sm:text-xl md:text-2xl font-bold text-zinc-800 w-[90%] text-center '>
        Add a new review
      </h1>
      <div>
      {target!==undefined && (<Card
        image={target.poster_path}
        title={target.title}
        genre={target.genre_names}
        rating={target.vote_average}
      />)}
      <select
          className={`p-4  rounded-md shadow-md outline-none bg-slate-50 `}
          //value={target ? target.title : "" }
          onChange={(e) => setTarget(movies.find(m=>m.id===e.value))}
        >
          <option value='' className='disabled:text-gray-500' disabled>
            Movie
          </option>
          {movies.map((movie) => (
            <option key={movie.id} value={movie.id}>
              {movie.title}
            </option>
          ))}
        </select>
        </div>
      {target && (
        <div><img
          src={target.poster_path}
          alt='preview'
          className='max-w-[600px] w-[90%] object-cover mb-8 shadow-md rounded-md' />
          <form
            onSubmit={handleSubmit}
            className='flex flex-col max-w-[600px] w-[90%] mx-auto gap-3 mb-16'
          >
            <input
              type='number'
              placeholder='Rating (0 - 5)'
              className='p-4 rounded-md shadow-md outline-none bg-slate-50'
              min={0}
              max={5}
              value={rating || ''}
              onChange={(e) => setRating(e.target.value)} />
            <textarea
              type='text'
              placeholder='Description'
              className='p-4 rounded-md shadow-md outline-none resize-none bg-slate-50 h-[200px]'
              value={description || ''}
              onChange={(e) => setDescription(e.target.value)} />
            <input
              type='submit'
              value={'Upload Review'}
              className='w-full p-4 font-bold text-white transition-all duration-300 rounded-md shadow-sm cursor-pointer bg-zinc-800 hover:bg-zinc-700 hover:tracking-wider' />
          </form></div>
      )}
    </section>
  );
};

export default NewReview;
