import { useEffect, useState } from 'react';
import Hero from 'components/Hero';
import PersonalInfo from 'components/PersonalInfo';
import React from 'react';
import Box from '@material-ui/core/Box';
import InspectionTable from 'components/InspectionTable';
import { useCustomerStorage } from 'lib/useCustomerData';

export default function CustomerDetails({ id }) {
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
        subtext={`User Id: ${personalinfo?.id ?? ''}`} 
        ctalink={{ label: 'Request Inspection', url: `/customer/${id}/inspection/new` }} 
      />
      <PersonalInfo {...personalinfo} />
      <Box>
        <InspectionTable 
          customerId={personalinfo?.id} 
          list={personalinfo?.properties[0]?.inspections} 
          policyAssociated={personalinfo?.properties[0]?.policy?.id}
        />
      </Box>
    </>
  );
  return null;
}

CustomerDetails.getInitialProps = ({ query: { id } }) => {
  return { id };
};