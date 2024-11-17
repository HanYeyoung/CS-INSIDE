import React, { useRef } from 'react'
import { IoIosChatboxes } from 'react-icons/io';
import Dropdown from 'react-bootstrap/Dropdown';
import Image from 'react-bootstrap/Image';
import { useDispatch, useSelector } from 'react-redux';
import { getAuth, signOut, updateProfile } from "firebase/auth";
import { getStorage, ref as strRef, getDownloadURL, uploadBytesResumable } from "firebase/storage";
import app, { db } from '../../../firebase';
import { ref, update } from "firebase/database";
import { clearUser, setPhotoUrl } from '../../../store/userSlice';

function UserPanel() {
  const { currentUser } = useSelector(state => state.user)
  const dispatch = useDispatch();
  const auth = getAuth(app);
  const inputOpenImageRef = useRef();

  const handleLogout = () => {
    signOut(auth).then(() => {
      dispatch(clearUser());
    }).catch((error) => {
      console.error(error);
    });
  }

  const handleOpenImageRef = () => {
    inputOpenImageRef.current.click();
  }

  const handleUploadImage = async (event) => {
    const file = event.target.files[0];
    const user = auth.currentUser;

    const metadata = { contentType: file.type };
    const storage = getStorage();

    try {
      let uploadTask = uploadBytesResumable(strRef(storage, `user_image/${user.uid}`), file, metadata)

      uploadTask.on('state_changed',
        (snapshot) => {

          const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
          console.log('Upload is ' + progress + "% done");
          switch (snapshot.state) {
            case 'paused':
              console.log('Upload is paused');
              break;
            case 'running':
              console.log('Upload is running');
              break;
            default:
              break;
          }
        },
        (error) => {
          switch (error.code) {
            case 'storage/unauthorized':
              break;
            case 'storage/canceled':
              break;
            case 'storage/unknown':
              break;
            default:
              break;
          }
        },
        () => {
          getDownloadURL(uploadTask.snapshot.ref).then((downloadURL) => {
            updateProfile(user, {
              photoURL: downloadURL
            })
            dispatch(setPhotoUrl(downloadURL))
            update(ref(db, `users/${user.uid}`), { image: downloadURL })
          });
        }
      );
    } catch (error) {
        console.log(error)
      }
  }
  
  if (!currentUser) return <div>...loading</div>
  return (
    <div>
      <h3 style={{ color: 'white'}}>
        <IoIosChatboxes />{" "} Chat App
      </h3>

      <div style={{ display: 'flex', marginBottom: '1rem'}}>
        <Image
          src={currentUser.photoURL}
          style={{ width: '30px', height: '30px', marginTop: '3px'}}
          roundedCircle
        />

        <Dropdown>
          <Dropdown.Toggle
            style={{ background: 'transparent', border: '0px' }}
            id="dropdown-basic"
          >
            {currentUser.displayName}
          </Dropdown.Toggle>

          <Dropdown.Menu>
            <Dropdown.Item onClick={handleOpenImageRef}>
              Edit Your Profile
            </Dropdown.Item>
            <Dropdown.Item onClick={handleOpenImageRef}>
              Log Out
            </Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
      </div>
      <input
        onChange={handleUploadImage}
        accept="image/jpeg, image/png"
        style={{ display: 'none' }}
        ref={inputOpenImageRef}
        type='file'
      />
    </div>
  )
}

export default UserPanel;