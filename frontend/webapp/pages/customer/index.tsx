import React, { useEffect, useState } from 'react';
import { createStyles, Theme, makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';
import Grid from '@material-ui/core/Grid';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import IconButton from '@material-ui/core/IconButton';
import Box from '@material-ui/core/Box';
import ArrowForward from '@material-ui/icons/ArrowForward';
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import Typography from '@material-ui/core/Typography';
import Link from 'next/link';
import { useCustomerStorage } from 'lib/useCustomerData';

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      width: '100%',
      minWidth: '70vw',
      maxHeight: 'calc(80vh - 64px)',
      overflow: 'auto',
    },
    inline: {
      display: 'inline',
    },
    bottemGap: {
      marginBottom: theme.spacing(4)
    },
    noContentMsg: {
      display: 'grid',
      placeItems: 'center',
      minHeight: theme.spacing(10),
      marginTop: theme.spacing(3)
    }
  }),
);

export default function Customer() {
  const classes = useStyles();
  const { data, fetchAll } = useCustomerStorage();

  const [newCustomer, setNewCustomer] = useState(null)
  const [policyHolders, setPolicyHolders] = useState(null)
  useEffect(() => {
    fetchAll()
  }, [])

  useEffect(() => {
    if (data) {
      console.log(data);
      
      setNewCustomer(data.filter((c: any) => c?.properties?.find((prop: any) => !prop?.policy?.id)))
      setPolicyHolders(data.filter((c: any) => c?.properties?.find((prop: any) => prop?.policy?.id)))
      // setPolicyHolders(data.filter((c: any) => !!c.policyAssociated))
      console.log(data);
    }
  }, [data])
  useEffect(() => {
    console.log(newCustomer, policyHolders);

  }, [newCustomer, policyHolders])

  const noData = () => {
    return (<Box className={classes.noContentMsg}>
      <ErrorOutlineIcon fontSize="large" color="primary" />
      <Typography variant="h6" id="tableTitle" component="span">
        No Data found
        </Typography>
    </Box>)
  }
  return (<Grid container
    spacing={0}
    direction="column"
    style={{ minHeight: 'calc(100vh - 64px)', padding: '64px' }}>
    <Box className={classes.bottemGap}>
      <Typography variant="h4">Prospect Customer</Typography>
      {(!newCustomer || newCustomer.length === 0) && noData()}
      <List className={classes.root}>
        {newCustomer && newCustomer.map((item, index) =>
          <Box key={item.id}>
            <ListItem alignItems="flex-start" key={item.id}>
              <ListItemAvatar>
                <Avatar alt={item.name} src={item.avtar} />
              </ListItemAvatar>
              <ListItemText
                primary={item.name}
                secondary={
                  <Typography
                    component="span"
                    variant="body2"
                    className={classes.inline}
                  >
                    {item.id}
                  </Typography>
                }
              />
              <ListItemSecondaryAction>
                <Link href={`customer/${item.id}`}>
                  <IconButton edge="end" aria-label="comments">
                    <ArrowForward />
                  </IconButton>
                </Link>
              </ListItemSecondaryAction>
            </ListItem>
            {((newCustomer.length - 1) !== index) ? <Divider variant="inset" component="li" /> : null}
          </Box>
        )}
      </List>
    </Box>
    <Box>
      <Typography variant="h4">Policyholders</Typography>
      <List className={classes.root}>
        {(!policyHolders || policyHolders.length === 0) && noData()}
        {policyHolders && policyHolders.map((item, index) =>
          <>
            <ListItem alignItems="flex-start">
              <ListItemAvatar>
                <Avatar alt={item.name} src={item.avtar} />
              </ListItemAvatar>
              <ListItemText
                primary={item.name}
                secondary={
                  <Typography
                    component="span"
                    variant="body2"
                    className={classes.inline}
                    color="textPrimary"
                  >
                    {item.id}
                  </Typography>
                }
              />
              <Link href={`customer/${item.id}`}>
                <ListItemSecondaryAction>
                  <IconButton edge="end" aria-label="comments">
                    <ArrowForward />
                  </IconButton>
                </ListItemSecondaryAction>
              </Link>
            </ListItem>
            {((policyHolders.length - 1) !== index) ? <Divider variant="inset" component="li" /> : null}
          </>
        )}
      </List>
    </Box>
  </Grid>
  );
}