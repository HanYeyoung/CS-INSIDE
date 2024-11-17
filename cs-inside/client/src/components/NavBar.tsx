import axios from "axios";
import Image from "next/image";
import Link from "next/link";
import { FaSearch } from "react-icons/fa";
import { useAuthDispatch, useAuthState } from "../context/auth";

const NavBar: React.FC = () => {
    const { loading, authenticated } = useAuthState();
    const dispatch = useAuthDispatch();

    const handleLogout = () => {
        axios.post("/auth/logout")
            .then(() => {
                dispatch("LOGOUT");
                window.location.reload();
            })
            .catch((error) => {
                console.log(error);
            });
    };

    return (
        <div className="fixed inset-x-0 top-0 z-10 flex items-center justify-between px-5 bg-white h-13">
            <span className="text-2xl font-semibold text-gray-400">
                <Link href="/">
                    <Image
                        src="/cs-inside-name-logo.png"
                        alt="logo"
                        width={80}
                        height={45}
                    />
                </Link>
            </span>
            <div className="max-w-full px-4">
                <div className="relative flex items-center bg-gray-100 border rounded hover:border-gray-700 hover:bg-white">
                    <FaSearch className="ml-2 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Search CS-INSIDE"
                        className="px-3 py-1 bg-transparent rounded h-7 focus:outline-none"
                    />
                </div>
            </div>

            <div className="flex">
                {!loading && (
                    authenticated ? (
                        <button
                            className="w-20 px-2 mr-2 text-sm text-center text-white bg-gray-400 rounded h-7"
                            onClick={handleLogout}
                        >
                            Log Out
                        </button>
                    ) : (
                        <>
                            <Link href="/login">
                                <div className="w-20 px-2 pt-1 mr-2 text-sm text-center text-blue-500 border border-blue-500 rounded h-7">
                                    Log In
                                </div>
                            </Link>
                            <Link href="/register">
                                <div className="w-20 px-2 pt-1 text-sm text-center text-white bg-gray-400 rounded h-7">
                                    Sign Up
                                </div>
                            </Link>
                        </>
                    )
                )}
            </div>
        </div>
    );
};

export default NavBar;
