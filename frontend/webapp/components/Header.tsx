import React from 'react';
import { makeStyles, Theme } from '@material-ui/core/styles';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Link as LinkText,
  Switch,
} from '@material-ui/core';
import Link from 'next/link';

export default function Header({ darkState, handleThemeChange }) {
  const classes = useStyles();

  const links = [
    { label: 'Customers', href: '/customer' },
    { label: 'Add Customer', href: '/customer/new' },
    { label: 'Sign Out', href: '/' },
  ]
    .filter((link) => link)
    .map(({ label, href }) => {
      return (
        <Link href={href} key={href}>
          <Button color="inherit">{label}</Button>
        </Link>
      );
    });

  return (
    <div className={classes.root}>
      <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" className={classes.title}>
              <Link href="/customer">
                <LinkText href="" color="inherit">
                Dronify Agro Insurance
              </LinkText>
              </Link>
            </Typography>
            <Switch checked={darkState} onChange={handleThemeChange} />
            {links}
          </Toolbar>
      </AppBar>
    </div>
  );
}

const useStyles = makeStyles((theme: Theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
  list: {
    width: 250,
  },
}));