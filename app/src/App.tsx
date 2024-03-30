import * as React from 'react';

import { styled } from '@mui/system';

import { AppBar, Toolbar, Typography, Link, Box, Container, Stack } from '@mui/material';

import {
  RouterProvider,
} from "react-router-dom";

import { router } from "./router";


// Custom styled components using MUI's 'styled' utility
const StyledAppBar = styled(AppBar)(({ theme }) => ({
  backgroundColor: 'rgba(255,185,179,0.6)',//theme.palette.background.paper,
  color: theme.palette.text.primary,
}));

const App = () => {
  return (
    <div>
      <StyledAppBar position="static" elevation={0}>
        <Toolbar sx={{ color: 'rgb(138, 54, 49)' }}>

          <Box
            sx={{
              width: 64,
              height: 64,
              borderRadius: 1,
            }}
          >
            <img
              src="/anime_logo_transparent.png"
              width='100%'
            />
          </Box>
          
          <Typography variant="h6" color="inherit" noWrap my={0} py={0}>
            <Link href="/" underline="hover" color="inherit" mx={1}>
              Bangumi Link
            </Link>
          </Typography>

          <Box sx={{ flexGrow: 1 }} />

          <Link href="/" underline="hover" color="inherit" mx={1}>
            Updates
          </Link>
          <Link href="/" underline="hover" color="inherit" mx={1}>
            Home
          </Link>
        </Toolbar>
      </StyledAppBar>
      <Box mb={2}></Box>
      <RouterProvider router={router} />
    </div>
  );
};

export default App;
