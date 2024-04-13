import React from "react";
import {
  createBrowserRouter,
} from "react-router-dom";

import { FullBangumiPage } from "./pages/FullBangumiPage"
import { BangumiDataPage } from "./pages/BangumiDataPage";
import { RecentUpdatesPage } from "./pages/RecentUpdatesPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <RecentUpdatesPage />,
  },
  {
    path: "/archieve",
    element: <FullBangumiPage />,
  },
  {
    path: "/updates",
    element: <RecentUpdatesPage />,
  },
  {
    path: "/bangumi/:bangumiID",
    element: <BangumiDataPage />,
  },
]);