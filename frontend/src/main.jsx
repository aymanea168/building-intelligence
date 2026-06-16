/**
 * Application Entry Point
 * 
 * Renders the main App component into the root DOM element.
 * Imports global styles and initializes React.
 */

import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";

// Render the App component
createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
