import React from 'react'
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';

function PersonalInfo({
  email, age, gender, mobile, address, location, experience, properties
}) {
  const cropType = properties && properties[0]?.cropName;
  return (
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
              Personal Information
            </Typography>
          </Grid>
          <Grid item md={4} xs={6}>
            <Typography
              component="p"
              variant="inherit"
              color="inherit"
              gutterBottom
            >
              Email
            </Typography>
            <Typography
              component="p"
              variant="h6"
              color="inherit"
              gutterBottom
            >
              {email}
            </Typography>
          </Grid>
        
          <Grid item md={4} xs={6}>
            <Typography
              component="p"
              variant="inherit"
              color="inherit"
              gutterBottom
            >
              Age
            </Typography>
            <Typography
              component="p"
              variant="h6"
              color="inherit"
              gutterBottom
            >
              {age}
            </Typography>
          </Grid>
        
          <Grid item md={4} xs={6}>
            <Typography
              component="p"
              variant="inherit"
              color="inherit"
              gutterBottom
            >
              Gender
            </Typography>
            <Typography
              component="p"
              variant="h6"
              color="inherit"
              gutterBottom
            >
              {gender}
            </Typography>
          </Grid>


          <Grid item md={4} xs={6}>
            <Typography
              component="p"
              variant="inherit"
              color="inherit"
              gutterBottom
            >
              Mobile
            </Typography>
            <Typography
              component="p"
              variant="h6"
              color="inherit"
              gutterBottom
            >
              {mobile}
            </Typography>
          </Grid>
       
       
          <Grid item md={4} xs={6}>
            <Typography
              component="p"
              variant="inherit"
              color="inherit"
              gutterBottom
            >
              Location
            </Typography>
            <Typography
              component="p"
              variant="h6"
              color="inherit"
              gutterBottom
            >
              {location}
            </Typography>
          </Grid>
        
        
          <Grid item md={4} xs={6}>
            <Typography
              component="p"
              variant="inherit"
              color="inherit"
              gutterBottom
            >
              Address
            </Typography>
            <Typography
              component="p"
              variant="h6"
              color="inherit"
              gutterBottom
            >
              {address}
            </Typography>
          </Grid>
        
          <Grid item md={4} xs={6}>
            <Typography
              component="p"
              variant="inherit"
              color="inherit"
              gutterBottom
            >
              Experience
            </Typography>
            <Typography
              component="p"
              variant="h6"
              color="inherit"
              gutterBottom
            >
              {experience}
            </Typography>
          </Grid>
        
        
          <Grid item md={4} xs={6}>
            <Typography
              component="p"
              variant="inherit"
              color="inherit"
              gutterBottom
            >
              Type of Crop
            </Typography>
            <Typography
              component="p"
              variant="h6"
              color="inherit"
              gutterBottom
            >
              {cropType}
            </Typography>
          </Grid>
        </Grid>
      </Container>
    </Box>
  )
}

export default PersonalInfo
