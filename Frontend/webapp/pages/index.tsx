import { useState } from 'react';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import { useAuth } from 'lib/useAuth';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  cover: {
    backgroundImage: 'url(https://images.unsplash.com/photo-1573744271804-5bbfe6ee19da?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&dl=ali-yilmaz-hbYrBY8eVMc-unsplash.jpg)',    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
  }
}))

export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { error, signIn } = useAuth();

  const onSubmit = async (event) => {
    event.preventDefault();
    signIn(email, password);
  };
  //

  const styles = useStyles();
  return (
    <Box >
      <Grid container
        className={styles.cover}
        spacing={0}
        direction="column"
        alignItems="center"
        justify="center"
        style={{ minHeight: 'calc(100vh)' }}>
        <Paper elevation={9} style={{ padding: '64px' }}>
          <form onSubmit={onSubmit}>
            {error && <p>{error}</p>}
            <Typography variant="h3">Dronify Agro Insurance</Typography>
            <Typography variant="h6" color="primary">Insurer portal</Typography>
            <Box pb={5} />
            <Typography variant="h5">Sign In</Typography>
            <Box pb={1} />
            <TextField
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="form-control"
              label="Email"
              fullWidth={true}
              required
              />
            <Box pb={2.5} />
            <TextField
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              fullWidth={true}
              className="form-control"
              label="Password"
              required
            />
            <Box pb={2.5} />
            <Button
              variant="contained"
              color="primary"
              size="large"
              type="submit"
            >
              Sign In
          </Button>
          </form>
        </Paper>
      </Grid>
    </Box>
  );
}