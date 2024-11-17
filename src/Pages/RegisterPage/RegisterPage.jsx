import React, { useState } from 'react'
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import {createUserWithEmailAndPassword, getAuth, updateProfile} from 'firebase/auth';
import app, { db } from '/src/firebase';
import md5 from 'md5';
import { ref, set } from 'firebase/database';
import { setUser } from '../../store/userSlice';

function RegisterPage() {

    const auth = getAuth(app)
    const [loading, setLoading] = useState(false);
    const [errorFromSubmit, setErrorFromSubmit] = useState("");
    const { 
        register,
        watch,
        formState: { errors },
        handleSubmit
    } = useForm();

    const onSubmit = async (data) => {
        // data.email => johndoe12@gmail.com   data.password => 123123 data.name => john doe

        try {
            setLoading(true);
            const createdUser = await createUserWithEmailAndPassword(auth, data.email, data.password)

            await updateProfile(auth.currentUser, {
                displayName: data.name,
                photoURL: `http://gravatar.com/avatar/${md5(createdUser.user.email)}?d=identicon`,
            })

            const userData = {
                uid: createdUser.user.uid,
                displayName: createdUser.user.displayName,
                photoURL: createdUser.user.photoURL
            }
            dispatch(setUser(userData));

            set(ref(db, `users/${createdUser.user.uid}`), {
                name: createdUser.user.displayName,
                image: createdUser.user.photoURL
            })
            setLoading(false)
        } catch (error) {
            setErrorFromSubmit(error.message);
            setLoading(false)
            setTimeout(() => {
                setErrorFromSubmit("");
            }, 5000);
        }
    }


    return (
        <div className='auth-wrapper'>
            <div style={{textAlign: 'center'}}>
                <h3>Register</h3>
            </div>
            <form onSubmit={handleSubmit(onSubmit)}>
                <label htmlFor='email'>Email</label>
                <input
                    name='email'
                    type='email'
                    id='email'
                    {...register("email", { required: true, pattern: /^\S+@\S+$/i })}
                />
                {errors.email && <p>The email field is required</p>}

                <label htmlFor='name'>Name</label>
                <input
                    name='name'
                    type='text'
                    id='name'
                    {...register("name", {required: true, maxLength: 30})}
                />
                {errors.name && errors.name.type === "required" && <p>The name field is required</p>}
                {errors.name && errors.name.type === "maxLength" && <p>Check your input again</p>}

                <label htmlFor='password'>Password</label>
                <input
                    name='password'
                    type='password'
                    id='password'
                    {...register("password", {required: true, minLength: 8 })}

                />
                {errors.password && errors.password.type === "required" && <p>The password field is required</p>}
                {errors.password && errors.password.type === "minLength" && <p>Password must be longer than 8 characters</p>}

                <label>Password Confirm</label>
                <input
                    name="password_confirm"
                    type="password"
                    {...register("password_confirm", {
                        required: true,
                        validate: (value) =>
                            value === password.current
                    })}
                />
                {errors.password_confirm && errors.password_confirm.type === "required" && <p>This password confirm field is required</p>}
                {errors.password_confirm && errors.password_confirm.type === "validate" && <p>The passwords do not match</p>}

                {errorFromSubmit &&
                    <p>{errorFromSubmit}</p>
                    }
                <input  type='submit' disabled={loading} />
                <Link style={{ color: 'gray', textDecoration: 'none'}} to={'/login'}>Already have an account?</Link>
            </form>
        </div>
    )
}

export default RegisterPage;