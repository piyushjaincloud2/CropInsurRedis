import grey from "@material-ui/core/colors/grey";
import blue from "@material-ui/core/colors/blue";
import { createMuiTheme } from "@material-ui/core/styles";

const themeDark = createMuiTheme({
  palette: {
    primary: { main: grey[400] },
    secondary: { main: grey[600] },
    type: "dark",
  },
});

const themeLight = createMuiTheme({
  palette: {
    primary: { main: blue[800] },
    secondary: { main: blue[700] },
    type: "light",
  },
});

export { themeDark, themeLight };