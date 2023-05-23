import logo from './logo.svg';
import './App.css';
import {
  BrowserRouter,
  Routes,
  Route,
  Outlet,
  Link,
  useLocation
} from "react-router-dom";
import { noTokenRequest } from './http';

function App() {
  function test() {
    noTokenRequest.get('/test', {
    }).then((res) => {
      console.log('res.data.data');
    })
  }
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" onClick={test} />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <button onClick={test}>testAPI</button>
    </div>
  );
}

export default App;
