import logo from './logo.svg';
import Navigation from './nav/Navigation.js'
import './App.css';
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'

library.add(fas);

function App() {
  return (
    <div className="App">
      <script src="https://kit.fontawesome.com/8b0c2202e4.js" crossorigin="anonymous"></script>
      <Navigation/>
    </div>
  );
}

export default App;
