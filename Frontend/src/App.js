// Routes
import { Routes, Route, Navigate } from 'react-router-dom';

// Hooks
import { useState } from 'react';

// Components
import Header from './components/Header';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Details from './pages/Details';
import Profile from './pages/Profile';
import NewReview from './pages/NewReview';
import Favorites from './pages/Favorites';
import UserProfile from './UserProfile';
import { ReactSession } from 'react-client-session';
ReactSession.setStoreType("localStorage");
function App() {
  const [user, setUser] = useState(undefined);
  const update = ()=>{
    setUser(UserProfile.getUsername);
  }
  return (
    <div className='App'>
      <Header user={user} update={update} />
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/login' element={user ? <Navigate to='/' /> : <Login update={update}/>} />
        <Route
          path='/register'
          element={user ? <Navigate to='/' /> : <Register />}
        />
        <Route path='/details/:id' element={<Details user={user} />} />
        <Route
          path='/profile'
          element={!user ? <Navigate to='/' /> : <Profile user={user} />}
        />
        <Route
          path='/favorites'
          element={!user ? <Navigate to='/' /> : <Favorites user={user} />}
        />
        <Route
          path='/add-review'
          element={!user ? <Navigate to='/' /> : <NewReview user={user} />}
        />
        <Route path='/details/:id' element={<Details />} />
        <Route path='/*' element={<Navigate to='/' />} />
      </Routes>
    </div>
  );
}

export default App;