import * as React from 'react';
import Link from '@mui/material/Link';
import Slider from '@mui/material/Slider';
import PopoverMenu from './PopoverMenu';
import ProTip from './ProTip';
import { styled } from '@mui/system';

import { AppBar, Toolbar, Typography, Container, Box } from '@mui/material';


// 假设这是从外部API或服务获取的动漫数据
const animeData = {
  "index": [
    {
      "id": "1",
      "names": [
        {
          "language_code": "CHS",
          "name": "葬送的芙莉莲"
        }
      ]
    },
    {
      "id": "2",
      "names": [
        {
          "language_code": "CHS",
          "name": "不死不幸"
        }
      ]
    },
    {
      "id": "3",
      "names": [
        {
          "language_code": "CHS",
          "name": "家里蹲吸血姬的苦闷"
        }
      ]
    }
  ]
};
// Custom styled components using MUI's 'styled' utility
const StyledAppBar = styled(AppBar)(({ theme }) => ({
  backgroundColor: theme.palette.background.paper,
  color: theme.palette.text.primary,
}));

const StyledNavLink = styled(Typography)(({ theme }) => ({
  margin: theme.spacing(0, 1),
  cursor: 'pointer',
  '&:hover': {
    textDecoration: 'underline',
  },
}));

const App = () => {
  return (
    <div>
      <StyledAppBar position="static" elevation={0}>
        <Toolbar>
          <Typography variant="h6" color="inherit" noWrap>
            LOGO
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          <StyledNavLink>
            最近更新
          </StyledNavLink>
          <StyledNavLink>
            全部动漫
          </StyledNavLink>
        </Toolbar>
      </StyledAppBar>
      
      <Container maxWidth="lg">
        <Box my={2}>
          {animeData.index.map((anime) => (
            <Typography key={anime.id} variant="body1" className="py-2">
              {anime.names[0].name}
            </Typography>
          ))}
        </Box>
      </Container>
    </div>
  );
};

export default App;
