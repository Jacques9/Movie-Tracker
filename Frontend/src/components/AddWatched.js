import { useEffect, useState } from 'react';

import { TbBookmark, TbBookmarkOff } from 'react-icons/tb';
import Manager from '../ApiManager';
import Loading from './Loading';
const AddWatched = ({ movieId, user, callback, watched }) => {
  const [isWatched, setIsWatched] = useState(watched);
  const [error,setError] = useState(undefined);
  const [loading,setLoading] = useState(false);
  const addWatched = async () => {
    setLoading(true);
    Manager.addMovieToWatched(user,movieId).then((result)=>{
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

  const removeWatched = async () => {
    setLoading(true);
    Manager.removeMovieFromWatched(user,movieId).then((result)=>{
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
    Manager.getWatchedMovies(user).then((result)=>{
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
        <TbBookmarkOff
          size={30}
          className='text-yellow-400'
          onClick={removeWatched}        />
      ) : (
        <TbBookmark
          size={30}
          className='text-yellow-400'
          onClick={addWatched}
        />
      )}
    </>
  );
};

export default AddWatched;
