import Link from 'next/link'
import React from 'react'

const Register = () => {
    return (
        <div className='bg-white'>
            <div className='flex flex-col items-center justify-center h-screen p-6'>
                <div className='w-10/12 mx-auto md:w-96'>
                    <h1 className='mb-2 text-lg font-medium'>Sign-up</h1>
                    <form>
                        <button className='w-full py-2 mb-1 text-xs font-bold text-white uppercase bg-gray-400 border border-gray-400 rounded'>
                            Sign-up
                        </button>
                    </form>
                    <small>
                        Did you sign-up already?
                        <Link href="/login">
                            <a className='ml-1 text-blue-500 uppercase'>Log-in</a>
                        </Link>
                    </small>
                </div>
            </div>
        </div>
    )
}

export default Register