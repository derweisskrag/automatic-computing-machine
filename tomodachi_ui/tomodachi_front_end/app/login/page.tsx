"use client";

import { Box, Button } from "@mui/material";
import { UiTextField, UiSelectField } from "@/components/baseForm";
import AuthForm from "@/components/AuthForm";
import { useState } from "react";

const languageOptions = [
  { id: "en", label: "English" },
  { id: "ru", label: "Russian" },
  { id: "et", label: "Estonian" },
];


export default function Login(){
    const [username, setUsername] = useState("");
    const [language, setLanguage] = useState("en");

    return (
        <section className="">
        <AuthForm />;
        


        {/* 
        
        Form 
        I wanna safe it for now!
        
        */}
        {/* <div>
            <Box sx={{ display: "flex", flexDirection: "column", gap: 2, width: 300 }}>
                <UiTextField
                label="Username"
                value={username}
                onChange={setUsername}
                />

                <UiSelectField
                label="Preferred Language"
                idKey="id"
                labelKey="label"
                value={language}
                onChange={setLanguage}
                options={languageOptions}
                />

                <Button variant="contained" onClick={() => console.log({ username, language })}>
                Submit
                </Button>
            </Box>
        </div> */}
        </section>
    );
}