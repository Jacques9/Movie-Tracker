import React, { useState } from 'react';

import { FaLock } from 'react-icons/fa';
import { TiDelete } from 'react-icons/ti';
import { Link } from 'react-router-dom';
import Manager from '../ApiManager';
import Loading from '../components/Loading';

const Comments = ({ movie, user }) => {
  const [review, setReview] = useState('');
  const [rating,setRating] = useState(undefined);
  const [loading,setLoading] = useState(false);
  const [error,setError] = useState(undefined);
  const [movieReviews,setMovieReviews] = useState(movie.reviews);
  console.log(movie.reviews);
  const deleteComment = (id) =>{ 

  }
  const commentHandler = (e) => {
    e.preventDefault();
    setLoading(true);
    if (review === '' || rating===undefined) {
      setLoading(false);
      return;
    }
    Manager.addReview(user,movie.id,rating,review).then(m=>{
      if(m.response.ok){
        Manager.getMovieById(movie.id).then(
          m=>{

            m = m.data;
            movie.reviews = m.reviews;
            setMovieReviews(m.reviews);
            setRating(undefined);
            setReview(undefined); 
            setLoading(false);
          }
        )
      }else{
        setError(m.data.message);
        setLoading(false);
      }
    });
  };
  if (loading){
    return <div className='flex items-center justify-center w-full'>
      <Loading size={'30px'} />
      </div>;
  }
  return (
    <div className='flex flex-col gap-8 my-4 lg:my-8'>
      <h2 className='pl-4 text-2xl font-bold border-l-8 border-yellow-400 lg:text-4xl '>
        Reviews
      </h2>
      {user ? (
        <form className='relative' onSubmit={commentHandler}>
          <input
              type='number'
              placeholder='Rating (0 - 5)'
              className='p-2 rounded-md shadow-md outline-none bg-slate-50 w-1/4'
              min={0}
              max={5}
              value={rating || ''}
              onChange={(e) => setRating(e.target.value)} />
          
          <input
            value={review || ''}
            onChange={(e) => {
              setReview(e.target.value);
            }}
            type='text'
            placeholder='Write your review'
            className='w-full p-2 text-lg border-2 rounded-lg outline-none lg:p-4 bg-slate-50'
          />
          
          <input
            className='absolute right-0 px-10 py-2 text-lg font-bold text-white transition-all duration-300 bg-yellow-400 border-2 border-yellow-400 rounded-r-lg cursor-pointer lg:py-4 hover:bg-yellow-300 hover:border-yellow-300 hover:tracking-wider'
            type='submit'
            value={(error?error:'Send')}
          />
        </form>
      ) : (
        <p className='flex items-center justify-center gap-2 p-4 font-bold border-2 border-gray-500 rounded-md bg-slate-50 text-slate-400'>
          <FaLock className='mt-[-4px]' /> <Link to='/login'>Log in</Link> to
          comment
        </p>
      )}
      <div className='space-y-4'>
        {movieReviews
          ?.sort((a, b) => b.review_data.stars - a.review_data.stars)
          .map((comment, index) => (
            <div className='py-1 bg-slate-50' key={index}>
              <p className='mb-1 font-bold lg:text-xl float-right'>Rating: {comment.review_data.stars}</p>
              <p className='mb-1 font-bold lg:text-xl '>{comment.review_data.user_id}</p>
              <div className='flex items-center justify-between w-full gap-4'>
                <p className='w-full py-2 overflow-hidden text-sm italic text-gray-700 break-words'>
                  "{comment.review_data.text}"
                </p>
                {user === comment.review_data.user_id && (
                  <p
                    onClick={() => deleteComment(comment.id)}
                    className='text-2xl text-red-500'
                  >
                    <TiDelete />
                  </p>
                )}
              </div>
            </div>
          ))}
      </div>
    </div>
  );
};

export default Comments;
