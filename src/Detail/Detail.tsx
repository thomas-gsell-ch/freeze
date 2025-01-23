import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { TextField, Typography, Box, Button, MenuItem } from '@mui/material';
import Header from '../components/Header';
import dayjs from 'dayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
//import customParseFormat from 'dayjs/plugin/customParseFormat';

//dayjs.extend(customParseFormat); // Plugin für benutzerdefinierte Formate aktivieren
//dayjs.locale('de'); // Lokalisierung auf Deutsch setzen



const Detail: React.FC = () => {
    const location = useLocation();
    const { id, name, category, amount, location: loc, freezingDate, bestBefore } = location.state || {};
    const [isEditMode, setIsEditMode] = useState(false); // Startet mit Bearbeiten-Modus deaktiviert
    //const [isEditMode, setIsEditMode] = useState(true);

    const [localName, setLocalName] = useState(name || "");
    const [localCategory, setLocalCategory] = useState(category || "");
    const [localAmount, setLocalAmount] = useState(amount || "");
    const [localLoc, setLocalLoc] = useState(loc || "");
    //const [localLoc, setLocalLoc] = useState(loc || "");
    const [localFreezingDate, setLocalFreezingDate] = useState(freezingDate || "");
    const [localBestBefore, setLocalBestBefore] = useState(bestBefore || "");

    const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setLocalName(event.target.value);
        handleInputChange(event);
    };

    const handleCategoryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setLocalCategory(event.target.value);
      handleInputChange(event);
    };

    const handleAmountChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setLocalAmount(event.target.value);
      handleInputChange(event);
    };

    const handleLocChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setLocalLoc(event.target.value);
      handleInputChange(event);
    };



    const handleFreezingDateChange = (field: string) => (date: any) => {
      const formattedDate = dayjs(date).format('DD-MM-YYYY');
      console.log("The freezing Date after change is: ", formattedDate);      
      setLocalFreezingDate(formattedDate);
      console.log("The freezing Date field is: ", field);
      handleDateChange(field)(date);
    };

    const handleBestBeforeChange = (field: string) => (date: any) => {
      const formattedDate = dayjs(date).format('DD-MM-YYYY');
      setLocalBestBefore(formattedDate);
      handleDateChange(field)(date);
    };

    const handleDateChange = (field: string) => (date: any) => {
      setFormData({ ...formData, [field]: date });
    };

    const navigate = useNavigate();

    const [formData, setFormData] = useState({
      name: localName || '',
      category: localCategory || '',
      amount: localAmount || '',
      location: localLoc || '',
      freezingDate: localFreezingDate || '',
      bestBefore: localBestBefore || '',
    });

    //const handleChange = (field: string) => (event: { target: { value: any; }; }) => {
      //console.debug("handleChange called.")
    //  setFormData({ ...formData, [field]: event.target.value });
    //};

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      console.log("handleInputChange called.")
      const { name, value } = event.target;
      setFormData((prevData) => ({
          ...prevData,
          [name]: value,
      }));
    };

    //Auslagern der Entscheidungsfunktion in welchem Modus der Zweifach verwendete Button ist.
    const handleDualUseButtonClicked = async (event: { preventDefault: () => void; }) => {
      isEditMode ? handleUpdate(event) : handleEditClick();
    }

    //Der Benutzer möchte in den Bearbeiten Modus wechseln
    const handleEditClick = () => {
      console.log("handleEditClick called.")
        setIsEditMode(!isEditMode);
    };
      
    //Der Benutzer möchte seine Änderungen abspeichern.
    const handleUpdate = async (event: { preventDefault: () => void; }) => {
 
      event.preventDefault();
        const formattedData = {
            ...formData,
            //freezingDate: formData.freezingDate ? dayjs(formData.freezingDate).format('DD-MM-YYYY') : null,
            //bestBefore: formData.bestBefore ? dayjs(formData.bestBefore).format('DD-MM-YYYY') : null,
            freezingDate: formData.freezingDate ? localFreezingDate : null,
            bestBefore: formData.bestBefore ? localBestBefore : null,
        };

        //const formattedData = {
        //  ...formData,
        //  freezingDate: formData.freezingDate ? dayjs(formData.freezingDate).format('DD-MM-YYYY') : localFreezingDate,
        //  bestBefore: formData.bestBefore ? dayjs(formData.bestBefore).format('DD-MM-YYYY') : localBestBefore,
        //};
    
        console.log("Die ID des Datensatzes:", id);
        console.log("Updated Data:", JSON.stringify(formattedData));
    
        try {
            const response = await fetch(`http://localhost:5000/product/${id}`, { // Hier PUT verwenden
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                
                body: JSON.stringify(formattedData),
            });
    
            if (response.ok) {
                console.log('Product updated successfully');
                setIsEditMode(false); // Nach erfolgreichem Update Bearbeiten-Modus verlassen
            } else {
                console.error('Failed to update product');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };
  
    return (
      
      <div className="App">
        <Header />
        <Typography variant="h6" component="h1" gutterBottom sx={{ flex: '1 1 100%', mt: 1 }}>
          Detail
        </Typography>
        <Box component="form" noValidate autoComplete="off">
          <TextField
            label="Name"
            name="name"
            value={localName}
            
            onChange={handleNameChange}
            slotProps={{
              input: {
                readOnly: !isEditMode,
              },
            }}
            fullWidth
            margin="normal"
            variant="outlined"
            sx={{ mx: 2, maxWidth: 380 }}
          />
          <TextField
            label="Kategorie"
            name="category"
            value={localCategory}
            onChange={handleCategoryChange}
            slotProps={{
              input: {
                readOnly: !isEditMode,
              },
            }}
            select
            fullWidth
            margin="normal"
            variant="outlined"
            sx={{ mx: 2, maxWidth: 380, textAlign: "left" }}
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
            name="amount"
            value={localAmount}
            onChange={handleAmountChange}
            slotProps={{
              input: {
                readOnly: !isEditMode,
              },
            }}
            fullWidth
            margin="normal"
            variant="outlined"
            sx={{ mx: 2, maxWidth: 380 }}
          />
          <TextField
            label="Lagerort"
            
            // name="loc" 
            name="location"

            value={localLoc}
            onChange={handleLocChange}
            slotProps={{
              input: {
                readOnly: !isEditMode,
              },
            }}
            fullWidth
            margin="normal"
            variant="outlined"
            sx={{ mx: 2, maxWidth: 380 }}
          />

          <LocalizationProvider dateAdapter={AdapterDayjs}>
          {/*<TextField
            label="Einfrierdatum"
            name="localFreezingDate"
            value={localFreezingDate}
            onChange={handleFreezingDateChange}
            slotProps={{
              input: {
                readOnly: !isEditMode,
              },
            }}
            fullWidth
            margin="normal"
            variant="outlined"
            sx={{ mx: 2, maxWidth: 380 }}
          />*/}
          
          <DatePicker
            label="Einfrierdatum"
            value={dayjs(localFreezingDate, "DD-MM-YYYY")}
            //value={localFreezingDate}
            format="DD-MM-YYYY"
            //dateFormat="DD-MM-YYYY"
            
            onChange={handleFreezingDateChange("freezingDate")}
            //onChange={handleDateChange("localFreezingDate")}

            disabled={!isEditMode}
            slotProps={{
              textField: {
                sx: { my: 2, mx: 2, width: '100%', maxWidth: '380px'}, // Setzt die Breite auf 100% des Containers
              },
            }}
            sx={{ mx: 2, maxWidth: 380 }}
          />
          
          {/*<TextField
            label="Haltbarkeitsdatum"
            name="localBestBefore"
            value={localBestBefore}
            onChange={handleBestBeforeChange}
            slotProps={{
              input: {
                readOnly: !isEditMode,
              },
            }}
            fullWidth
            margin="normal"
            variant="outlined"
            sx={{ mx: 2, maxWidth: 380 }}
          /> */}
          <DatePicker
            label="Haltbarkeitsdatum"
            value={dayjs(localBestBefore, "DD-MM-YYYY")}
            format="DD-MM-YYYY"
            onChange={handleBestBeforeChange("bestBefore")}
            // onChange={handleDateChange("localBestBefore")}
            disabled={!isEditMode}
            slotProps={{
              textField: {
                sx: { my: 2, mx: 2, width: '100%', maxWidth: '380px'}, // Setzt die Breite auf 100% des Containers
              },
            }}
            sx={{ mx: 2, maxWidth: 380 }}
          />

          </LocalizationProvider>
        </Box>
        <Button variant="contained" onClick={() => {navigate('/');}} sx={{ mb: 2 }}>Zurück</Button>
        {/* <Button variant="contained" onClick={handleEditClick} sx={{ ml: 2, mb: 2 }}>
          {isEditMode ? 'Speichern' : 'Bearbeiten'} 
        </Button> */}
        {/* <Button variant="contained" onClick={handleEditClick} sx={{ ml: 2, mb: 2 }}>
          {isEditMode ? 'Speichern' : 'Bearbeiten'} 
        </Button> */}
        {/* <Button variant="contained" onClick={isEditMode ? handleUpdate : handleEditClick} sx={{ ml: 2, mb: 2 }}> */}
        <Button variant="contained" onClick={handleDualUseButtonClicked} sx={{ ml: 2, mb: 2 }}>
          {isEditMode ? 'Speichern' : 'Bearbeiten'}
        </Button>
      </div>
      
    );
  };

export default Detail;






