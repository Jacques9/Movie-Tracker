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
import Watched from './pages/Watched';
import { ReactSession } from 'react-client-session';
import Watching from './pages/Watching';
ReactSession.setStoreType("localStorage");
function App() {
  const [user, setUser] = useState(undefined);
  const callback = ()=>{
    setUser(UserProfile.getId);
  }
  return (
    <div className='App'>
      <Header user={user} update={callback} />
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/login' element={user ? <Navigate to='/' /> : <Login update={callback}/>} />
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
          path='/watched'
          element={!user ? <Navigate to='/' /> : <Watched user={user} />}
        />
        <Route
          path='/watching'
          element={!user ? <Navigate to='/' /> : <Watching user={user} />}
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
