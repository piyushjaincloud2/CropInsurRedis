import React from 'react';
import Paper from '@material-ui/core/Paper';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import TableContainer from '@material-ui/core/TableContainer';
import Box from '@material-ui/core/Box';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import IconButton from '@material-ui/core/IconButton';
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import ArrowForward from '@material-ui/icons/ArrowForward';
import Link from 'next/link';
import { makeStyles, Theme } from '@material-ui/core/styles';

const useStyles = makeStyles((theme: Theme) => ({

  root: {
    width: '100%',
    padding: theme.spacing(3)
  },
  paper: {
    width: '100%',
    margin: theme.spacing(8, 0),
  },
  visuallyHidden: {
    border: 0,
    clip: 'rect(0 0 0 0)',
    height: 1,
    margin: -1,
    overflow: 'hidden',
    padding: 0,
    position: 'absolute',
    top: 20,
    width: 1,
  },
  table: {
    maxWidth: '100%',
    overflow: 'hidden'
  },
  image: {
    maxWidth: '100px',
    maxHeight: '100px',
    outline: '4px solid black',
    padding: '2px',
  },
  noContentMsg: {
    display:'grid',
    placeItems:'center',
    minHeight: theme.spacing(10),
    marginTop:theme.spacing(3) 
  }
}));

const InspectionTable = ({ customerId, list, policyAssociated, isInspectionPage = false }) => {
  const classes = useStyles();
  const policyLink = ({customerId, }) => {
    return <Link href={`/customer/${customerId}/policy/${policyAssociated}`}>{policyAssociated}</Link>
  }
  const rows: any = list && list.sort((a:any, b:any)=> (new Date(b.Timestamp) > new Date(a.Timestamp))? 1 : -1 )
    .reduce((acc: any, item: any) => {
    const data = {
      inspectionId: item.id,
      IDV: item.postHarvestIdv || item.preHarvestIdv,
      policy: policyLink(item)
    }
    acc.push(data)
    return acc;
  }, []) || [];



  return (
    <Paper className={isInspectionPage && classes.paper} elevation={0}>
      <Container className={classes.root}>
        <Typography variant="h4" id="tableTitle" component="h3">
          Inspection History
        </Typography>
        {list && list.length > 0 ?
          <TableContainer>
            <Table className={classes.table} aria-label="simple table">
              <TableHead>
                <TableRow>
                  {rows && rows[0] && Object.keys(rows[0]).map((_key, index) => (
                    <TableCell align={index === 0 ? 'left' : 'center'}>{_key.toUpperCase()}</TableCell>
                  ))}
                  <TableCell align='center'>Details</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map((row) => (
                  <TableRow key={row.name}>
                    {Object.values(row).map((_value, index) => (
                      <TableCell component="th" scope="row" align={index === 0 ? 'left' : 'center'}>
                        {_value}
                      </TableCell>)
                    )}
                    <TableCell align="right">
                      <Link href={`/customer/${customerId}/inspection/${row.inspectionId}`}>
                        <IconButton><ArrowForward /></IconButton>
                      </Link>
                    </TableCell>
                  </TableRow>

                ))}
              </TableBody>
            </Table>
          </TableContainer>
          :
          <Box className={classes.noContentMsg}>
            <ErrorOutlineIcon color="primary" fontSize='large'/>
            <Typography variant="h6" id="tableTitle" component="span">
              No Records Found
            </Typography>
          </Box>}
      </Container>
    </Paper>
  );
}
export default InspectionTable