import Typography from '@material-ui/core/Typography';
import Link from 'next/link';
import Button from '@material-ui/core/Button';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { makeStyles} from '@material-ui/core/styles';

import { useAuth } from 'lib/useAuth';

export default function Hero({
  title, subtext, ctalink, ctaSecLink = null
}) {
  const classes = useStyles()
  const { user = { emial: 'none', policyId: 'someid' } } = useAuth();

  return (
    <Paper className={classes.mainFeaturedPost}>
      <div className={classes.overlay} />
      <Grid container>
        <Grid item md={6}>
          <div className={classes.mainFeaturedPostContent}>
            <Typography
              component="h1"
              variant="h3"
              color="inherit"
              gutterBottom
            >
              {title}
            </Typography>
            <Typography variant="h5" color="inherit" paragraph>
              {subtext}
            </Typography>
            <Box pb={1} />
            <Link href={`${ctalink?.url}`}>
              <Button variant="outlined" color="inherit">
              {ctalink?.label}
                </Button>
            </Link>

            {ctaSecLink && <Link href={`${ctaSecLink?.url}`}>
              <Button variant="outlined" color="inherit" className={classes.secondary}>
              {ctaSecLink?.label}
                </Button>
            </Link>}
          </div>
        </Grid>
      </Grid>
    </Paper>
  );
}

const useStyles = makeStyles((theme) => ({
  toolbar: {
    borderBottom: `1px solid ${theme.palette.divider}`,
  },
  toolbarTitle: {
    flex: 1,
  },
  mainFeaturedPost: {
    position: 'relative',
    backgroundColor: theme.palette.grey[800],
    color: theme.palette.common.white,
    marginBottom: theme.spacing(2),
    backgroundImage: 'url(https://source.unsplash.com/featured/?farms)',
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
  },
  overlay: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    right: 0,
    left: 0,
    backgroundColor: 'rgba(0,0,0,.7)',
  },
  mainFeaturedPostContent: {
    position: 'relative',
    padding: theme.spacing(3),
    [theme.breakpoints.up('md')]: {
      padding: theme.spacing(6),
      paddingRight: 0,
    },
  },
  secondary:{ 
    marginLeft:theme.spacing(2)
  }
}));