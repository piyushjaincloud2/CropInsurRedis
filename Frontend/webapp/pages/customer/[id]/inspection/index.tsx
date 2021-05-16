import { useEffect, useState } from 'react';
import Hero from 'components/Hero';
import React from 'react';
import Box from '@material-ui/core/Box';
import InspectionTable from 'components/InspectionTable';
import { useCustomerStorage } from 'lib/useCustomerData';

export default function InspectionList({ id }) {
  const { userData, fetch } = useCustomerStorage();
  const [personalinfo, setPersonalInfo] = useState(null);
  useEffect(() => { fetch(id) }, [])
  useEffect(() => {
    setPersonalInfo(userData)
  }, [userData])

  return (
    <>
      <Hero 
        title={personalinfo?.name} 
        subtext={`User Id: ${personalinfo?.userId ?? ''}`} 
        ctalink={{ label: 'Policy information', url: `/policy/${id}` }} 
        ctaSecLink={{ label: 'Request Inspection', url: `/customer/${id}/inspection/new` }} 
      />
       <InspectionTable 
          customerId={id} 
          list={personalinfo?.properties[0]?.inspections} 
          policyAssociated={personalinfo?.properties[0]?.policy?.id}
        />
      <Box>
      </Box>
    </>
  );
  return null;
}

InspectionList.getInitialProps = ({ query: { id } }) => {
  return { id };
};