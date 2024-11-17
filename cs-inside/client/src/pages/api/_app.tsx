import '../styles/globals.css'
import type { AppProps } from 'next/app'
import Axios from 'axios'
import { AuthProvider } from '../context/auth';
import NavBar from '../../components/NavBar';
import { useRouter } from 'next/router';
// import { SWRConfig } from 'swr';
// import Head from 'next/head';

function MyApp({ Component, pageProps }: AppProps) {
    Axios.defaults.baseURL = process.env.NEXT_PUBLIC_SERVER_BASE_URL + "/api";
    Axios.defaults.withCredentials = true;

  const { pathname } = useRouter();
  const authRoutes = ["/register", "/login"];
  const authRoute = authRoutes.includes(pathname);

  // const fetcher = async (url: string) => {
  //   try {
  //     const res = await axios.get(url);
  //     return res.data;
  //   } catch (error: any) {
  //     throw error.response.data
  //   }
  // }

    return <AuthProvider>
      {!authRoute && <NavBar />}
      <div className={authRoute ? "": "pt-12"}>
        <Component {...pageProps} />
      </div>
    </AuthProvider>
}

export default MyApp
