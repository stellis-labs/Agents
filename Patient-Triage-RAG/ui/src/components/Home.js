// src/components/Home.js
import React, { useState } from 'react';
import './css/Home.css'; // Optional: Create a separate CSS file for Home styles

export default function Home() {
  const [symptoms, setSymptoms] = useState('');
  const [history, setHistory] = useState('');
  const [diagnosis, setDiagnosis] = useState('');
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
  
    try 
    {
      console.log('Sending request to backend with:', { symptoms, history, diagnosis });

      const response = await fetch('http://localhost:8001/assign-triage-level/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symptoms, history, diagnosis }),
      });
  
      console.log('response:', response);
  
      if (!response.ok) {
        throw new Error('Failed to fetch triage report and ', `HTTP error! Status: ${response.status}`);
      }
  
      const data = await response.json();
      setReport(data);
    } catch (error) {
      setError('Error fetching triage report. Please try again.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-container">
      <div className="home-header">
        <h3>Welcome to Patient Triage Dignostic System</h3>
      </div>
      <div className="home-content">
        {/* <h2>Home</h2> */}
        <p>Add the Patient Details below:</p>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="symptoms">Symptoms</label>
            <input 
              type="symptoms" 
              id="symptoms" 
              placeholder="Enter Symptoms"
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
            />
          </div>
          <div className="input-group">
            <label htmlFor="history">History</label>
            <input 
              type="history" 
              id="history" 
              placeholder="Enter Medical History"
              value={history}
              onChange={(e) => setHistory(e.target.value)}
            />
          </div>
          <div className="input-group">
            <label htmlFor="diagnosis">Diagnosis</label>
            <input 
              type="diagnosis" 
              id="diagnosis" 
              placeholder="Enter Preliminary Diagnosis" 
              value={diagnosis} 
              onChange={(e) => setDiagnosis(e.target.value)}
            />
          </div>
          <button className="button" disabled={loading}>
            {loading ? 'Processing...' : 'TRIAGE LEVEL'}
          </button>
        </form>

        {error && <p className="error">{error}</p>}
        
        {report && (
          <div className="report-container">
            <h2>Triage Report</h2>
            <table>
              <thead>
                <tr>
                  <th>Step</th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
                {report.steps.map((step, index) => (
                  <tr key={index}>
                    <td>{step.description}</td>
                    <td>
                      {typeof step.details === 'object' ? (
                        <pre>{JSON.stringify(step.details, null, 2)}</pre>
                      ) : (
                        step.details
                      )}
                    </td>
                  </tr>
                ))}
                <tr>
                  <td>Final Output</td>
                  <td>
                    <strong>Triage Level:</strong> {report.final_output.triage_level}
                    <br />
                    <strong>Explanation:</strong> {report.final_output.explanation}
                  </td>
                </tr>
                <tr>
                  <td>Confidence</td>
                  <td>{report.confidence.toFixed(2)}</td>
                </tr>
                <tr>
                  <td>Guidelines Used</td>
                  <td>
                    <ul>
                      {report.guidelines_used.map((guideline, index) => (
                        <li key={index}>{guideline}</li>
                      ))}
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        )}

        <p className="footer">
          {/* <a href="/forgot-password" className="link">Forgot Password?</a> */}
        </p>

      </div>
    </div>
  );
}