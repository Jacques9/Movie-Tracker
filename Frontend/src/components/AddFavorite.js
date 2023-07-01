import { useEffect, useState } from 'react';

import { TbHeartPlus, TbHeartMinus } from 'react-icons/tb';
import Manager from '../ApiManager';
import Loading from '../components/Loading';
const AddFavorite = ({ movieId, user, callback, favorite }) => {
  const [isFavorite, setIsFavorite] = useState(favorite);
  const [error,setError] = useState(undefined);
  const [loading,setLoading] = useState(false);
  const addFavorite = async () => {
    setLoading(true);
    Manager.addMovieToFav(user,movieId).then((result)=>{
      if(result.response.ok){
        setError(undefined);
        setIsFavorite(true);
        if(callback)callback();
      }else{
        setError(result.response.statusText);
      }
      setLoading(false)
    });
  };

  const removeFavorite = async () => {
    setLoading(true);
    Manager.removeMovieFromFav(user,movieId).then((result)=>{
      if(result.response.ok){
        setError(undefined);
        setIsFavorite(false);
        if(callback)callback();
      }else{
        setError(result.response.statusText);
      }
      setLoading(false)
    });
  };
  if(isFavorite === undefined && loading===false){
    setLoading(true);
    Manager.getFavMovies(user).then((result)=>{
      if(result.response.ok){
        let ok = false;
        result.data?.forEach(element => {
          if(element.id===movieId){
            ok=true;
          }
        });
        setIsFavorite(ok);
      }else{
        setIsFavorite("error");
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
      {isFavorite ? (
        <TbHeartMinus
          size={30}
          className='text-yellow-400'
          onClick={removeFavorite}
        />
      ) : (
        <TbHeartPlus
          size={30}
          className='text-yellow-400'
          onClick={addFavorite}
        />
      )}
    </>
  );
};

export default AddFavorite;
