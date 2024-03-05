import React, { Suspense, lazy } from 'react';
import { HashRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import "./App.css";
const Login = lazy(() => import("./auth/Login"));
const Chat = lazy(() => import("./components/chat/Chat"));
const Details = lazy(() => import("./components/chat/Details"));


function Authorization() {
    const user = JSON.parse(localStorage.getItem('komodoUser'))
    return user?.email !== null && user?.email !== undefined && user?.email !== "" ? <Outlet /> : <Navigate to={"/login"} />
}

function App() {
    return (
        <Router>
            <Suspense
                fallback={
                    <></>
                }
            >
                <Routes>
                    <Route path="/" strict >
                        <Route index element={<Login />} />
                        <Route path="/login" strict element={<Login />} />
                    </Route>
                    <Route element={<Authorization />}>
                        <Route path="/chat" element={<Chat />} />
                        <Route path="/details/:id" element={<Details />} />
                    </Route>
                </Routes>
            </Suspense>
        </Router>
    );
}

export default App;
