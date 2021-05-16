import { useState, useContext, createContext } from 'react';
// import azure from 'azure-storage';
import { uid } from 'uid';
import { useRouter } from 'next/router';
import axios from 'axios';

const TABLE_NAME = 'Inspections';
type InspectionStorageProps = {
  error: string
  insert(inspectionData: any, callback: Function): void
}

const InspectionStorageContext = createContext<Partial<InspectionStorageProps>>({});

export function InspectionStorageProvider({ children }) {
  const InspectionData = useProvideInspectionStorage()
  return <InspectionStorageContext.Provider value={InspectionData}>{children}</InspectionStorageContext.Provider>
}
export const useInspectionStorage = () => {
  return useContext(InspectionStorageContext);
};

function dataParser(data: any) {
  const parsedData = {
    id: uid()
  };
  for (const key in data) {
    if (key.toLowerCase().search(/(rowkey)|(partitionkey)|(.metadata)/) === -1) {
      if (data[key]['$'] === 'Edm.DateTime') {
        parsedData[key] = data[key]['_'].toLocaleString()
      } else {
        parsedData[key] = data[key]['_'];
      }
    }
  }
  return parsedData;
};

function useProvideInspectionStorage():InspectionStorageProps {
  const [error, setError] = useState('');


  const insert = (inspectionData: any, callback?: Function) => {
    setError('');
    axios.post(`${process.env.NEXT_PUBLIC_INSPECTION_SERVICE}/inspection/save`, inspectionData)
    .then((response) => {
        callback({...response.data, id:inspectionData.id})
    }).catch((error)=>{
        setError(error.message)
    });
  }

  return {
    error,
    insert,
  }
}