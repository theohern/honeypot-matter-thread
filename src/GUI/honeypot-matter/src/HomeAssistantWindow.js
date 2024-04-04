import React, { useState } from 'react';
import CSVReader from 'react-csv-reader';

const HomeAssistantWindow = () => {
  const [csvData, setCsvData] = useState([]);

  const handleFile = (data) => {
    setCsvData(data);
  };

  return (
    <div className="window homeassistant">
      <strong>This is the Homeassistant Window</strong>
      <CSVReader
        onFileLoaded={handleFile}    
        parserOptions={{ header: true, skipEmptyLines: true }}
      />
      <table>
        <thead>
          <tr>
            <th>Friendly Name</th>
            <th>Change Count</th>
            <th>State Change Count</th>
          </tr>
        </thead>
        <tbody>
          {csvData.map((item, index) => (
            <tr key={index}>
              <td>{item['Friendly Name']}</td>
              <td>{item['Change Count']}</td>
              <td>{item['State Change Count']}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default HomeAssistantWindow;