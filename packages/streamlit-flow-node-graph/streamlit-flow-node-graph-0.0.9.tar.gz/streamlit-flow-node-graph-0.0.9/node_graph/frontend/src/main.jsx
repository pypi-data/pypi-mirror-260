import React from "react"
import ReactDOM from "react-dom"
import { StreamlitProvider } from "streamlit-component-lib-react-hooks"
import App from "./MyComponent"
import "./index.css"
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <StreamlitProvider>
      <App />
    </StreamlitProvider>
  </React.StrictMode>,
)