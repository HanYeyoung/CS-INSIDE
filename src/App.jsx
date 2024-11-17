import { Route, Routes, useNavigate } from 'react-router-dom'
import './App.css'
import ChatPage from '/src/Pages/ChatPage/ChatPage.jsx';
import LoginPage from '/src/Pages/LoginPage/LoginPage.jsx';
import RegisterPage from '/src/Pages/RegisterPage/RegisterPage.jsx';
import { getAuth, onAuthStateChanged } from "firebase/auth";
import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import { clearUser, setUser } from "./store/userSlice";
import app from "./firebase";

function App() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const auth = getAuth(app);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        navigate('/');
        const userData = {
          uid: user.uid,
          displayName: user.displayName,
          photoURL: user.photoURL
        }
        dispatch(setUser(userData));
      } else {
        navigate('/login');
        dispatch(clearUser());
      }
    });

    return () => {
      unsubscribe();
    }
  }, []);

  return (
    <Routes>
      <Route path='/' element={<ChatPage />}></Route>
      <Route path='/login' element={<LoginPage />}></Route>
      <Route path='/register' element={<RegisterPage />}></Route>
    </Routes>
  );
}

export default App;
