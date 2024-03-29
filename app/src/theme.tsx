import { createTheme, ThemeProvider } from '@mui/material/styles';
import * as ReactDOM from 'react-dom/client';

declare module '@mui/material/styles' {
    interface Palette {
        pink: Palette['primary'];
    }

    interface PaletteOptions {
        pink?: PaletteOptions['primary'];
    }
}

declare module '@mui/material/Button' {
    interface ButtonPropsColorOverrides {
        pink: true;
    }
}

declare module '@mui/material/IconButton' {
    interface IconButtonPropsColorOverrides {
        pink: true;
    }
}

declare module '@mui/material/Switch' {
    interface SwitchPropsColorOverrides {
        pink: true;
    }
}


const rootElement = document.getElementById('root');

// All `Portal`-related components need to have the the main app wrapper element as a container
// so that the are in the subtree under the element used in the `important` option of the Tailwind's config.
let baseTheme = createTheme({
    components: {
        MuiPopover: {
            defaultProps: {
                container: rootElement,
            },
        },
        MuiPopper: {
            defaultProps: {
                container: rootElement,
            },
        },
    },
});

export const theme = createTheme(baseTheme, {
    // Custom colors created with augmentColor go here
    palette: {
        pink: baseTheme.palette.augmentColor({
            color: {
                main: '#ff9b92',
            },
            name: 'pink',
        }),
    },
});