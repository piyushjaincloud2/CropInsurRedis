import { useState, useContext, createContext } from 'react';
// import azure from 'azure-storage';
import { uid } from 'uid';
import { useRouter } from 'next/router';
import axios from 'axios';

const TABLE_NAME = 'Users';
type CustomerStorageProps = {
  data: []
  userData: any
  error: string
  fetch(userId: string): void
  fetchAll(): void
  insert(userData: any): void
}

const CustomerStorageContext = createContext<Partial<CustomerStorageProps>>({});

export function CustomerStorageProvider({ children }) {
  const customerData = useProvideCustomerStorage()
  return <CustomerStorageContext.Provider value={customerData}>{children}</CustomerStorageContext.Provider>
}
export const useCustomerStorage = () => {
  return useContext(CustomerStorageContext);
};

function useProvideCustomerStorage(): CustomerStorageProps {
  const router = useRouter();
  const [customerData, setCustomerData] = useState(null);
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState('');


  const fetch = (userId: string) => {
    setError('')
    setUserData(null)

    axios.get(`${process.env.NEXT_PUBLIC_CUSTOMER_SERVICE}/customer/get/${userId}`)
      .then((response) => {
        const parsedData = response.data;
        console.log(response.data);

        setUserData(parsedData.data);
      }).catch((error) => {
        setError(error.message)
      });
  }

  const fetchAll = () => {
    setError('')
    axios.get(`${process.env.NEXT_PUBLIC_CUSTOMER_SERVICE}/customer/get`, userData)
      .then((response) => {
        const parsedData = response.data;
        setCustomerData(parsedData.data);
      }).catch((error) => {
        setError(error.message)
      });
  }

  const insert = (userData: any) => {
    setError('');
    axios.post(`${process.env.NEXT_PUBLIC_CUSTOMER_SERVICE}/customer/save`, userData)
      .then((response) => {
        router.push('/customer');
      }).catch((error) => {
        setError(error.message)
      });
  }

  return {
    data: customerData,
    userData,
    error,
    fetch,
    fetchAll,
    insert
  }
}