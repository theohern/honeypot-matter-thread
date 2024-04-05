import React, { useState, useEffect } from 'react';
import './styles.css';

const HomeAssistantWindow = () => {
  /* const [csvData, setCsvData] = useState([]);

  useEffect(() => {
    fetch('/get_homeassistant')  // Assuming Flask server is running on the same host
      .then(response => response.text())
      .then(data => {
        const parsedData = parseCsv(data);
        setCsvData(parsedData);
      })
      .catch(error => {
        console.error('Error fetching CSV:', error);
      });
  }, []);

  const parseCsv = (csv) => {
    const rows = csv.trim().split('\n');
    const headers = rows[0].split(',');
    const parsedData = rows.slice(1).map(row => {
      const rowData = row.split(',');
      return headers.reduce((obj, header, index) => {
        obj[header.trim()] = rowData[index].trim();
        return obj;
      }, {});
    });
    return parsedData;
  }; */


  return (
    <div className="embedded topRight background">
      <strong>This is the Homeassistant Window</strong>
      {/* <table>
        <thead>
          <tr>
            {Object.keys(csvData[0]).map((key, index) => (
              <th key={index}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {csvData.map((row, index) => (
            <tr key={index}>
              {Object.values(row).map((value, index) => (
                <td key={index}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table> */}
    </div>
  );
};

export default HomeAssistantWindow;