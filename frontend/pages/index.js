import * as React from 'react';
import {useState} from 'react';
import {LocalizationProvider} from '@mui/x-date-pickers/LocalizationProvider';
import {AdapterDayjs} from '@mui/x-date-pickers/AdapterDayjs';
import {Box, Container, Paper, Typography} from "@mui/material";
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import DateFilter from "../components/DateFilter";


const defaultOptions = {
  chart: {
    type: 'line',
    backgroundColor: '#f8f8f8',
    options3d: {
      enabled: true,
      alpha: 15,
      beta: 30,
      depth: 300,
    },
  },
  tooltip: {
    pointFormat: '<b>{series.options.custom.code}:</b> {series.options.custom.symbol} {point.y:.2f}<br/>',
    shared: true,
  },
  title: {
    text: "Cotação baseada no Dolar ($)",
  },
  yAxis: {
    type: 'logarithmic',
    title: {
      text: 'Moeda X Dolar ($)',
    },
    tickInterval: 1,
    lineWidth: 2,
    offset: 20,
  },
  xAxis: [{
    type: 'datetime',
    title: {
      text: 'Data'
    },
    offset: 20,
    tickWidth: 1,
    labels: {
      format: '{value:%d %b %Y}',
    },
    dateTimeLabelFormats: {
      day: '%d %b %Y',
      week: '%d %b %Y',
      month: '%b %Y',
      year: '%Y'
    }
  }],
  plotOptions: {
    line: {
      dataLabels: {
        enabled: true,
        format: '{series.options.custom.symbol} {point.y:.2f}'
      },
      depth: 100
    }
  },
  series: [{name: "", data: []}],
  credits: {
    enabled: false,
  },
}

export default function Home() {
  const [chartOptions, setChartOptions] = useState(defaultOptions);

  const retrieveApiData = async (startDate, endDate, setError) => {
    console.log(startDate);
    console.log(endDate);

    const startDateString = startDate?.toISOString().split('T')[0];
    const endDateString = endDate?.toISOString().split('T')[0];

    const mapApiResponse = (data) => {
      console.log(data)
      let series = []
      Object.entries(data.currencies).map(([currency, obj]) => {
        if (currency === "USD") return

        series.push({
          name: obj.name,
          xAxis: 0,
          custom: {
            code: obj.code,
            symbol: obj.symbol,
          },
          data: data.results.map((result) => {
            const rates = result.rates;
            const dateParts = result.date.split('-');
            const year = parseInt(dateParts[0]);
            const month = parseInt(dateParts[1]) - 1;
            const day = parseInt(dateParts[2]);
            return [Date.UTC(year, month, day), parseFloat(rates[currency])]
          })
        })
      })
      console.log(series);
      setChartOptions({...chartOptions, series: series});
    }

    let response = await fetch(
      `http://localhost:8000/api/rates/?start_date=${startDateString}&end_date=${endDateString}&currencies=true`
    )
    let data = await response.json();
    if (response.status === 400) {
      console.log("resposta é 400");
      setError(data);
    } else {
      setError(null);
      mapApiResponse(data);
    }
  }

  return (
    <Box display="flex" justifyContent="center" alignItems="center" height="100vh" width="100vw">
      <Paper elevation={10} style={{padding: 20}}>
        <Box display="flex" justifyContent="center">
          <Typography variant="h2" gutterBottom>
            Currency Quote
          </Typography>
        </Box>
        <Box display="flex" justifyContent="center" alignItems="center" height="80vh" width="80vw">
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <Container maxWidth="xl" style={{display: 'flex'}}>
              <Container maxWidth="md" style={{flex: 2}}>
                <HighchartsReact highcharts={Highcharts} options={chartOptions}/>
              </Container>
              <Container maxWidth="sm" style={{flex: 1}}>
                <Box display="flex" justifyContent="center" alignItems="center" height="100%">
                  <DateFilter handleApplyFilters={retrieveApiData}/>
                </Box>
              </Container>
            </Container>
          </LocalizationProvider>
        </Box>
      </Paper>
    </Box>
  )
}
