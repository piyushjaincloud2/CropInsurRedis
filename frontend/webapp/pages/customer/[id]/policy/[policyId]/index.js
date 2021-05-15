import {useState, useEffect} from 'react';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import { makeStyles } from '@material-ui/core/styles';
import Hero from 'components/Hero';
import InspectionTable from 'components/InspectionTable';
import {useCustomerStorage} from 'lib/useCustomerData';
import PictureAsPdfIcon from '@material-ui/icons/PictureAsPdf';


const __policyData = [{
  key:'farmArea',
  label: 'Farm area',
  unit: 'acres',
}, {
  key:'expectedYeild',
  label: 'Expected yield',
  unit: 'Qntl/acre',
}, {
  key:'expectedMarketPrice',
  label: 'Expected market price',
  unit: 'Rs/Kg',
}, {
  label: 'Premium rate',
  unit: '%',
  value: '2'
}, {
  key:'policySumAssured',
  label: 'Sum Assured',
  unit: 'Rs',
}, {
  key:'policyPremium',
  label: 'Single Premium',
  unit: 'Rs',
}, {
  key:'coveragePeriod',
  label: 'Coverage Period',
  unit: 'months',
}, {
  key:'date',
  label: 'Policy commencement date',
},{
  key:'claimAmount',
  label: 'Claim Amount',
},]



export default function PolicyDetails({ id, policyId }) {
  const { userData, fetch } = useCustomerStorage();
  const [personalinfo, setPersonalInfo] = useState(null);
  const [policyInfo, setPolicyInfo] = useState(null);
  useEffect(() => { 
    fetch(id) 
  }, [policyId]);

  useEffect(() => {
    setPersonalInfo(userData)
    
    const policyData = {...userData?.properties[0], ...userData?.properties[0]?.policy};
    if(policyData) {
      const data = __policyData.map(item=>{
        if(item.key) {
          if(item.key === 'date') {
            item.value = (new Date(policyData[item.key])).toDateString();  
          } else {
            item.value = policyData[item.key] || '-'
          }
        }
        return item;
      });
      setPolicyInfo(data)
    }
  }, [userData]);

  const classes = useStyles();
  return (
    <>
      <Hero title={personalinfo?.name} 
        subtext={policyId && `Policy no: ${policyId}`} 
        ctalink={{ label: 'Personal information', url: `/customer/${id}` }} 
     />
      <Box>
        <Container>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography
                component="h2"
                variant="h4"
                color="inherit"
                gutterBottom
              >
                Policy Details
            </Typography>
            </Grid>
            {policyInfo && policyInfo.map(item => (
              <Grid item md={4} xs={6}>
                <Typography
                  component="p"
                  variant="inherit"
                  color="inherit"
                  gutterBottom
                >
                  {item.label}
                </Typography>
                <Typography
                  component="p"
                  variant="h6"
                  color="inherit"
                  gutterBottom
                >
                  {item.value} {item.unit}
                </Typography>
              </Grid>
            ))}
            
          </Grid>
            <Box className={classes.download}>
              <PictureAsPdfIcon 
                  color="secondary"/>
                <Typography
                  className={classes.downloadTxt}
                  component="span"
                  variant="inherit"
                  color="secondary"
                >
                  Download Policy as PDF
                </Typography> 
            </Box>
        </Container>
      </Box>      
      <Box>
        <InspectionTable 
          customerId={id} 
          list={personalinfo?.properties[0]?.inspections} 
          policyAssociated={personalinfo?.properties[0]?.policy?.id}
        />
      </Box>
    </>
  );
}

const useStyles = makeStyles((theme) => ({
  gridBg: {
    backgroundColor: 'rgba(30, 136, 229, 0.1)'
  },
  download: {
    cursor:'pointer',
    margin: theme.spacing(2, 0),
    display: 'flex',
    alignItems: 'center'
  },
  downloadTxt: {
    marginLeft: theme.spacing(1),
  }
}))

PolicyDetails.getInitialProps = ({ query: { id, policyId } }) => {
  return { id, policyId };
};