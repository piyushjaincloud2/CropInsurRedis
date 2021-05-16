import { useState, useContext, createContext, useEffect } from 'react';
import { useRouter } from 'next/router';

type AuthProps = {
  user: any;
  error: string;
  signIn: (email: any, password: any) => Promise<void>;
  signUp: (email: any, password: any) => Promise<void>;
  signOut: () => void;
}
const AuthContext = createContext<Partial<AuthProps>>({});

// You can wrap your _app.js with this provider
export function AuthProvider({ children }) {
  const auth = useProvideAuth();
  return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>;
}

// Custom React hook to access the context
export const useAuth = () => {
  return useContext(AuthContext);
};

function useProvideAuth() {
  const router = useRouter();
  const [error, setError] = useState('');
  const [user, setUser] = useState(null);

  useEffect(() => {
    console.log(user, sessionStorage.getItem(user));
  }, [])
  const signIn = async (email, password) => {
    console.log(`signIn called, ${email} ${password}`);
    if (email && password) {
      sessionStorage.setItem('token', '123456');
      sessionStorage.setItem('user', 'jeshu911@gmail.com');
      setUser({email, policyId:'AX-258963', _id:'ax-9887'})
      router.push('/customer');
    } else {
      setError("Invalid Login");
    }
  }

  const signOut = () => {
    sessionStorage.removeItem('token');
    setUser(null)
    router.push('/');
  }

  return {
    user,
    error,
    signIn,
    signOut,
  };
} 
