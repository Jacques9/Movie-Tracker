import React, { useState } from 'react';
import { FaUserAlt } from 'react-icons/fa';
import Loading from '../components/Loading';
import Manager from '../ApiManager';

const Profile = ({ user }) => {
  const [username, setUsername] = useState(undefined);
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading,setLoading] = useState(false);
  const [error, setError] = useState('');
  if(username===undefined){
    setUsername("");
    setLoading(true);
    Manager.getAllUsers().then(response=>{
      if(response.response.ok){
        var temp = response.data.find(u=>u.id);
        console.log(temp);
        if(temp!== null)setUsername(temp.username);
      }
      setLoading(false);
    });
  }
  const handleUpdateProfile = (e) => {
    e.preventDefault();
    setError(null);

    if (
      username === '' &&
      password === '' &&
      confirmPassword === ''
    ) {
      setError('There are empty fields');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords must be equal');
      return;
    }

    if (username !== '') {
      setLoading(true);
      Manager.updateUsername(username,user).then((response)=>{
        if(!response.response.ok)
          setError(response.data);
        setLoading(false)
      });
        
    }

    if (
      password !== '' &&
      confirmPassword !== '' &&
      password === confirmPassword
    ) {
      setLoading(true);
      Manager.updatePassword(password,user).then(setLoading(false))
      // updateUserPassword(password);
    }

    setUsername('');
    setPassword('');
    setConfirmPassword('');
    return;
  };
  if (loading){
    return <div className='flex items-center justify-center w-full'>
      <Loading size={'30px'} />
      </div>;
  }
  return (
    <section className='flex flex-col items-center justify-center sectionHeight bg-amber-200'>
      <div className='flex flex-col w-[90%] mx-auto justify-center items-center my-16 gap-8 '>

          <div className='flex justify-center items-center rounded-full w-[250px] h-[250px] object-cover border-4 border-zinc-800 shadow-md'>
            <FaUserAlt size={100} />
          </div>

        <h1 className='pb-2 text-2xl font-bold border-b-4 sm:text-3xl md:text-3xl lg:text-4xl text-zinc-800 border-zinc-800'>
          Hi, {username}!
        </h1>
      </div>

      <form
        className='flex flex-col max-w-[600px] w-[90%] mx-auto gap-3 mb-8
      '
        onSubmit={handleUpdateProfile}
      >
        {/* <div className='flex items-center w-full gap-3'>
          <input
            type='file'
            className='block w-full p-4 m-0 text-base font-normal text-gray-700 transition ease-in-out border-none rounded shadow-md bg-slate-50 form-control bg-clip-padding focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'
            onChange={(e) => setImage(e.target.files[0])}
          />
        </div> */}
        {/* <div className='flex items-center w-full gap-3'>
          <input
            type='text'
            value={username || ''}
            onChange={(e) => {
              setUsername(e.target.value);
            }}
            placeholder='Username'
            className='w-full p-4 rounded-md shadow-md outline-none bg-slate-50'
          />
        </div> */}
       
        <div className='flex items-center w-full gap-3'>
          <div className='flex flex-col w-full gap-3'>
            <input
              type='password'
              value={password || ''}
              onChange={(e) => {
                setPassword(e.target.value);
              }}
              placeholder='Password'
              className='p-4 rounded-md shadow-md outline-none bg-slate-50'
              autoComplete='true'
            />
            <input
              type='password'
              value={confirmPassword || ''}
              onChange={(e) => {
                setConfirmPassword(e.target.value);
              }}
              placeholder='Confirm Password'
              className='p-4 rounded-md shadow-md outline-none bg-slate-50'
              autoComplete='true'
            />
          </div>

        </div>

          <input
            type='submit'
            value='Update Password'
            className='w-full p-4 font-bold text-white transition-all duration-300 rounded-md shadow-sm cursor-pointer bg-zinc-800 hover:bg-zinc-700 hover:tracking-wider'
          />

        {error && <p className='error'>{error}</p>}
      
      </form>
    </section>
  );
};

export default Profile;
