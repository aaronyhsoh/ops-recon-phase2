import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Layout from './Layout';
import reportWebVitals from './reportWebVitals';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import BondCustodyInter from './pages/OpsReconciliation/BondCustodyInter';
import MarginAccount from './pages/OpsReconciliation/MarginAccount';
import MutualFund from './pages/OpsReconciliation/MutualFund';
import BondCustodyClient from './pages/OpsReconciliation/BondCustodyClient';
import CCDCHoldingSetting from './pages/Settings/CCDCHoldingSetting';
import PathSetting from './pages/Settings/PathSetting';
import PlaceHolder1 from './pages/Settings/PlaceHolder1';
import PlaceHolder2 from './pages/Settings/PlaceHolder2';
import ReconcileAll from './pages/OpsReconciliation/ReconcileAll';
import { AppContextProvider } from './contexts/AppContext';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "marginaccount",
        element: <MarginAccount />
      },
      {
        path: "mutualfund",
        element: <MutualFund />
      },
      {
        path: "bondcustodyinter",
        element: <BondCustodyInter />
      },
      {
        path: "bondcustodyclient",
        element: <BondCustodyClient />
      },
      {
        path: "",
        element: <ReconcileAll />
      },
      {
        path: "ccdcholdingsetting",
        element: <CCDCHoldingSetting />
      },
      {
        path: "pathsetting",
        element: <PathSetting />
      },
      {
        path: "placeholder1",
        element: <PlaceHolder1 />
      },
      {
        path: "placeholder2",
        element: <PlaceHolder2 />
      },
    ]
  },
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AppContextProvider>
        <RouterProvider router={router} />
    </AppContextProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
