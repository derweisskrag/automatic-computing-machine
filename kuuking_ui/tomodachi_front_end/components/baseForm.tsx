import { FormControl, InputLabel, Select, MenuItem, TextField, Button, Box } from "@mui/material";
import { ChangeEventHandler, useState } from "react";


export function UiSelectField<
  IdKey extends string,
  LabelKey extends string,
  Option extends Record<IdKey, number | string | undefined> & Record<LabelKey, string>
>({
  idKey,
  label,
  labelKey,
  onChange,
  options,
  value,
}: {
  label: string;
  idKey: IdKey;
  labelKey: LabelKey;
  value: Option[IdKey];
  onChange: (value: Option[IdKey]) => void;
  options: Option[];
}) {
  return (
    <FormControl variant="outlined" fullWidth>
      <InputLabel>{label}</InputLabel>
      <Select
        value={value}
        onChange={(e) => onChange(e.target.value as Option[IdKey])}
        label={label}
      >
        {options.map((option) => (
          <MenuItem key={option[idKey]} value={option[idKey]}>
            {option[labelKey]}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}


export function UiTextField({
  label,
  onChange,
  value,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  const handleChange: ChangeEventHandler<HTMLInputElement> = (event) => {
    onChange(event.target.value);
  };
  return (
    <TextField
      label={label}
      variant="outlined"
      fullWidth
      value={value}
      onChange={handleChange}
    />
  );
}


export function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = () => {
    // call Rust API here
    console.log("Logging in with", { email, password });
  };

  return (
    <Box component="form" onSubmit={(e) => { e.preventDefault(); handleSubmit(); }} sx={{ gap: 2, display: 'flex', flexDirection: 'column' }}>
      <UiTextField label="Email" value={email} onChange={setEmail} />
      <UiTextField label="Password" value={password} onChange={setPassword} />
      <Button variant="contained" type="submit">Login</Button>
    </Box>
  );
}

