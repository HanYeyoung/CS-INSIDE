// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBoX_IUysDOdjDSwH0V-ZtppghgkDc4ih4",
  authDomain: "cheezee-chat.firebaseapp.com",
  databaseURL: "https://cheezee-chat-default-rtdb.firebaseio.com/",
  projectId: "cheezee-chat",
  storageBucket: "cheezee-chat.appspot.com",
  messagingSenderId: "529704262748",
  appId: "1:529704262748:web:bb078dff49cd0ce3bada99"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getDatabase(app);
export default app;