import { Navigate } from "react-router-dom";
import { supabase } from "./supabase";

export default function AdminRoute({ children }) {
  const user = supabase.auth.getUser();
  const role = localStorage.getItem("role");

  if (!user || role !== "admin") {
    return <Navigate to="/" />;
  }
  return children;
}