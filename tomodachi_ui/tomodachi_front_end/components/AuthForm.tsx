"use client";

import { Box, Button, Typography } from "@mui/material";
import { useState } from "react";
import { UiTextField } from "@/components/baseForm";

type FormMode = "login" | "signup";

export default function AuthForm() {
  const [mode, setMode] = useState<FormMode>("login");

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState(""); // Only for signup

  const handleSubmit = async () => {
    const payload = {
      username,
      password,
      ...(mode === "signup" && { email }),
    };

    try {
      const res = await fetch(`/api/${mode}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Something went wrong");

      const data = await res.json();
      console.log(`${mode} success:`, data);
    } catch (err) {
      console.error("Auth error:", err);
    }
  };

  return (
    <section className="min-h-screen flex items-center justify-center  text-white">
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: 2,
          width: 350,
          padding: 3,
          backgroundColor: "#a9afb696",
          borderRadius: "12px",
        }}
      >
        <Typography variant="h5" align="center" color="black">
          {mode === "login" ? "Login to your account" : "Create a new account"}
        </Typography>

        <UiTextField
          label="Username"
          value={username}
          onChange={setUsername}
        />

        {mode === "signup" && (
          <UiTextField
            label="Email"
            value={email}
            onChange={setEmail}
            //type="email"
          />
        )}

        <UiTextField
          label="Password"
          value={password}
          onChange={setPassword}
          //type="password"
        />

        <Button variant="contained" onClick={handleSubmit}>
          {mode === "login" ? "Login" : "Sign Up"}
        </Button>

        <Typography
          variant="body2"
          align="center"
          className="text-gray-400 cursor-pointer hover:underline"
          onClick={() => setMode(mode === "login" ? "signup" : "login")}
        >
          {mode === "login"
            ? "Don't have an account? Sign up"
            : "Already have an account? Log in"}
        </Typography>
      </Box>
    </section>
  );
}
