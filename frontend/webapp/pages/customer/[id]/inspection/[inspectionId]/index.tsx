import { useState, useEffect } from 'react';
import Container from '@material-ui/core/Container';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Alert from '@material-ui/lab/Alert';
import { makeStyles } from '@material-ui/core/styles';
import DroneDataTable from 'components/DroneDataTable';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useInspectionStorage } from 'lib/useInspectionData';
import { usePolicyStorage } from 'lib/usePolicyData';
import { calculatePostHarvest, getRecommanation } from 'utils/IDVCalculator';
import { useCustomerStorage } from 'lib/useCustomerData';
import { uid } from 'uid';

const useStyles = makeStyles((theme) => ({
  topShift: {
    marginTop: theme.spacing(6)
  },
  sliderBase: {
    '& .react-slider__ul': {
      display: 'none',
    }
  },
  alert: {
    display: 'flex',
    alignItems: 'center',
    '& button': {
      marginLeft: theme.spacing(2)
    }
  },
  textfield: {
    marginLeft: theme.spacing(1)
  },
  recommendation: {
    display: 'flex',
    alignItems: 'center',
    justifyContent:'space-between',
    marginBottom:theme.spacing(3)
  },
}))


export default function NewInspection({ id, inspectionId }) {
  const router = useRouter()
  const classes = useStyles();
  const [newInspectionId, setNewInspectionId] = useState(null);
  const [inspectionStarted, setInspectionStarted] = useState(false);
  const [enableCalculator, setEnableCalculator] = useState(false);
  const [claimPending, setClaimPending] = useState(true);
  const { userData: customerData, fetch:fetchCustomerData } = useCustomerStorage();
  const { saveClaim } = usePolicyStorage();
  const { insert: insertInspection } = useInspectionStorage();
  const [idv, setIDV] = useState(null);
  const [ws, setWS] = useState(null);
  const [droneData, setDroneData] = useState([]);
  const [policyData, setPolicyData] = useState(null);
  const [inspectionData, setInspectionData] = useState(null);
  let data:any = [];

  useEffect(() => {
    fetchCustomerData(id);
    const websocket = new WebSocket('ws://localhost:3625' );
    websocket.onopen = function() {
      setWS(websocket)
    }
    websocket.onmessage =  (res) => {
      updateDroanData(JSON.parse(res.data));
    }
  }, [])

  
  const updateDroanData = (newData) =>{
    data = [...data, newData];
    setDroneData([...data]);
  }

  useEffect(() => {
    if (customerData) {
      console.log(customerData);
      const _inspectionData = customerData?.properties[0].inspections.find(i => i.id === inspectionId);
      _inspectionData.IDV = _inspectionData?.postHarvestIdv || _inspectionData?.preHarvestIdv;
      const _droneData = _inspectionData?.fieldDataList
      setInspectionData(_inspectionData);
      setPolicyData(customerData?.properties[0].policy);
      setDroneData(_droneData);
    }
  }, [customerData])

  useEffect(() => {
    if (policyData)
      if (policyData?.claimAmount) {
        setClaimPending(false)
      }
  }, [policyData])

  const startInspection = () => {
    const inspectionId = uid();
      ws.send(`inspection|${inspectionId}`)
      setClaimPending(true);
      setNewInspectionId(inspectionId)
      setInspectionStarted(true);
  };

  const onSimulationEnd = (_avgValues) => {
    setInspectionStarted(false);
    setEnableCalculator(true);
    const recomadations = getRecommanation(_avgValues);
    insertInspection({
      id:newInspectionId, 
      customerId:id, 
      propertyId:customerData?.properties[0]?.id, 
      fieldDataList: droneData}, (data) => {
        setIDV({recomadations, IDV:data.data.postHarvestIdv, premium:data.data.preHarvestPremium});
        console.log(data);
      })
  }

  const convertToClaims = () => {
    saveClaim({
      customerId: id,
      propertyId: customerData?.properties[0].id,
      inspectionId: newInspectionId || inspectionId
    }, () => {
      router.push(`/customer/${id}/policy/${policyData.id}`);
    })
  }

  const renderRecomandatios = () => {
    const recomStr = idv?.recomadations || inspectionData?.recomadations || '';
    if (recomStr && !inspectionStarted) {
      const recommendation = recomStr.split("##");
      return (
        <Grid item xs={12} className={classes.sliderBase}>
          <Box className={classes.recommendation}>
            <Typography
              component="h6"
              variant="h5"
              color="inherit"
              gutterBottom
            >
              Recommendation(s) based on Inspection
              </Typography>
            <Button component="a" href={`mailto:?&subject=Drone%20Argo%20Insurence | Recommendations ;&body=Recommendations%0A%0A${recommendation.join('%0A%0A')}`} variant="outlined" color="secondary">Notify</Button>
          </Box>
          <Box >
            {recommendation.map(item => (
              <Alert severity="info" className={classes.alert}>
                {item}
              </Alert>
            )
            )}
          </Box>
        </Grid>
      )
    }
    return null;
  }

  return (
    <Box>
      <Container className={classes.topShift}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography
              component="h2"
              variant="h4"
              color="inherit"
              gutterBottom
            >
              Inspection with Drone
            <Typography
                component="span"
                variant="h6"
                color="inherit"
                gutterBottom
              >
                {(newInspectionId && ` (${newInspectionId})`) || (inspectionId && ` (${inspectionId})`)}
              </Typography>
            </Typography>

            <>
              {policyData && policyData?.policySumAssured &&
                <Typography
                  component="h6"
                  variant="h6"
                  color="inherit"
                  gutterBottom
                >
                  Sum Assured : {policyData.policySumAssured} Rs.
              </Typography>
              }
              <Typography
                component="h6"
                variant="h6"
                color="inherit"
                gutterBottom
              >
                IDV after Inspection : {idv ? parseFloat(`${idv.IDV}`).toFixed(2) : inspectionData && parseFloat(inspectionData.IDV).toFixed(2)} Rs.
              </Typography>
              {policyData?.policyPremium &&
                <Typography
                  component="h6"
                  variant="h6"
                  color="inherit"
                  gutterBottom
                >
                  Single Premium : {policyData?.policyPremium ?? '-'} Rs.
              </Typography>}
            </>

            {!claimPending && inspectionData &&
              <>
                <Typography
                  component="h6"
                  variant="h6"
                  color="inherit"
                  gutterBottom
                >
                  Claim is settled at {policyData ? ` ${parseFloat(policyData.claimAmount).toFixed(2)} Rs.` : ''}
                </Typography>
                <Link href={`/customer/${id}/policy/${policyData.id}`}>
                  <Button variant="outlined" color="secondary">
                    Back to Policy
                </Button>
                </Link>
              </>
            }

            {claimPending && !inspectionStarted && !enableCalculator &&
              <Button variant="outlined" color="secondary" onClick={startInspection}>
                Start New Inspection
            </Button>}
            {claimPending && enableCalculator &&
              <>
                <Button variant="outlined" color="secondary" onClick={convertToClaims}>
                  Convert to Claim
            </Button>
                <Link href={`/customer/${id}`}>
                  <Button variant="outlined" color="secondary">
                    Save
              </Button>
                </Link>
              </>
            }
          </Grid>
          {renderRecomandatios()}
          <Grid item xs={12} className={classes.sliderBase}>
            <DroneDataTable
              droneData={droneData}
              inspectionStarted={inspectionStarted}
              onSimulationEnd={onSimulationEnd}
            />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

NewInspection.getInitialProps = ({ query: { id, inspectionId } }) => {
  return { id, inspectionId };
};