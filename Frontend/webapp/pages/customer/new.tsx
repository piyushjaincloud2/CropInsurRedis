import { useState } from 'react';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Container from '@material-ui/core/Container';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import Button from '@material-ui/core/Button';
import { useCustomerStorage } from 'lib/useCustomerData';
import { makeStyles } from '@material-ui/core/styles';



const useStyles = makeStyles((theme) => ({
  formGrid: {
    paddingTop: theme.spacing(6)
  }
}));

export default function NewCustomer() {
  const { error, insert } = useCustomerStorage();
  const onSubmit = async (event) => {
    event.preventDefault();
    insert({
      name, email, age, gender, mobile, location,
      address, experience, properties: [{premiumRate,cropName:cropType, farmArea, expectedYeild,
      expectedMarketPrice, coveragePeriod, latitude, longitude}]
    });
  };

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');
  const [mobile, setMobile] = useState('');
  const [location, setLocation] = useState('');
  const [address, setAddress] = useState('');
  const [pincode, setPincode] = useState('');
  const [experience, setExperience] = useState('');
  const [cropType, setCropType] = useState('');
  const [premiumRate, setPremiumRate] = useState('2');
  const [farmArea, setFarmArea] = useState('');
  const [expectedYeild, setExpectedYeild] = useState('');
  const [expectedMarketPrice, setExpectedMarketPrice] = useState('');
  const [coveragePeriod, setCoveragePeriod] = useState('4');
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');

  const styles = useStyles();
  return (
    <Container >
      <Grid container
        className={styles.formGrid}
        spacing={0}
        direction="column"
        alignItems="center"
        style={{ minHeight: 'calc(100vh - 64px)' }}>
        <Grid item xs={12} md={6}
        >
          <form onSubmit={onSubmit}>
            {error && <p>{error}</p>}
            <Typography variant="h4">Add New Customer</Typography>
            <Box pb={2.5} />
            <TextField
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="form-control"
              label="Name"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <TextField
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              type="email"
              className="form-control"
              label="Email"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <TextField
              value={mobile}
              onChange={(e) => setMobile(e.target.value)}
              type="tel"
              className="form-control"
              label="phone"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <TextField
              value={age}
              onChange={(e) => setAge(e.target.value)}
              className="form-control"
              label="Age"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <FormControl component="fieldset">
              <FormLabel component="legend">Gender</FormLabel>
              <RadioGroup aria-label="gender" name="gender1" value={gender} onChange={(e) => { setGender(e.target.value) }}>
                <FormControlLabel value="female" control={<Radio />} label="Female" />
                <FormControlLabel value="male" control={<Radio />} label="Male" />
              </RadioGroup>
            </FormControl>
            <Box pb={2.5} />
            <TextField
              value={cropType}
              onChange={(e) => setCropType(e.target.value)}
              className="form-control"
              label="Crop"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <TextField
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              className="form-control"
              label="Address"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <TextField
              value={pincode}
              onChange={(e) => setPincode(e.target.value)}
              className="form-control"
              label="Pincode"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <TextField
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="form-control"
              label="Location"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <TextField
              value={experience}
              onChange={(e) => setExperience(e.target.value)}
              className="form-control"
              label="Experience"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <TextField
              value={premiumRate}
              onChange={(e) => setPremiumRate(e.target.value)}
              className="form-control"
              type='number'
              label="Premium Rate (%)"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <TextField
              value={farmArea}
              onChange={(e) => setFarmArea(e.target.value)}
              className="form-control"
              type='number'
              label="Farm Area (in acres)"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <TextField
              value={expectedYeild}
              onChange={(e) => setExpectedYeild(e.target.value)}
              className="form-control"
              type='number'
              label="Expected Yeild (in qntl/acre)"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <TextField
              value={expectedMarketPrice}
              onChange={(e) => setExpectedMarketPrice(e.target.value)}
              type='number'
              className="form-control"
              label="Expected market price (Rs./Kg)"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <TextField
              value={coveragePeriod}
              onChange={(e) => setCoveragePeriod(e.target.value)}
              className="form-control"
              type='number'
              label="Coverage Period (months)"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            
            <TextField
              value={latitude}
              onChange={(e) => setLatitude(e.target.value)}
              className="form-control"
              label="Latitude"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />            
            <TextField
              value={longitude}
              onChange={(e) => setLongitude(e.target.value)}
              className="form-control"
              label="Longitude"
              fullWidth={true}
              required
            />
            <Box pb={2.5} />
            <Button
              variant="contained"
              color="primary"
              size="large"
              type="submit"
            >
              Add Customer
          </Button>
          </form>
        </Grid>
      </Grid>
    </Container>
  );
}