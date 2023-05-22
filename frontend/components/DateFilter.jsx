import React, {useState} from 'react';
import {Alert, Button, Grid, TextField} from '@mui/material';
import {DatePicker} from '@mui/x-date-pickers/DatePicker';

const DateFilter = ({handleApplyFilters}) => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [error, setError] = useState(null);

  const handleStartDateChange = (date) => {
    setStartDate(date);
    // Ensure that the selected end date is not lower than the start date
    if (endDate !== null && date > endDate) {
      setEndDate(date);
    }
  };

  const handleEndDateChange = (date) => {
    // Ensure that the selected end date is not lower than the start date
    if (startDate !== null && date < startDate) {
      setStartDate(date);
    }
    setEndDate(date);
  };

  const buttonOnClick = () => {
    handleApplyFilters(startDate, endDate, setError);
  }

  return (<Grid container spacing={2} alignItems="center">
      <Grid item>
        <DatePicker
          label="Data Inicial"
          value={startDate}
          onChange={handleStartDateChange}
          renderInput={(params) => <TextField {...params} />}
          disableFuture
        />
      </Grid>
      <Grid item>
        <DatePicker
          label="Data Final"
          value={endDate}
          onChange={handleEndDateChange}
          renderInput={(params) => <TextField {...params} />}
          disableFuture
        />
      </Grid>
      <Grid item>
        <Grid container justifyContent="flex-end">
          <Button variant="contained" onClick={buttonOnClick}>
            Aplicar
          </Button>
        </Grid>
      </Grid>
      {error && (<Grid item xs={12}>
          <Alert severity="error">{Object.values(error)}</Alert>
        </Grid>)}
    </Grid>);
};

export default DateFilter;
