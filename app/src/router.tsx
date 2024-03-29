import React from "react";
import {
  createBrowserRouter,
} from "react-router-dom";

import { FullBangumiPage } from "./pages/FullBangumiPage"
import { BangumiDataPage } from "./pages/BangumiDataPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <FullBangumiPage />,
  },
  {
    path: "/list",
    element: <FullBangumiPage />,
  },
  {
    path: "/bangumi/:bangumiID",
    element: <BangumiDataPage />,
  },
]);