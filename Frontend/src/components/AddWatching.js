import { useEffect, useState } from 'react';

import { TbEye, TbEyeOff } from 'react-icons/tb';
import Manager from '../ApiManager';
import Loading from './Loading';
const AddWatching = ({ movieId, user, callback, watching }) => {
  const [isWatched, setIsWatched] = useState(watching);
  const [error,setError] = useState(undefined);
  const [loading,setLoading] = useState(false);
  const addWatching = async () => {
    setLoading(true);
    Manager.addMovieToWatching(user,movieId).then((result)=>{
      if(result.response.ok){
        setError(undefined);
        setIsWatched(true);
        if(callback)callback();
      }else{
        setError(result.response.statusText);
      }
      setLoading(false)
    });
  };

  const removeWatching = async () => {
    setLoading(true);
    Manager.removeMovieFromWatching(user,movieId).then((result)=>{
      if(result.response.ok){
        setError(undefined);
        setIsWatched(false);
        if(callback)callback();
      }else{
        setError(result.response.statusText);
      }
      setLoading(false)
    });
  };
  if(isWatched === undefined && loading===false){
    setLoading(true);
    Manager.getWatchingMovies(user).then((result)=>{
      if(result.response.ok){
        let ok = false;
        result.data?.forEach(element => {
          if(element.id===movieId){
            ok=true;
          }
        });
        setIsWatched(ok);
      }else{
        setIsWatched("error");
        setError(result.response.statusText);
      }
      setLoading(false);
    });
  }

  if(error){
    return <p>{error}</p>;
  }
  if (loading){
    return <div className='flex items-center justify-center w-full'>
    <Loading size={'20px'} />
  </div>;
  }
  
  return (
    <>
      {isWatched ? (
        <TbEyeOff
          size={30}
          className='text-yellow-400'
          onClick={removeWatching}        />
      ) : (
        <TbEye
          size={30}
          className='text-yellow-400'
          onClick={addWatching}
        />
      )}
    </>
  );
};

export default AddWatching;
