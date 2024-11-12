import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Home from "./pages/Home";
import LoginForm from "./pages/LoginForm";
import SignUpForm from "./pages/SignUpForm";
import VoteFilm from "./pages/VoteFilm";
import { AuthProvider } from "./context/AuthContext";
import "./App.css";



export default function App() {
  return (
    

      <BrowserRouter>
      <AuthProvider>
            <div id="app">
              <main id="main-content">
                <Routes>
                  <Route
                    path="/"
                    element={<LoginForm />}
                  />
                  <Route
                    path="/home"
                    element={<Home />}
                  />
                  <Route
                    path="/signUp"
                    element={<SignUpForm />}
                  />
                  <Route
                    path="/vote"
                    element={<VoteFilm />}
                  />
                </Routes>
              </main>
            </div>
          </AuthProvider>  
      </BrowserRouter>
      
  );
}
