import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import Avatar from "@mui/material/Avatar";
import logo from '../android-launchericon-512-512.webp';

const Header = () => {
  return (
    <AppBar position="static" sx={{ width: "100%", backgroundColor: "#3355ff" }}>
      <Toolbar>
        <IconButton edge="start" color="inherit" aria-label="logo" sx={{ mr: 2 }}>
          <Avatar
            src={logo}
            alt="App Logo"
            sx={{ width: 40, height: 40 }}
          />
        </IconButton>

        <Box sx={{ flexGrow: 1, textAlign: "center" }}>
          <Typography variant="h6" component="div" sx={{ fontWeight: "bold" }}>
            Freeze
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
