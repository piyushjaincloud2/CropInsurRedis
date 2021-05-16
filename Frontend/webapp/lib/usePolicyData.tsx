import { useState, useContext, createContext } from 'react';
// import azure from 'azure-storage';
import { uid } from 'uid';
import { useRouter } from 'next/router';
import axios from 'axios';

const TABLE_NAME = 'Policies';
type PolicyStorageProps = {
  policyList: []
  policyData: any
  error: string
  insert(policyData: any, callback: Function): void
  saveClaim(claimData: any,callback: Function): void
}

const PolicyStorageContext = createContext<Partial<PolicyStorageProps>>({})

export function PolicyStorageProvider({ children }) {
  const _mPolicyData = useProvidePolicyStorage()
  return <PolicyStorageContext.Provider value={_mPolicyData}>{children}</PolicyStorageContext.Provider>
}
export const usePolicyStorage = () => {
  return useContext(PolicyStorageContext);
};

const useProvidePolicyStorage = (): PolicyStorageProps => {
  const [policyList, setPolicyList] = useState(null);
  const [policyData, setPolicyData] = useState(null);
  const [error, setError] = useState('');

  const fetch = (policyId:string) => {
    setPolicyData(null);
    setError('');
    
    axios.get(`${process.env.NEXT_PUBLIC_POLICY_SERVICE}/policy/get/${policyId}`)
    .then((response) => {
      const parsedData = response.data; 
        setPolicyData(parsedData[0])
    }).catch((error)=>{
        setError(error.message)
    });
  }
  const fetchAll = (customerId:string) => {
    setPolicyList(null)
    setError('')
    
    axios.get(`${process.env.NEXT_PUBLIC_POLICY_SERVICE}/policy/get/`)
    .then((response) => {
      const parsedData = response.data; 
      setPolicyList(parsedData)
    }).catch((error)=>{
        setError(error.message)
    });
  }
  const insert = (policyData:any, callback?:Function) => {
    setError('');

    const policyId = uid();
    policyData['policyId'] = policyId
    axios.post(`${process.env.NEXT_PUBLIC_POLICY_SERVICE}/policy/save`, policyData)
    .then((response) => {
      callback(policyId)
    }).catch((error)=>{
        setError(error.message)
    });
  }
  
  const saveClaim = (claimData:any, callback?: Function) => {
    setError('')
    axios.post(`${process.env.NEXT_PUBLIC_POLICY_SERVICE}/policy/claim`, claimData)
    .then((response) => {
      callback(response)
    }).catch((error)=>{
        setError(error.message)
    });
  }


  return {
    policyData,
    policyList,
    error,
    insert,
    saveClaim
  }

}