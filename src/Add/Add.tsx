import React, { useState } from "react";
import { Box, Button, MenuItem, TextField, Typography, Stack } from "@mui/material";
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import Header from "../components/Header";
import { useNavigate } from "react-router-dom";
import dayjs from 'dayjs';

const ProductForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    category: "",
    amount: "",
    location: "",
    freezingDate: null,
    bestBefore: null,
  });

  const navigate = useNavigate();

  const handleChange = (field: string) => (event: { target: { value: any; }; }) => {
    setFormData({ ...formData, [field]: event.target.value });
  };

  const handleDateChange = (field: string) => (date: any) => {
    setFormData({ ...formData, [field]: date });
  };

  const handleSubmit = async (event: { preventDefault: () => void; }) => {
    event.preventDefault();
    const formattedData = {
      ...formData,
      freezingDate: formData.freezingDate ? dayjs(formData.freezingDate).format('DD-MM-YYYY') : null,
      bestBefore: formData.bestBefore ? dayjs(formData.bestBefore).format('DD-MM-YYYY') : null,
    };
    console.log("Form Data:", formattedData);
    try {
        const response = await fetch('http://localhost:5000/product', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formattedData),
        });
  
        if (response.ok) {
          console.log('Product created successfully');
          navigate('/');
        } else {
          console.error('Failed to create product');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
    <Header/>
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          maxWidth: 400,
          margin: "auto",
          padding: 3,
          border: "1px solid #ddd",
          borderRadius: 2,
          boxShadow: 2,
          backgroundColor: "#fff",
        }}>
        <Typography variant="h6" sx={{ mb: 2, textAlign: "center" }}>
          Produkt hinzufügen
        </Typography>
        <Stack spacing={2}>
          <TextField
            label="Name"
            variant="outlined"
            fullWidth
            value={formData.name}
            onChange={handleChange("name")}
            required />
          <TextField
            label="Kategorie"
            variant="outlined"
            select
            fullWidth
            value={formData.category}
            onChange={handleChange("category")}
            required>
            {["Fleisch", "Fisch", "Gemüse", "Früchte", "Brot", "Sonstiges"].map(
              (option) => (
                <MenuItem key={option} value={option}>
                  {option}
                </MenuItem>
              )
            )}
          </TextField>
          <TextField
            label="Menge"
            variant="outlined"
            fullWidth
            value={formData.amount}
            onChange={handleChange("amount")}
            required />
          <TextField
            label="Lagerort"
            variant="outlined"
            fullWidth
            value={formData.location}
            onChange={handleChange("location")} />
          <DatePicker
            label="Einfrierdatum"
            value={formData.freezingDate}
            format="DD-MM-YYYY"
            onChange={handleDateChange("freezingDate")} />
          <DatePicker
            label="Haltbarkeitsdatum"
            value={formData.bestBefore}
            format="DD-MM-YYYY"
            onChange={handleDateChange("bestBefore")} />
          <Button variant="contained" onClick={() => {navigate('/');}} sx={{ mb: 2 }}>Zurück</Button>
          <Button type="submit" variant="contained" color="primary" fullWidth>Speichern</Button>
        </Stack>
      </Box>
    </LocalizationProvider>
  );
};

export default ProductForm;